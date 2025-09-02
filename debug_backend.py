#!/usr/bin/env python3
"""
Debug version of the backend to identify the exact issue
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import lancedb
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="Debug Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    lender_filter: Optional[str] = None
    num_results: int = 15

class SearchResult(BaseModel):
    text: str
    metadata: Dict
    score: Optional[float] = None

# Initialize database connection
table = None
def init_database():
    global table
    try:
        print("🔍 Connecting to database...")
        db = lancedb.connect("data/lancedb/lender_criteria.lance")
        table = db.open_table("lender_criteria")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        table = None
        return False

# Try to initialize database
init_database()

@app.get("/")
async def root():
    return {
        "message": "Debug Backend API",
        "status": "running",
        "database_connected": table is not None
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_available": table is not None,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.post("/search", response_model=List[SearchResult])
async def search_criteria(request: SearchRequest):
    """Search mortgage criteria endpoint with debugging."""
    try:
        print(f"🔍 Search request: {request.query}")
        
        if not table:
            print("🔄 Database not available, trying to reconnect...")
            if not init_database():
                raise Exception("Database not available and reconnection failed")
        
        print("🔍 Creating embedding...")
        # Create embedding for the query
        response = client.embeddings.create(
            input=request.query,
            model="text-embedding-ada-002"
        )
        query_embedding = response.data[0].embedding
        print(f"✅ Embedding created, length: {len(query_embedding)}")
        
        print("🔍 Searching database...")
        if request.lender_filter:
            # Filter by specific lender
            result = table.search(query_embedding, vector_column_name='embedding').where(f"metadata.lender_name = '{request.lender_filter}'").limit(request.num_results)
        else:
            # Search across all lenders
            result = table.search(query_embedding, vector_column_name='embedding').limit(request.num_results)
        
        print("🔍 Converting to pandas...")
        # Convert to pandas and sort by relevance score
        df = result.to_pandas()
        print(f"✅ Query successful, got {len(df)} results")
        
        if not df.empty and 'score' in df.columns:
            df = df.sort_values('score', ascending=False)
        
        if df.empty:
            print("⚠️ No results found")
            return []
        
        # Convert DataFrame to SearchResult objects
        search_results = []
        for _, row in df.iterrows():
            search_result = SearchResult(
                text=row['text'],
                metadata=row['metadata'],
                score=row.get('score', None)
            )
            search_results.append(search_result)
        
        print(f"✅ Returning {len(search_results)} results")
        return search_results
        
    except Exception as e:
        print(f"❌ Search endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Debug Backend...")
    print("📊 Database connection:", "✅ Connected" if table else "❌ Failed")
    print("🔑 OpenAI API:", "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing")
    print("🌐 Server starting on http://localhost:8000")
    
    uvicorn.run(
        "debug_backend:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
