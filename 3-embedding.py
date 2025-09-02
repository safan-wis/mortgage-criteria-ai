from typing import List
import pickle
import lancedb
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from openai import OpenAI
from utils.tokenizer import OpenAITokenizerWrapper

load_dotenv()

# Initialize OpenAI client (make sure you have OPENAI_API_KEY in your environment variables)
client = OpenAI()

tokenizer = OpenAITokenizerWrapper()  # Load our custom tokenizer for OpenAI
MAX_TOKENS = 8191  # text-embedding-3-large's maximum context length

# --------------------------------------------------------------
# Load lender chunks from previous step
# --------------------------------------------------------------

def load_lender_chunks():
    """Load the chunked lender documents from the previous step."""
    try:
        with open("lender_chunks.json", "r", encoding='utf-8') as f:
            import json
            chunks_data = json.load(f)
            return chunks_data
    except FileNotFoundError:
        print("❌ No lender chunks found. Please run 2-chunking-fixed.py first.")
        return None

# --------------------------------------------------------------
# Create a LanceDB database and table for lender criteria
# --------------------------------------------------------------

def create_lender_database():
    """Create LanceDB database and table for lender criteria."""
    print("🗄️ Creating LanceDB database for lender criteria...")
    
    # Create a LanceDB database
    db = lancedb.connect("data/lancedb")
    
    # Get the OpenAI embedding function
    func = get_registry().get("openai").create(name="text-embedding-3-large")
    
    # Define comprehensive metadata schema for lender criteria
    class LenderCriteriaMetadata(LanceModel):
        """
        Metadata schema for lender criteria chunks.
        Fields must be in alphabetical order for Pydantic.
        """
        
        chunk_id: str
        criteria_section: str | None
        filename: str
        lender_name: str
        page_numbers: List[int] | None
        source_type: str  # 'text' or 'pdf'
        title: str | None
    
    # Define the main schema for lender criteria chunks
    class LenderCriteriaChunks(LanceModel):
        text: str = func.SourceField()
        vector: Vector(func.ndims()) = func.VectorField()
        metadata: LenderCriteriaMetadata
    
    # Create table with comprehensive schema
    table = db.create_table("lender_criteria", schema=LenderCriteriaChunks, mode="overwrite")
    
    print("✅ Created lender_criteria table")
    return table, func

# --------------------------------------------------------------
# Prepare lender chunks for the database
# --------------------------------------------------------------

def prepare_lender_chunks_for_db(chunks, func):
    """Prepare lender chunks for database insertion with comprehensive metadata."""
    print("🔧 Preparing lender chunks for database...")
    
    processed_chunks = []
    
    for i, chunk in enumerate(chunks):
        try:
            # Extract text content
            chunk_text = chunk['text'] if isinstance(chunk, dict) else str(chunk)
            
            # Extract metadata
            lender_name = chunk.get('meta', {}).get('lender_name', 'Unknown Lender') if isinstance(chunk, dict) else 'Unknown Lender'
            filename = chunk.get('meta', {}).get('source_file', 'Unknown File') if isinstance(chunk, dict) else 'Unknown File'
            
            # Determine source type
            source_type = 'pdf' if filename.lower().endswith('.pdf') else 'text'
            
            # Extract criteria section from headings if available
            criteria_section = None
            if isinstance(chunk, dict) and chunk.get('meta', {}).get('headings'):
                criteria_section = chunk['meta']['headings'][0] if chunk['meta']['headings'] else None
            
            # Extract page numbers if available
            page_numbers = None
            if isinstance(chunk, dict) and chunk.get('meta', {}).get('doc_items'):
                try:
                    pages = set()
                    for item in chunk['meta']['doc_items']:
                        if hasattr(item, 'prov'):
                            for prov in item.prov:
                                if hasattr(prov, 'page_no'):
                                    pages.add(prov.page_no)
                    page_numbers = sorted(list(pages)) if pages else None
                except:
                    page_numbers = None
            
            # Create chunk data
            chunk_data = {
                "text": chunk_text,
                "metadata": {
                    "chunk_id": f"chunk_{i:06d}",
                    "criteria_section": criteria_section,
                    "filename": filename,
                    "lender_name": lender_name,
                    "page_numbers": page_numbers,
                    "source_type": source_type,
                    "title": criteria_section
                }
            }
            
            processed_chunks.append(chunk_data)
            
        except Exception as e:
            print(f"❌ Error processing chunk {i}: {str(e)}")
            continue
    
    print(f"✅ Prepared {len(processed_chunks)} chunks for database")
    return processed_chunks

# --------------------------------------------------------------
# Main embedding and database creation process
# --------------------------------------------------------------

if __name__ == "__main__":
    # Load lender chunks
    chunks = load_lender_chunks()
    
    if chunks:
        print(f"📚 Processing {len(chunks)} lender criteria chunks...")
        
        # Create database and table
        table, func = create_lender_database()
        
        # Prepare chunks for database
        processed_chunks = prepare_lender_chunks_for_db(chunks, func)
        
        # Add chunks to database (automatically creates embeddings)
        print("🚀 Adding chunks to database and generating embeddings...")
        table.add(processed_chunks)
        
        # Display database statistics
        print(f"\n📊 Database Statistics:")
        print(f"   Total chunks: {table.count_rows()}")
        
        # Show sample data
        print(f"\n🔍 Sample data from database:")
        sample_data = table.to_pandas().head(3)
        for _, row in sample_data.iterrows():
            print(f"   Lender: {row['metadata']['lender_name']}")
            print(f"   Section: {row['metadata']['criteria_section']}")
            print(f"   Text preview: {row['text'][:100]}...")
            print()
        
        print("🎯 Lender criteria database created successfully!")
        print("📋 Ready for search and chat functionality!")
        
    else:
        print("❌ No chunks to process. Please run 2-chunking.py first.")
