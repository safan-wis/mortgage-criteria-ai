# 🏦 AI Mortgage Advisor System

## Overview
An intelligent AI-powered system that provides instant access to comprehensive UK mortgage lender criteria from 30+ major lenders. Built with Streamlit, OpenAI, and LanceDB for fast, accurate mortgage advice.

## 🚀 Features
- **Instant Access**: Get mortgage criteria answers in seconds
- **30+ Lenders**: Comprehensive coverage of major UK mortgage providers
- **AI-Powered**: Uses GPT-4 for intelligent, contextual responses
- **Vector Search**: Fast, accurate retrieval of relevant criteria
- **Clean Interface**: User-friendly Streamlit web application

## 🏗️ System Architecture

### Core Components
1. **Document Processing Pipeline**
   - Text extraction from PDF/TXT files
   - Intelligent chunking for optimal search
   - Vector embedding generation

2. **Vector Database (LanceDB)**
   - Stores 4000+ criteria chunks
   - Fast semantic search capabilities
   - Efficient storage and retrieval

3. **AI Chat Interface**
   - Streamlit web application
   - OpenAI GPT-4 integration
   - Context-aware responses

## 📁 File Structure
```
docling/
├── 5-chat.py                 # Main Streamlit application
├── 1-extraction-fixed.py     # Document text extraction
├── 2-chunking-fixed.py       # Document chunking
├── 3-embedding.py            # Vector embedding generation
├── residential/              # Lender criteria files
│   ├── lender_config.json    # Lender configuration
│   ├── nationwide-residential.txt
│   ├── hsbc_residential.txt
│   └── ... (30+ lender files)
├── data/
│   └── lancedb/             # Vector database
└── utils/                    # Utility functions
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Launch the Application
```bash
streamlit run 5-chat.py
```

### 4. Access the App
Open your browser to `http://localhost:8501`

## 💬 How to Use

### Basic Questions
- "What is the maximum age for mortgage applicants in HSBC?"
- "What are the income requirements for Barclays?"
- "What is the minimum deposit for first-time buyers with Nationwide?"

### Advanced Queries
- "Compare maximum LTV between Santander and Halifax"
- "What are the criteria for self-employed borrowers across all lenders?"
- "Find lenders that accept gifted deposits"

## 🔧 How It Works

### 1. User Input Processing
- User types a question
- System creates vector embedding of the query
- Searches database for relevant criteria chunks

### 2. Context Retrieval
- Finds most relevant chunks based on semantic similarity
- Retrieves lender names, criteria sections, and text content
- Formats context for AI processing

### 3. AI Response Generation
- Sends user query + retrieved context to GPT-4
- AI generates comprehensive, accurate response
- Response cites specific lenders and criteria

### 4. Result Display
- Clean, formatted response in chat interface
- Shows source information
- Maintains conversation history

## 📊 Current Lenders
- **Major Banks**: HSBC, Barclays, Santander, NatWest
- **Building Societies**: Nationwide, Coventry, Leeds, Skipton
- **Specialist Lenders**: Fleet, Kent Reliance, Moda Mortgages
- **And 20+ more lenders**

## 🛠️ Technical Details

### AI Models Used
- **Embeddings**: OpenAI text-embedding-ada-002 (1536 dimensions)
- **Chat**: OpenAI GPT-4 for intelligent responses
- **Vector Database**: LanceDB for fast similarity search

### Performance
- **Search Speed**: <1 second for most queries
- **Database Size**: ~4000 chunks, ~50MB
- **Response Quality**: High accuracy with source citations

## 🔒 Security & Privacy
- No personal data stored
- All criteria sourced from public lender documents
- OpenAI API calls for processing only
- Local vector database storage

## 📈 System Benefits
- **For Advisors**: Instant access to current criteria
- **For Clients**: Quick, accurate mortgage guidance
- **For Lenders**: Consistent information distribution
- **For Industry**: Standardized criteria access

---

*This system provides professional mortgage advice based on current lender criteria. Always verify information with lenders directly for the most up-to-date requirements.*



