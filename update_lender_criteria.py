#!/usr/bin/env python3
"""
Automated Lender Criteria Update Script
Updates the AI system when lender criteria files change
"""

import os
import shutil
import json
import subprocess
from datetime import datetime
import streamlit as st

def backup_current_database():
    """Create a backup of the current database."""
    backup_dir = f"data/lancedb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if os.path.exists("data/lancedb"):
        print(f"📦 Creating backup: {backup_dir}")
        shutil.copytree("data/lancedb", backup_dir)
        print(f"✅ Backup created successfully: {backup_dir}")
        return backup_dir
    else:
        print("⚠️ No existing database found to backup")
        return None

def update_lender_files():
    """Interactive file update process."""
    print("\n🔄 LENDER FILE UPDATE PROCESS")
    print("=" * 50)
    
    # Show current files
    print("\n📁 Current files in residential folder:")
    current_files = os.listdir("residential")
    for i, file in enumerate(sorted(current_files), 1):
        if file.endswith(('.txt', '.pdf')):
            print(f"  {i}. {file}")
    
    print("\n💡 To update files:")
    print("1. Replace/remove files in the 'residential' folder")
    print("2. Update 'residential/lender_config.json' if adding/removing lenders")
    print("3. Press Enter when ready to continue...")
    
    input("Press Enter to continue with database refresh...")

def refresh_ai_system():
    """Refresh the AI system with updated criteria."""
    print("\n🤖 REFRESHING AI SYSTEM")
    print("=" * 50)
    
    try:
        # Run the setup pipeline
        print("📚 Step 1: Extracting text from files...")
        result = subprocess.run(["python", "1-extraction.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Text extraction completed")
        else:
            print(f"❌ Text extraction failed: {result.stderr}")
            return False
        
        print("✂️ Step 2: Chunking content...")
        result = subprocess.run(["python", "2-chunking.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Chunking completed")
        else:
            print(f"❌ Chunking failed: {result.stderr}")
            return False
        
        print("🧠 Step 3: Generating embeddings...")
        result = subprocess.run(["python", "3-embedding.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Embeddings generated")
        else:
            print(f"❌ Embedding generation failed: {result.stderr}")
            return False
        
        print("✅ AI system refresh completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during refresh: {str(e)}")
        return False

def verify_update():
    """Verify the database update was successful."""
    print("\n🔍 VERIFYING UPDATE")
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
        
        print(f"🏦 Lenders in database: {len(lenders)}")
        for lender in sorted(lenders):
            print(f"  • {lender}")
        
        print(f"\n✅ Database verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

def main():
    """Main update process."""
    print("🏦 LENDER CRITERIA UPDATE SYSTEM")
    print("=" * 50)
    print("This script will help you update lender criteria and refresh the AI system.")
    print("Use this when lenders update their criteria (typically monthly).")
    
    # Step 1: Backup
    print("\n📦 STEP 1: Creating backup...")
    backup_dir = backup_current_database()
    
    # Step 2: Update files
    print("\n📁 STEP 2: Update lender files...")
    update_lender_files()
    
    # Step 3: Refresh system
    print("\n🤖 STEP 3: Refreshing AI system...")
    if refresh_ai_system():
        # Step 4: Verify
        print("\n🔍 STEP 4: Verifying update...")
        verify_update()
        
        print("\n🎉 UPDATE PROCESS COMPLETED SUCCESSFULLY!")
        print("\n💡 Next steps:")
        print("1. Test the updated system: streamlit run 5-chat.py")
        print("2. Ask questions to verify new criteria is working")
        print("3. If issues occur, restore from backup: " + (backup_dir or "N/A"))
    else:
        print("\n❌ UPDATE FAILED!")
        if backup_dir:
            print(f"💡 You can restore from backup: {backup_dir}")

if __name__ == "__main__":
    main()



