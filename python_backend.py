#!/usr/bin/env python3
"""
Python backend service for the Next.js mortgage criteria chat application.
This service handles LanceDB operations and search functionality.
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

app = FastAPI(title="Mortgage Criteria Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
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

def search_lender_criteria(query: str, num_results: int = 15, lender_filter: str = None):
    """Search lender criteria with comprehensive results - exact replica of Python code."""
    try:
        if not table:
            print("🔄 Database not available, trying to reconnect...")
            if not init_database():
                raise Exception("Database not available and reconnection failed")
            
        # Create embedding for the query
        response = client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = response.data[0].embedding
        
        if lender_filter:
            # Filter by specific lender
            result = table.search(query_embedding, vector_column_name='embedding').where(f"metadata.lender_name = '{lender_filter}'").limit(num_results)
        else:
            # Search across all lenders with higher limit for better coverage
            result = table.search(query_embedding, vector_column_name='embedding').limit(num_results)
        
        # Convert to pandas and sort by relevance score
        df = result.to_pandas()
        if not df.empty and 'score' in df.columns:
            df = df.sort_values('score', ascending=False)
        
        return df
    except Exception as e:
        print(f"Search error: {str(e)}")
        return pd.DataFrame()

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Mortgage Criteria Backend API",
        "status": "running",
        "database_connected": table is not None
    }

@app.post("/search", response_model=List[SearchResult])
async def search_criteria(request: SearchRequest):
    """Search mortgage criteria endpoint."""
    try:
        results_df = search_lender_criteria(
            query=request.query,
            num_results=request.num_results,
            lender_filter=request.lender_filter
        )
        
        if results_df.empty:
            return []
        
        # Convert DataFrame to SearchResult objects
        search_results = []
        for _, row in results_df.iterrows():
            search_result = SearchResult(
                text=row['text'],
                metadata=row['metadata'],
                score=row.get('score', None)
            )
            search_results.append(search_result)
        
        return search_results
        
    except Exception as e:
        print(f"Search endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database_available": table is not None,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

if __name__ == "__main__":
    print("🚀 Starting Mortgage Criteria Backend...")
    print("📊 Database connection:", "✅ Connected" if table else "❌ Failed")
    print("🔑 OpenAI API:", "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Missing")
    print("🌐 Server starting on http://localhost:8000")
    
    uvicorn.run(
        "python_backend:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
