#!/bin/bash

echo "🚀 Starting Python Backend Service..."
echo "====================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your OpenAI API key"
    exit 1
fi

# Activate virtual environment and start backend
echo "🐍 Activating virtual environment..."
source .venv/bin/activate

echo "📦 Checking dependencies..."
pip install fastapi uvicorn > /dev/null 2>&1

echo "🚀 Starting FastAPI backend..."
echo "📍 Backend will be available at: http://localhost:8000"
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the backend"
echo ""

python python_backend.py
