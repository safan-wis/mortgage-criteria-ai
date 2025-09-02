#!/bin/bash

echo "⚛️  Starting Next.js Frontend Service..."
echo "========================================"

# Check if mortgage-ai-ui directory exists
if [ ! -d "mortgage-ai-ui" ]; then
    echo "❌ mortgage-ai-ui directory not found!"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

# Navigate to frontend directory
cd mortgage-ai-ui

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found!"
    echo "Creating .env.local with default values..."
    
    # Try to copy from parent .env
    if [ -f "../.env" ]; then
        echo "OPENAI_API_KEY=$(grep OPENAI_API_KEY ../.env | cut -d '=' -f2)" > .env.local
        echo "PYTHON_BACKEND_URL=http://localhost:8000" >> .env.local
        echo "✅ Created .env.local from parent .env"
    else
        echo "OPENAI_API_KEY=your_openai_api_key_here" > .env.local
        echo "PYTHON_BACKEND_URL=http://localhost:8000" >> .env.local
        echo "⚠️  Created .env.local with placeholder values"
        echo "Please update OPENAI_API_KEY in .env.local"
    fi
fi

echo "🚀 Starting Next.js development server..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the frontend"
echo ""

npm run dev
