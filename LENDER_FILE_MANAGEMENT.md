# 📁 Lender File Management Guide

## Overview
This guide explains how to add new lender files, update existing ones, and maintain the AI system's knowledge base.

## 🔄 Update Process Overview

### When to Update
- **Monthly**: Most lenders update criteria monthly
- **Quarterly**: Some building societies update quarterly
- **As Needed**: When lenders announce policy changes

### What Gets Updated
- Lender criteria documents (PDF/TXT files)
- Lender configuration file
- AI system database
- Search functionality

## 📥 Adding New Lender Files

### Step 1: Prepare the File
1. **Download** the latest criteria from the lender's website
2. **Convert** to TXT format if it's a PDF
3. **Name Convention**: `lender_name-residential.txt`
   - Example: `nationwide-residential.txt`
   - Use lowercase, hyphens, no spaces

### Step 2: Place the File
```
residential/
├── new_lender-residential.txt    # Add your new file here
├── lender_config.json            # Will be updated automatically
└── existing_lender_files.txt
```

### Step 3: Update Configuration
The system will automatically detect new files, but you can manually update `lender_config.json`:

```json
{
  "lender_files_config": {
    "total_files": 36,  // Increment this
    "last_updated": "2025-01-XX"  // Update date
  },
  "lender_categories": {
    "major_banks": [
      // Add to appropriate category
      "new_lender-residential.txt"
    ]
  }
}
```

## 🔄 Updating Existing Lender Files

### Step 1: Replace the File
1. **Backup** the old file (optional)
2. **Replace** with the new version
3. **Keep** the same filename
4. **Ensure** it's in TXT format

### Step 2: Verify Content
- Check that the new file contains updated criteria
- Ensure all sections are properly formatted
- Verify lender name consistency

## 🗑️ Removing Lender Files

### Step 1: Remove the File
```bash
rm residential/lender_name-residential.txt
```

### Step 2: Update Configuration
Remove references from `lender_config.json`:
- Remove from appropriate category list
- Decrement total file count
- Update last_updated date

## 🚀 Complete System Update Process

### Option 1: Automated Update (Recommended)
```bash
python3 update_lender_criteria.py
```

This script will:
1. ✅ Backup current database
2. ✅ Process all lender files
3. ✅ Recreate chunks and embeddings
4. ✅ Update the AI system
5. ✅ Verify the update

### Option 2: Manual Update Process

#### Step 1: Extract Text
```bash
python3 1-extraction-fixed.py
```
- Processes all TXT/PDF files in `residential/`
- Creates `processed_lender_docs.json`
- Handles text extraction and cleaning

#### Step 2: Create Chunks
```bash
python3 2-chunking-fixed.py
```
- Breaks documents into searchable chunks
- Preserves criteria structure
- Creates `lender_chunks.json`

#### Step 3: Generate Embeddings
```bash
python3 3-embedding.py
```
- Creates vector embeddings for all chunks
- Stores in LanceDB database
- Enables semantic search

#### Step 4: Verify Update
```bash
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); print(f'Database updated: {table.count_rows()} chunks')"
```

## 📋 File Naming Conventions

### Standard Format
```
{lender_name}-residential.txt
```

### Examples
- `nationwide-residential.txt`
- `hsbc_residential.txt`
- `santander_bank_residential.txt`
- `leeds_building_society_residential.txt`

### Rules
- ✅ Use lowercase letters
- ✅ Use hyphens or underscores (be consistent)
- ✅ Include "residential" identifier
- ✅ Use .txt extension
- ❌ No spaces in filenames
- ❌ No special characters

## 🔍 File Content Requirements

### Required Sections
- **Lender Information**: Name, contact details
- **Eligibility Criteria**: Age, income, employment
- **Property Requirements**: Type, location, condition
- **Financial Criteria**: LTV, affordability, deposits
- **Documentation**: Required paperwork

### Formatting Guidelines
- Use clear headings (###, ##, #)
- Include specific numbers and percentages
- Organize information logically
- Use bullet points for lists
- Include examples where helpful

## 🗄️ Database Management

### Backup Before Updates
```bash
# Create backup directory
mkdir -p backups/$(date +%Y-%m-%d)

# Copy database
cp -r data/lancedb/lender_criteria.lance backups/$(date +%Y-%m-%d)/

# Copy configuration
cp residential/lender_config.json backups/$(date +%Y-%m-%d)/
```

### Restore from Backup
```bash
# Stop the application first
pkill -f streamlit

# Restore database
rm -rf data/lancedb/lender_criteria.lance
cp -r backups/2025-01-XX/lender_criteria.lance data/lancedb/

# Restore configuration
cp backups/2025-01-XX/lender_config.json residential/

# Restart application
streamlit run 5-chat.py
```

## 🧪 Testing Updates

### Test Questions
After updating, test with:
1. **New Lender**: "What are the criteria for [new_lender]?"
2. **Updated Criteria**: "What is the current maximum LTV for [lender]?"
3. **General Search**: "Find lenders that accept [specific_criteria]"

### Expected Results
- ✅ New lender appears in search results
- ✅ Updated criteria is current and accurate
- ✅ Search returns relevant, recent information
- ✅ AI responses cite correct lender names

## 🚨 Troubleshooting

### Common Issues

#### Issue: New lender not found
**Solution**: Check file naming and run complete update process

#### Issue: Old criteria still showing
**Solution**: Clear browser cache and restart Streamlit app

#### Issue: Database errors
**Solution**: Restore from backup and re-run update process

#### Issue: Search not working
**Solution**: Verify database has correct vector schema

### Debug Commands
```bash
# Check database status
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); print(f'Rows: {db.open_table(\"lender_criteria\").count_rows()}')"

# Check specific lender
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); results = table.to_pandas(); print(results[results['metadata'].apply(lambda x: 'nationwide' in x['lender_name'].lower())].shape[0])"

# Test search functionality
python3 -c "import lancedb; from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); response = client.embeddings.create(input='test query', model='text-embedding-ada-002'); results = table.search(response.data[0].embedding, vector_column_name='embedding').limit(1).to_pandas(); print(f'Search working: {len(results)} results')"
```

## 📅 Maintenance Schedule

### Daily
- Monitor system performance
- Check for error logs

### Weekly
- Review search quality
- Test with sample queries

### Monthly
- Update lender criteria files
- Run complete system update
- Verify all lenders are current

### Quarterly
- Review and optimize chunking strategy
- Update system prompts if needed
- Performance optimization

## 💡 Best Practices

1. **Always backup** before major updates
2. **Test thoroughly** after each update
3. **Keep filenames consistent** across updates
4. **Document changes** in a changelog
5. **Monitor system performance** regularly
6. **Use automated scripts** when possible
7. **Verify content quality** before processing
8. **Maintain regular update schedule**

---

*This guide ensures your AI mortgage advisor system stays current and accurate. Regular updates are essential for providing reliable advice to clients.*



