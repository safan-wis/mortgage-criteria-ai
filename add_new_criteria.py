#!/usr/bin/env python3
"""
Quick script to add new lender criteria files to the system
Use this when you have new criteria files to add
"""

import os
import json
import subprocess
from datetime import datetime

def show_current_files():
    """Show current files in residential folder."""
    print("\n📁 Current files in residential folder:")
    current_files = [f for f in os.listdir("residential") if f.endswith(('.txt', '.pdf'))]
    for i, file in enumerate(sorted(current_files), 1):
        print(f"  {i}. {file}")
    print(f"\nTotal: {len(current_files)} files")

def add_new_files():
    """Guide user to add new files."""
    print("\n📥 ADDING NEW CRITERIA FILES")
    print("=" * 50)
    
    print("\n💡 To add new criteria files:")
    print("1. Place your new .txt or .pdf files in the 'residential/' folder")
    print("2. Use naming convention: 'lender_name-residential.txt'")
    print("3. Examples:")
    print("   - new_bank-residential.txt")
    print("   - another_lender-residential.pdf")
    print("4. Press Enter when you've added all files...")
    
    input("\nPress Enter to continue...")

def update_lender_config():
    """Update lender_config.json if needed."""
    config_path = "residential/lender_config.json"
    
    if os.path.exists(config_path):
        print("\n📋 Updating lender configuration...")
        
        # Count current files
        current_files = [f for f in os.listdir("residential") if f.endswith(('.txt', '.pdf'))]
        
        # Load existing config
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Update file count and date
        config['lender_files_config']['total_files'] = len(current_files)
        config['lender_files_config']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        # Save updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Updated config: {len(current_files)} files, updated {config['lender_files_config']['last_updated']}")
    else:
        print("⚠️ No lender_config.json found - will be created automatically")

def process_new_files():
    """Process the new files through the pipeline."""
    print("\n🔄 PROCESSING NEW FILES")
    print("=" * 50)
    
    try:
        # Step 1: Extract text
        print("📚 Step 1: Extracting text from files...")
        result = subprocess.run(["python", "1-extraction.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Text extraction completed")
        else:
            print(f"❌ Text extraction failed: {result.stderr}")
            return False
        
        # Step 2: Create chunks
        print("✂️ Step 2: Creating chunks...")
        result = subprocess.run(["python", "2-chunking.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Chunking completed")
        else:
            print(f"❌ Chunking failed: {result.stderr}")
            return False
        
        # Step 3: Generate embeddings
        print("🧠 Step 3: Generating embeddings...")
        result = subprocess.run(["python", "3-embedding.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Embeddings generated")
        else:
            print(f"❌ Embedding generation failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        return False

def verify_new_files():
    """Verify the new files were added successfully."""
    print("\n🔍 VERIFYING NEW FILES")
    print("=" * 50)
    
    try:
        import lancedb
        
        # Connect to database
        db = lancedb.connect("data/lancedb")
        table = db.open_table("lender_criteria")
        
        # Get total chunks
        total_chunks = table.count_rows()
        print(f"📊 Total criteria chunks: {total_chunks}")
        
        # Get unique lenders
        lenders = set()
        for row in table.search("").limit(1000):
            lender_name = row["metadata"]["lender_name"]
            # Clean up lender name for display
            clean_name = lender_name.replace('_residential.txt', '').replace('_residential.pdf', '')
            clean_name = clean_name.replace('_res', '').replace('_bank', '').replace('_building_society', '')
            clean_name = clean_name.replace('_mortgage', '').replace('_criteria', '')
            clean_name = clean_name.replace('_', ' ').title()
            lenders.add(clean_name)
        
        print(f"🏦 Total lenders in database: {len(lenders)}")
        print("\n📋 All lenders:")
        for lender in sorted(lenders):
            print(f"  • {lender}")
        
        print(f"\n✅ New files added successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

def main():
    """Main process for adding new criteria files."""
    print("🏦 ADD NEW LENDER CRITERIA FILES")
    print("=" * 50)
    print("This script helps you add new lender criteria files to the AI system.")
    print("Perfect for when you get new criteria files (like your 60 files in 3 days)!")
    
    # Show current state
    show_current_files()
    
    # Guide user to add files
    add_new_files()
    
    # Show updated state
    print("\n📁 Files after adding:")
    show_current_files()
    
    # Update configuration
    update_lender_config()
    
    # Process the files
    if process_new_files():
        # Verify the update
        verify_new_files()
        
        print("\n🎉 NEW FILES ADDED SUCCESSFULLY!")
        print("\n💡 Next steps:")
        print("1. Restart your backend: python optimized_backend.py")
        print("2. Test the system: Ask questions about the new lenders")
        print("3. The chatbot will now have access to the new criteria!")
        
    else:
        print("\n❌ FAILED TO ADD NEW FILES!")
        print("💡 Check the error messages above and try again")

if __name__ == "__main__":
    main()
