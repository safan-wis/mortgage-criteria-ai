#!/usr/bin/env python3
"""
Batch script to add multiple new lender criteria files at once
Perfect for adding 60+ files efficiently
"""

import os
import json
import subprocess
from datetime import datetime
import shutil

def create_backup():
    """Create backup before processing."""
    backup_dir = f"data/lancedb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if os.path.exists("data/lancedb"):
        print(f"📦 Creating backup: {backup_dir}")
        shutil.copytree("data/lancedb", backup_dir)
        print(f"✅ Backup created: {backup_dir}")
        return backup_dir
    return None

def prepare_batch_folder():
    """Create a batch processing folder."""
    batch_folder = "new_criteria_batch"
    
    if not os.path.exists(batch_folder):
        os.makedirs(batch_folder)
        print(f"📁 Created batch folder: {batch_folder}")
    
    return batch_folder

def show_batch_instructions():
    """Show instructions for batch processing."""
    print("\n📥 BATCH PROCESSING INSTRUCTIONS")
    print("=" * 60)
    print("\n💡 To add your 60 new criteria files:")
    print("1. Create a folder called 'new_criteria_batch' (already created)")
    print("2. Place ALL your new .txt/.pdf files in that folder")
    print("3. Use naming convention: 'lender_name-residential.txt'")
    print("4. Examples:")
    print("   - new_bank_1-residential.txt")
    print("   - another_lender_2-residential.pdf")
    print("   - building_society_3-residential.txt")
    print("5. Press Enter when ALL files are ready...")
    
    input("\nPress Enter to continue with batch processing...")

def move_files_to_residential():
    """Move files from batch folder to residential folder."""
    batch_folder = "new_criteria_batch"
    residential_folder = "residential"
    
    if not os.path.exists(batch_folder):
        print(f"❌ Batch folder not found: {batch_folder}")
        return 0
    
    moved_count = 0
    files = [f for f in os.listdir(batch_folder) if f.endswith(('.txt', '.pdf'))]
    
    print(f"\n📁 Moving {len(files)} files from batch folder to residential...")
    
    for file in files:
        src = os.path.join(batch_folder, file)
        dst = os.path.join(residential_folder, file)
        
        # Check if file already exists
        if os.path.exists(dst):
            print(f"⚠️ File already exists, skipping: {file}")
            continue
        
        try:
            shutil.move(src, dst)
            print(f"✅ Moved: {file}")
            moved_count += 1
        except Exception as e:
            print(f"❌ Failed to move {file}: {str(e)}")
    
    print(f"\n📊 Successfully moved {moved_count} files")
    return moved_count

def update_lender_config_batch():
    """Update lender configuration for batch processing."""
    config_path = "residential/lender_config.json"
    
    print("\n📋 Updating lender configuration...")
    
    # Count all files
    all_files = [f for f in os.listdir("residential") if f.endswith(('.txt', '.pdf'))]
    
    if os.path.exists(config_path):
        # Load existing config
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        # Create new config
        config = {
            "lender_files_config": {
                "total_files": 0,
                "last_updated": ""
            },
            "lender_categories": {
                "major_banks": [],
                "building_societies": [],
                "specialist_lenders": []
            }
        }
    
    # Update file count and date
    config['lender_files_config']['total_files'] = len(all_files)
    config['lender_files_config']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Updated config: {len(all_files)} total files")
    return len(all_files)

def process_batch_files():
    """Process all files through the pipeline."""
    print("\n🔄 PROCESSING BATCH FILES")
    print("=" * 50)
    
    try:
        # Step 1: Extract text
        print("📚 Step 1: Extracting text from all files...")
        result = subprocess.run(["python", "1-extraction.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Text extraction completed")
        else:
            print(f"❌ Text extraction failed: {result.stderr}")
            return False
        
        # Step 2: Create chunks
        print("✂️ Step 2: Creating chunks from all content...")
        result = subprocess.run(["python", "2-chunking.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Chunking completed")
        else:
            print(f"❌ Chunking failed: {result.stderr}")
            return False
        
        # Step 3: Generate embeddings
        print("🧠 Step 3: Generating embeddings for all chunks...")
        result = subprocess.run(["python", "3-embedding.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Embeddings generated")
        else:
            print(f"❌ Embedding generation failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error during batch processing: {str(e)}")
        return False

def verify_batch_results():
    """Verify the batch processing results."""
    print("\n🔍 VERIFYING BATCH RESULTS")
    print("=" * 50)
    
    try:
        import lancedb
        
        # Connect to database
        db = lancedb.connect("data/lancedb")
        table = db.open_table("lender_criteria")
        
        # Get total chunks
        total_chunks = table.count_rows()
        print(f"📊 Total criteria chunks in database: {total_chunks}")
        
        # Get unique lenders
        lenders = set()
        for row in table.search("").limit(2000):  # Increased limit for more files
            lender_name = row["metadata"]["lender_name"]
            # Clean up lender name for display
            clean_name = lender_name.replace('_residential.txt', '').replace('_residential.pdf', '')
            clean_name = clean_name.replace('_res', '').replace('_bank', '').replace('_building_society', '')
            clean_name = clean_name.replace('_mortgage', '').replace('_criteria', '')
            clean_name = clean_name.replace('_', ' ').title()
            lenders.add(clean_name)
        
        print(f"🏦 Total lenders in database: {len(lenders)}")
        print(f"\n📋 All lenders (showing first 20):")
        for i, lender in enumerate(sorted(lenders)[:20], 1):
            print(f"  {i:2d}. {lender}")
        
        if len(lenders) > 20:
            print(f"  ... and {len(lenders) - 20} more lenders")
        
        print(f"\n✅ Batch processing completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

def cleanup_batch_folder():
    """Clean up the batch processing folder."""
    batch_folder = "new_criteria_batch"
    
    if os.path.exists(batch_folder):
        remaining_files = [f for f in os.listdir(batch_folder) if f.endswith(('.txt', '.pdf'))]
        
        if remaining_files:
            print(f"\n⚠️ {len(remaining_files)} files still in batch folder:")
            for file in remaining_files:
                print(f"  • {file}")
            print("💡 These files were not moved (possibly duplicates)")
        else:
            print(f"\n🧹 Batch folder is empty - cleaning up...")
            os.rmdir(batch_folder)
            print("✅ Batch folder cleaned up")

def main():
    """Main batch processing function."""
    print("🏦 BATCH ADD LENDER CRITERIA FILES")
    print("=" * 60)
    print("This script helps you add 60+ new lender criteria files efficiently!")
    print("Perfect for bulk updates when you get many new criteria files.")
    
    # Create backup
    print("\n📦 STEP 1: Creating backup...")
    backup_dir = create_backup()
    
    # Prepare batch folder
    print("\n📁 STEP 2: Preparing batch folder...")
    prepare_batch_folder()
    
    # Show instructions
    show_batch_instructions()
    
    # Move files
    print("\n📥 STEP 3: Moving files to residential folder...")
    moved_count = move_files_to_residential()
    
    if moved_count == 0:
        print("❌ No files were moved. Please check your batch folder.")
        return
    
    # Update configuration
    print("\n📋 STEP 4: Updating configuration...")
    total_files = update_lender_config_batch()
    
    # Process files
    print("\n🔄 STEP 5: Processing all files...")
    if process_batch_files():
        # Verify results
        print("\n🔍 STEP 6: Verifying results...")
        verify_batch_results()
        
        # Cleanup
        print("\n🧹 STEP 7: Cleaning up...")
        cleanup_batch_folder()
        
        print("\n🎉 BATCH PROCESSING COMPLETED SUCCESSFULLY!")
        print(f"\n📊 Summary:")
        print(f"  • Files moved: {moved_count}")
        print(f"  • Total files: {total_files}")
        print(f"  • Backup created: {backup_dir}")
        
        print("\n💡 Next steps:")
        print("1. Restart your backend: python optimized_backend.py")
        print("2. Test the system with questions about new lenders")
        print("3. The chatbot now has access to all new criteria!")
        
    else:
        print("\n❌ BATCH PROCESSING FAILED!")
        if backup_dir:
            print(f"💡 You can restore from backup: {backup_dir}")

if __name__ == "__main__":
    main()
