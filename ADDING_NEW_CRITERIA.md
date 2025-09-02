# 📥 Adding New Lender Criteria Files

## 🚀 Quick Start (For Your 60 Files)

### Option 1: Batch Processing (Recommended for 60+ files)
```bash
python batch_add_criteria.py
```

**Steps:**
1. Place all 60 files in the `new_criteria_batch/` folder
2. Run the script
3. It will automatically process everything!

### Option 2: Individual Files
```bash
python add_new_criteria.py
```

**Steps:**
1. Place files directly in `residential/` folder
2. Run the script
3. Follow the prompts

## 📋 File Requirements

### ✅ File Format
- **Text files**: `.txt` format
- **PDF files**: `.pdf` format (will be converted to text)

### ✅ Naming Convention
```
lender_name-residential.txt
```

**Examples:**
- `new_bank-residential.txt`
- `building_society-residential.pdf`
- `specialist_lender-residential.txt`

### ✅ Content Requirements
Each file should contain:
- Lender name and contact information
- Eligibility criteria (age, income, employment)
- Property requirements
- Financial criteria (LTV, affordability)
- Documentation requirements

## 🔄 What Happens When You Add Files

### 1. **Text Extraction**
- Converts PDFs to text
- Cleans and formats content
- Extracts metadata

### 2. **Chunking**
- Breaks documents into searchable chunks
- Preserves criteria structure
- Maintains context

### 3. **Embedding Generation**
- Creates vector embeddings for each chunk
- Enables semantic search
- Stores in LanceDB

### 4. **Database Update**
- Adds new chunks to existing database
- Maintains search functionality
- Updates lender configuration

## 🎯 After Adding Files

### 1. **Restart Backend**
```bash
python optimized_backend.py
```

### 2. **Test the System**
Ask questions like:
- "What are the criteria for [new lender]?"
- "What's the maximum age for [new lender]?"
- "What documents does [new lender] require?"

### 3. **Verify Results**
The chatbot will now have access to all new criteria!

## 📊 File Management

### Current Files
Check what's currently in the system:
```bash
ls residential/*.txt
```

### File Count
The system automatically tracks:
- Total number of files
- Last update date
- Lender categories

### Backup
The system automatically creates backups before processing new files.

## 🚨 Troubleshooting

### Common Issues

**1. File Not Found**
- Check file is in correct folder
- Verify file extension (.txt or .pdf)
- Ensure proper naming convention

**2. Processing Errors**
- Check file content is readable
- Verify file isn't corrupted
- Ensure sufficient disk space

**3. Database Issues**
- Restart the backend
- Check database permissions
- Restore from backup if needed

### Getting Help
If you encounter issues:
1. Check the error messages
2. Verify file format and naming
3. Try processing one file at a time
4. Check system logs

## 📈 Performance Tips

### For Large Batches (60+ files)
- Use `batch_add_criteria.py` for efficiency
- Process during off-peak hours
- Ensure sufficient disk space
- Monitor system resources

### For Regular Updates
- Use `add_new_criteria.py` for individual files
- Update monthly or as needed
- Keep backups of important files
- Test after each update

## 🎉 Success!

Once you've added your 60 files:
- ✅ All criteria will be searchable
- ✅ Chatbot will have access to new lenders
- ✅ System will be more comprehensive
- ✅ Users can ask about any lender

**Your mortgage criteria AI system will be even more powerful!** 🚀
