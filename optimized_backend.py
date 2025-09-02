#!/usr/bin/env python3
"""
Optimized FastAPI backend with persistent connections like Streamlit
"""

import os
import json
import lancedb
import pandas as pd
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Mortgage Criteria AI Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for persistent connections (like Streamlit caching)
db = None
table = None
openai_client = None

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    query: str
    lender_filter: Optional[str] = None
    num_results: int = 15

class ChatResponse(BaseModel):
    response: str
    search_results: List[Dict]

def init_connections():
    """Initialize persistent connections (like Streamlit @st.cache_resource)"""
    global db, table, openai_client
    
    try:
        # Initialize database connection once
        if db is None:
            print("🔍 Initializing database connection...")
            db = lancedb.connect("data/lancedb/lender_criteria.lance")
            table = db.open_table("lender_criteria")
            print("✅ Database connection established")
        
        # Initialize OpenAI client once
        if openai_client is None:
            print("🔑 Initializing OpenAI client...")
            openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            print("✅ OpenAI client initialized")
            
    except Exception as e:
        print(f"❌ Connection initialization error: {str(e)}")
        raise e

def search_lender_criteria(query: str, num_results: int = 15, lender_filter: str = None):
    """Search lender criteria - optimized version with persistent connection."""
    global table, openai_client
    
    try:
        # Create embedding for the query
        response = openai_client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = response.data[0].embedding
        
        if lender_filter:
            # Filter by specific lender
            result = table.search(query_embedding, vector_column_name='embedding').where(f"metadata.lender_name = '{lender_filter}'").limit(num_results)
        else:
            # Search across all lenders
            result = table.search(query_embedding, vector_column_name='embedding').limit(num_results)
        
        # Convert to pandas and sort by relevance score
        df = result.to_pandas()
        if not df.empty and 'score' in df.columns:
            df = df.sort_values('score', ascending=False)
        
        return df
    except Exception as e:
        print(f"Search error: {str(e)}")
        return pd.DataFrame()

def get_context_from_results(results_df: pd.DataFrame) -> str:
    """Extract context from search results - exact same as Streamlit version."""
    if results_df.empty:
        return "No relevant criteria found."
    
    context_parts = []
    
    for _, row in results_df.iterrows():
        metadata = row['metadata']
        lender_name = metadata['lender_name']
        criteria_section = metadata['criteria_section'] or 'General Criteria'
        text_content = row['text']
        
        # Clean up the lender name (same logic as Streamlit)
        clean_lender_name = lender_name.replace('_residential.txt', '').replace('_residential.pdf', '')
        clean_lender_name = clean_lender_name.replace('_res', '').replace('_bank', '').replace('_building_society', '')
        clean_lender_name = clean_lender_name.replace('_mortgage', '').replace('_criteria', '')
        clean_lender_name = clean_lender_name.replace('_', ' ').title()
        
        # Additional cleaning for common patterns
        clean_lender_name = clean_lender_name.replace('Residential', '').replace('Res', '').strip()
        if clean_lender_name.endswith('.'):
            clean_lender_name = clean_lender_name[:-1]
        
        # Final cleanup - remove extra spaces and normalize
        clean_lender_name = ' '.join(clean_lender_name.split())
        
        # Handle specific cases
        if clean_lender_name == 'Hsbcidential 1.Txt':
            clean_lender_name = 'HSBC'
        elif clean_lender_name == 'Skipton':
            clean_lender_name = 'Skipton Building Society'
        elif clean_lender_name == 'Halifaxidentialing Services':
            clean_lender_name = 'Halifax'
        elif clean_lender_name == 'Santanderidential 1.Txt':
            clean_lender_name = 'Santander'
        
        # Format the context cleanly
        context_part = f"""
LENDER: {clean_lender_name}
SECTION: {criteria_section}
CRITERIA: {text_content}
---
"""
        context_parts.append(context_part)
    
    return "\n".join(context_parts)

def get_chat_response(messages: list, context: str, query: str) -> str:
    """Get AI response - exact same as Streamlit version."""
    global openai_client
    
    system_prompt = f"""You are an expert mortgage advisor AI assistant with access to comprehensive UK mortgage lender criteria from 30+ major lenders.

Your role is to provide 100% accurate answers based ONLY on the provided lender criteria. You must:

1. **ALWAYS cite the specific lender name** when providing information
2. **Use ONLY the provided criteria** - never make assumptions
3. **Be precise and accurate** with all numbers, percentages, and requirements
4. **Group responses by lender** for clarity
5. **Provide complete, readable information** - don't truncate mid-sentence
6. **If criteria differs between lenders, clearly show the differences**

Current query: {query}

Available criteria context:
{context}

IMPORTANT INSTRUCTIONS:
- Only use the information provided in the context
- If the context doesn't contain the specific information requested, say so clearly
- Never guess or provide generic mortgage advice
- Format your response professionally with clear lender attribution
- Group information by lender for easy reading
- Provide complete sentences and complete information
- Do NOT include file names, source paths, or technical metadata in your response
- Focus on the actual mortgage criteria content

Format your response like this:
🏦 [Lender Name]
[Complete, readable criteria information]

🏦 [Next Lender Name]
[Complete, readable criteria information]

And so on..."""

    messages_with_context = [
        {"role": "system", "content": system_prompt},
        *messages
    ]

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_context,
            temperature=0.1,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    print("🚀 Starting Optimized Backend...")
    init_connections()
    print("✅ Backend ready!")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Optimized backend is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint with optimized performance."""
    try:
        # Search for relevant criteria
        results = search_lender_criteria(request.query, request.num_results, request.lender_filter)
        
        if not results.empty:
            # Get context from results
            context = get_context_from_results(results)
            
            # Generate AI response
            response = get_chat_response(request.messages, context, request.query)
            
            # Return response
            return ChatResponse(
                response=response,
                search_results=[
                    {
                        "text": row['text'],
                        "metadata": row['metadata'],
                        "score": row.get('score', None)
                    }
                    for _, row in results.iterrows()
                ]
            )
        else:
            return ChatResponse(
                response="No relevant criteria found. Try rephrasing your question or check if the criteria exists.",
                search_results=[]
            )
            
    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lenders")
async def get_lenders():
    """Get available lenders."""
    try:
        with open("residential/lender_config.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lenders endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Optimized Mortgage Criteria AI Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
