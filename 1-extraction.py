from docling.document_converter import DocumentConverter
from utils.sitemap import get_sitemap_urls
import os
from pathlib import Path
import json

converter = DocumentConverter()

# --------------------------------------------------------------
# Process all residential lender files
# --------------------------------------------------------------

def get_residential_files():
    """Get all residential lender files for processing."""
    residential_dir = Path("residential")
    
    # Get all text and PDF files
    txt_files = list(residential_dir.glob("*.txt"))
    pdf_files = list(residential_dir.glob("*.pdf"))
    
    # Filter out non-lender files
    exclude_files = {
        'README_LENDER_FILES.md', 'ANALYSIS_SUMMARY.md', 'PROCESSING_PLAN.md',
        'lender_config.json', 'header_template.txt'
    }
    
    txt_files = [f for f in txt_files if f.name not in exclude_files]
    pdf_files = [f for f in pdf_files if f.name not in exclude_files]
    
    return txt_files + pdf_files

def extract_lender_name(filename):
    """Extract clean lender name from filename."""
    # Remove common suffixes
    name = filename.replace('_residential.txt', '').replace('_residential.pdf', '')
    name = name.replace('_res', '').replace('_bank', '').replace('_building_society', '')
    name = name.replace('_mortgage', '').replace('_criteria', '')
    
    # Convert to title case
    name = name.replace('_', ' ').title()
    
    return name

def process_residential_files():
    """Process all residential lender files and extract content."""
    print("🚀 Processing all residential lender files...")
    
    files = get_residential_files()
    print(f"📁 Found {len(files)} lender files to process")
    
    processed_docs = []
    
    for file_path in files:
        try:
            print(f"📄 Processing: {file_path.name}")
            
            # Extract lender name
            lender_name = extract_lender_name(file_path.name)
            
            # Convert document
            result = converter.convert(str(file_path))
            
            if result.document:
                # Add lender metadata
                result.document.meta.lender_name = lender_name
                result.document.meta.source_file = file_path.name
                
                # Convert to markdown and store
                markdown_output = result.document.export_to_markdown()
                
                processed_docs.append({
                    'lender_name': lender_name,
                    'filename': file_path.name,
                    'content': markdown_output,
                    'document': result.document
                })
                
                print(f"✅ Processed: {lender_name} ({file_path.name})")
            else:
                print(f"❌ Failed to process: {file_path.name}")
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
    
    print(f"\n🎯 Successfully processed {len(processed_docs)} lender files")
    return processed_docs

# --------------------------------------------------------------
# Main processing
# --------------------------------------------------------------

if __name__ == "__main__":
    # Process all residential files
    processed_docs = process_residential_files()
    
    # Save processed documents for next step
    import pickle
    with open("processed_lender_docs.pkl", "wb") as f:
        pickle.dump(processed_docs, f)
    
    print(f"\n💾 Saved {len(processed_docs)} processed documents to processed_lender_docs.pkl")
    print("📋 Ready for chunking and embedding!")
