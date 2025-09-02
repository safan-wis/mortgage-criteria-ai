#!/usr/bin/env python3
"""
Simple FastAPI backend for testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Simple Test Backend", version="1.0.0")

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
    return {"message": "Simple backend is working!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Simple backend is running"
    }

@app.post("/search")
async def test_search():
    return {
        "message": "Search endpoint is working",
        "results": []
    }

if __name__ == "__main__":
    print("🚀 Starting Simple Test Backend...")
    uvicorn.run(
        "simple_backend:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
