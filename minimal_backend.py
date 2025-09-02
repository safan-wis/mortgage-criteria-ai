#!/usr/bin/env python3
"""
Minimal FastAPI backend to test basic functionality
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Minimal Test Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Minimal backend is working!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Minimal backend is running"
    }

@app.post("/search")
async def test_search():
    return {
        "message": "Search endpoint is working",
        "results": [
            {
                "text": "Test result",
                "metadata": {"lender_name": "test", "criteria_section": "test"},
                "score": 0.9
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Minimal Test Backend...")
    uvicorn.run(
        "minimal_backend:app",
        host="127.0.0.1",
        port=8001,  # Different port to avoid conflict
        reload=True,
        log_level="info"
    )
