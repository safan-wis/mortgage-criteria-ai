# 📚 Quick Reference Guide

## 🚀 Essential Commands

### Start the Application
```bash
streamlit run 5-chat.py
```

### Stop the Application
```bash
pkill -f streamlit
```

### Check Database Status
```bash
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); print(f'Database rows: {table.count_rows()}')"
```

### Test Search Functionality
```bash
python3 -c "import lancedb; from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); response = client.embeddings.create(input='test', model='text-embedding-ada-002'); results = table.search(response.data[0].embedding, vector_column_name='embedding').limit(1).to_pandas(); print(f'Search working: {len(results)} results')"
```

## 🔄 Update Commands

### Complete System Update
```bash
python3 update_lender_criteria.py
```

### Manual Update Process
```bash
# Step 1: Extract text
python3 1-extraction-fixed.py

# Step 2: Create chunks
python3 2-chunking-fixed.py

# Step 3: Generate embeddings
python3 3-embedding.py
```

### Check Update Status
```bash
# Check processed documents
ls -la processed_lender_docs.*

# Check chunks
ls -la lender_chunks.*

# Check database
ls -la data/lancedb/
```

## 📁 File Management

### Add New Lender File
```bash
# Copy new file to residential folder
cp new_lender-residential.txt residential/

# Update system
python3 update_lender_criteria.py
```

### Remove Lender File
```bash
# Remove file
rm residential/lender_name-residential.txt

# Update system
python3 update_lender_criteria.py
```

### Backup Database
```bash
# Create backup
mkdir -p backups/$(date +%Y-%m-%d)
cp -r data/lancedb/lender_criteria.lance backups/$(date +%Y-%m-%d)/
cp residential/lender_config.json backups/$(date +%Y-%m-%d)/
```

### Restore from Backup
```bash
# Stop app
pkill -f streamlit

# Restore database
rm -rf data/lancedb/lender_criteria.lance
cp -r backups/2025-01-XX/lender_criteria.lance data/lancedb/

# Restore config
cp backups/2025-01-XX/lender_config.json residential/

# Restart app
streamlit run 5-chat.py
```

## 🧪 Testing Commands

### Test Specific Lender
```bash
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); results = table.to_pandas(); nationwide_results = results[results['metadata'].apply(lambda x: 'nationwide' in x['lender_name'].lower())]; print(f'Found {len(nationwide_results)} Nationwide chunks')"
```

### Test Search Quality
```bash
python3 -c "import lancedb; from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); query = 'What is the minimum age for mortgage applicants in Nationwide?'; response = client.embeddings.create(input=query, model='text-embedding-ada-002'); results = table.search(response.data[0].embedding, vector_column_name='embedding').limit(5).to_pandas(); nationwide_results = results[results['metadata'].apply(lambda x: 'nationwide' in x['lender_name'].lower())]; print(f'Query: {query}'); print(f'Found {len(results)} total results, {len(nationwide_results)} Nationwide results')"
```

## 🚨 Troubleshooting Commands

### Check System Health
```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep -E "(streamlit|lancedb|openai)"

# Check environment variables
echo $OPENAI_API_KEY

# Check file permissions
ls -la data/lancedb/
ls -la residential/
```

### Fix Common Issues

#### Database Connection Error
```bash
# Check database exists
ls -la data/lancedb/lender_criteria.lance/

# Recreate database if needed
python3 update_lender_criteria.py
```

#### Search Not Working
```bash
# Check database schema
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); print('Schema:', table.schema)"

# Check embeddings
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); df = table.to_pandas(); print('Sample embedding:', df['embedding'].iloc[0][:5] if not df.empty else 'No data')"
```

#### OpenAI API Errors
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connection
python3 -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('API key valid:', bool(client.api_key))"
```

## 📊 System Information

### Current Status
```bash
# Database size
du -sh data/lancedb/

# File counts
echo "Lender files: $(ls residential/*.txt | wc -l)"
echo "PDF files: $(ls residential/*.pdf | wc -l)"
echo "Total files: $(ls residential/* | wc -l)"

# Database rows
python3 -c "import lancedb; db = lancedb.connect('data/lancedb/lender_criteria.lance'); table = db.open_table('lender_criteria'); print(f'Database chunks: {table.count_rows()}')"
```

### Performance Metrics
```bash
# Check memory usage
ps aux | grep streamlit

# Check disk usage
df -h .

# Check system resources
top -l 1 | head -10
```

## 🔧 Configuration

### Environment Setup
```bash
# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Load environment
source .env

# Verify
echo $OPENAI_API_KEY
```

### Streamlit Configuration
```bash
# Create config file
mkdir -p ~/.streamlit
echo "[server]" > ~/.streamlit/config.toml
echo "port = 8501" >> ~/.streamlit/config.toml
echo "address = '0.0.0.0'" >> ~/.streamlit/config.toml
```

## 📱 Application URLs

### Local Access
- **Main App**: http://localhost:8501
- **Network Access**: http://your_ip:8501

### Default Ports
- **Streamlit**: 8501
- **Alternative**: 8502, 8503 (if 8501 is busy)

## 🎯 Quick Tests

### Test 1: Basic Functionality
1. Start app: `streamlit run 5-chat.py`
2. Open browser to http://localhost:8501
3. Ask: "What is the minimum age for mortgage applicants in Nationwide?"
4. Expected: Clear answer citing Nationwide criteria

### Test 2: Search Quality
1. Ask: "Compare maximum LTV between HSBC and Santander"
2. Expected: Detailed comparison with specific numbers

### Test 3: System Performance
1. Ask multiple questions quickly
2. Expected: Responses in <2 seconds each
3. Check for consistent formatting

## 💡 Pro Tips

1. **Always backup** before major updates
2. **Test thoroughly** after each update
3. **Monitor performance** regularly
4. **Keep filenames consistent**
5. **Use automated scripts** when possible
6. **Check logs** for errors
7. **Verify data quality** before processing
8. **Maintain regular update schedule**

---

*This quick reference provides essential commands and troubleshooting steps for daily system management.*



