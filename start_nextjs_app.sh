#!/bin/bash

# 🏦 Mortgage Criteria AI - Next.js Version Startup Script
# This script starts both the Python backend and Next.js frontend

echo "🚀 Starting Mortgage Criteria AI - Next.js Version"
echo "=================================================="

# Check if required files exist
if [ ! -f "data/lancedb/lender_criteria.lance/_latest.manifest" ]; then
    echo "❌ Error: LanceDB database not found!"
    echo "Please run the data preparation scripts first:"
    echo "  python 1-extraction.py"
    echo "  python 2-chunking.py" 
    echo "  python 3-embedding.py"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your OpenAI API key"
    exit 1
fi

if [ ! -f "mortgage-ai-ui/.env.local" ]; then
    echo "⚠️  Warning: .env.local not found in mortgage-ai-ui/"
    echo "Creating .env.local with default values..."
    echo "OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)" > mortgage-ai-ui/.env.local
    echo "PYTHON_BACKEND_URL=http://localhost:8000" >> mortgage-ai-ui/.env.local
    echo "✅ Created mortgage-ai-ui/.env.local"
fi

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo "🐍 Starting Python Backend (FastAPI)..."
python python_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Failed to start Python backend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Python backend started on http://localhost:8000"

echo "⚛️  Starting Next.js Frontend..."
cd mortgage-ai-ui

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Both services are starting up!"
echo "=================================="
echo "🐍 Python Backend: http://localhost:8000"
echo "⚛️  Next.js Frontend: http://localhost:3000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Open your browser and go to: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
