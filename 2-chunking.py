from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI
from utils.tokenizer import OpenAITokenizerWrapper
import pickle
from pathlib import Path

load_dotenv()

# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
client = OpenAI()

tokenizer = OpenAITokenizerWrapper()  # Load our custom tokenizer for OpenAI
MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length

# --------------------------------------------------------------
# Load processed lender documents
# --------------------------------------------------------------

def load_processed_docs():
    """Load the processed lender documents from the previous step."""
    try:
        with open("processed_lender_docs.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("❌ No processed documents found. Please run 1-extraction.py first.")
        return None

# --------------------------------------------------------------
# Apply hybrid chunking to all lender documents
# --------------------------------------------------------------

def chunk_lender_documents(processed_docs):
    """Apply hybrid chunking to all lender documents with metadata preservation."""
    print("🔪 Applying hybrid chunking to all lender documents...")
    
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True,
    )
    
    all_chunks = []
    
    for doc_info in processed_docs:
        lender_name = doc_info['lender_name']
        filename = doc_info['filename']
        document = doc_info['document']
        
        print(f"📄 Chunking: {lender_name} ({filename})")
        
        try:
            # Apply chunking
            chunk_iter = chunker.chunk(dl_doc=document)
            chunks = list(chunk_iter)
            
            # Add lender metadata to each chunk
            for chunk in chunks:
                # Ensure chunk has metadata
                if not hasattr(chunk, 'meta'):
                    chunk.meta = type('Meta', (), {})()
                
                # Add lender information
                chunk.meta.lender_name = lender_name
                chunk.meta.source_file = filename
                
                # Add chunk to collection
                all_chunks.append(chunk)
            
            print(f"✅ Created {len(chunks)} chunks for {lender_name}")
            
        except Exception as e:
            print(f"❌ Error chunking {lender_name}: {str(e)}")
    
    print(f"\n🎯 Total chunks created: {len(all_chunks)}")
    return all_chunks

# --------------------------------------------------------------
# Main chunking process
# --------------------------------------------------------------

if __name__ == "__main__":
    # Load processed documents
    processed_docs = load_processed_docs()
    
    if processed_docs:
        # Apply chunking
        all_chunks = chunk_lender_documents(processed_docs)
        
        # Save chunks for next step
        with open("lender_chunks.pkl", "wb") as f:
            pickle.dump(all_chunks, f)
        
        print(f"\n💾 Saved {len(all_chunks)} chunks to lender_chunks.pkl")
        print("📋 Ready for embedding and database creation!")
        
        # Display chunk statistics
        lender_stats = {}
        for chunk in all_chunks:
            lender = chunk.meta.lender_name
            if lender not in lender_stats:
                lender_stats[lender] = 0
            lender_stats[lender] += 1
        
        print("\n📊 Chunks per lender:")
        for lender, count in sorted(lender_stats.items()):
            print(f"   {lender}: {count} chunks")
    else:
        print("❌ No documents to process. Please run 1-extraction.py first.")
