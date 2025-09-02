# 🏦 Mortgage Criteria AI - Next.js Version

This is a Next.js implementation of the mortgage criteria chat application, replacing the Streamlit interface with the exact same functionality.

## Features

- 💬 **Interactive Chat Interface** - Ask questions about mortgage criteria in natural language
- 🔍 **Advanced Search** - Search across 30+ UK lender criteria with vector similarity
- 🎯 **Lender Filtering** - Filter results by specific lenders
- 📊 **Search Results Panel** - View detailed search results with source attribution
- 🏦 **100% Accurate Responses** - AI responses based only on actual lender criteria
- 📱 **Responsive Design** - Modern, professional interface with Tailwind CSS

## Architecture

This application consists of two parts:

1. **Next.js Frontend** (`mortgage-ai-ui/`) - Modern React-based UI
2. **Python Backend** (`python_backend.py`) - FastAPI service handling LanceDB operations

## Setup Instructions

### 1. Environment Variables

Create a `.env.local` file in the `mortgage-ai-ui` directory with:

```bash
# OpenAI API Key (use the same one from your Python .env file)
OPENAI_API_KEY=your_openai_api_key_here

# Python Backend URL (default for local development)
PYTHON_BACKEND_URL=http://localhost:8000
```

### 2. Install Dependencies

```bash
# In the mortgage-ai-ui directory
cd mortgage-ai-ui
npm install
```

### 3. Install Python Backend Dependencies

```bash
# In the main docling directory
pip install fastapi uvicorn
```

## Running the Application

### Step 1: Start the Python Backend

In the main docling directory:

```bash
python python_backend.py
```

This will start the FastAPI server on `http://localhost:8000`

### Step 2: Start the Next.js Frontend

In a new terminal, in the `mortgage-ai-ui` directory:

```bash
npm run dev
```

This will start the Next.js development server on `http://localhost:3000`

### Step 3: Access the Application

Open your browser and go to `http://localhost:3000`

## How It Works

### Frontend (Next.js)
- **Main Page** (`src/app/page.tsx`) - Main chat interface
- **Components**:
  - `ChatMessage.tsx` - Individual chat message display
  - `Sidebar.tsx` - Search options and controls
- **API Routes**:
  - `/api/chat` - Handles chat requests and OpenAI integration
  - `/api/search` - Proxies search requests to Python backend
  - `/api/lenders` - Serves lender configuration

### Backend (Python)
- **FastAPI Service** - Handles LanceDB vector search operations
- **Endpoints**:
  - `POST /search` - Vector similarity search across lender criteria
  - `GET /health` - Health check and status
  - `GET /` - API information

### Data Flow

1. User asks a question in the chat interface
2. Frontend sends request to `/api/chat`
3. Chat API calls Python backend `/search` endpoint
4. Python backend performs vector search on LanceDB
5. Search results are returned to chat API
6. OpenAI generates response based on search context
7. Response and search results displayed to user

## Key Differences from Streamlit Version

- ✅ **Better Performance** - No page reloads, smooth interactions
- ✅ **Modern UI** - Professional design with Tailwind CSS
- ✅ **Better Mobile Support** - Responsive design
- ✅ **Real-time Updates** - Instant search results and chat updates
- ✅ **Better Error Handling** - Graceful error messages and retry logic
- ✅ **Production Ready** - Can be easily deployed to Vercel, Netlify, etc.

## API Documentation

When the Python backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Troubleshooting

### Backend Connection Issues

1. Ensure the Python backend is running on port 8000
2. Check that your `.env.local` file has the correct `PYTHON_BACKEND_URL`
3. Verify LanceDB database exists at `data/lancedb/lender_criteria.lance`

### Missing Lender Data

1. Ensure you've run the data preparation scripts:
   ```bash
   python 1-extraction.py
   python 2-chunking.py
   python 3-embedding.py
   ```

### OpenAI API Issues

1. Check your OpenAI API key is valid in both `.env` (Python) and `.env.local` (Next.js)
2. Ensure you have sufficient OpenAI API credits

## Development

### Adding New Features

- **Frontend changes**: Edit files in `src/app/`
- **API changes**: Edit files in `src/app/api/`
- **Backend changes**: Edit `python_backend.py`

### Styling

The application uses Tailwind CSS for styling. The design matches the professional look of the original Streamlit application.

## Deployment

### Frontend Deployment

Deploy to Vercel (recommended):
```bash
npm run build
vercel deploy
```

### Backend Deployment

The Python backend can be deployed to:
- Railway
- Render
- Heroku
- Digital Ocean App Platform

Update the `PYTHON_BACKEND_URL` environment variable to point to your deployed backend.

## Support

For issues or questions, check that:
1. All dependencies are installed correctly
2. Environment variables are set properly
3. Database files exist and are accessible
4. Both services are running simultaneously

This Next.js version provides the exact same functionality as the Streamlit application but with a modern, production-ready interface.
