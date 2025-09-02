#!/usr/bin/env python3
"""
Simple search script that works like Streamlit
"""

import sys
import json
import lancedb
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def search_lender_criteria(query: str, num_results: int = 15, lender_filter: str = None):
    """Search lender criteria - exact same as Streamlit version."""
    try:
        # Initialize database connection
        db = lancedb.connect("data/lancedb/lender_criteria.lance")
        table = db.open_table("lender_criteria")
        
        # Create embedding for the query
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
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
        print(f"Search error: {str(e)}", file=sys.stderr)
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
        
        # Clean up the lender name (same logic as Python)
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
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_context,
            temperature=0.1,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_search.py <query> [lender_filter] [num_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    lender_filter = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "None" else None
    num_results = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    
    # Search for relevant criteria
    results = search_lender_criteria(query, num_results, lender_filter)
    
    if not results.empty:
        # Get context from results
        context = get_context_from_results(results)
        
        # Generate AI response
        messages = [{"role": "user", "content": query}]
        response = get_chat_response(messages, context, query)
        
        # Return JSON response
        result = {
            "response": response,
            "search_results": [
                {
                    "text": row['text'],
                    "metadata": row['metadata'],
                    "score": row.get('score', None)
                }
                for _, row in results.iterrows()
            ]
        }
        
        print(json.dumps(result))
    else:
        result = {
            "response": "No relevant criteria found. Try rephrasing your question or check if the criteria exists.",
            "search_results": []
        }
        print(json.dumps(result))
