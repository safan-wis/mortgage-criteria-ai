import streamlit as st
import lancedb
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from typing import List, Dict
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Page configuration
st.set_page_config(
    page_title="🏦 All-in-One Mortgage Criteria AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .lender-badge {
        background-color: #e8f4fd;
        border: 1px solid #2980b9;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        display: inline-block;
        font-weight: 600;
        color: #1f4e79;
    }
    .criteria-section {
        background-color: #f8f9fa;
        border-left: 4px solid #2980b9;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .source-info {
        background-color: #e8f5e8;
        border: 1px solid #28a745;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9em;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database connection
@st.cache_resource
def init_db():
    """Initialize database connection."""
    try:
        db = lancedb.connect("data/lancedb/lender_criteria.lance")
        table = db.open_table("lender_criteria")
        return table
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

# Load lender configuration
@st.cache_data
def load_lender_config():
    """Load lender configuration."""
    try:
        with open("residential/lender_config.json", "r") as f:
            return json.load(f)
    except:
        return None

# Search functions
def search_lender_criteria(table, query: str, num_results: int = 15, lender_filter: str = None):
    """Search lender criteria with comprehensive results."""
    try:
        # Create embedding for the query
        from openai import OpenAI
        import os
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
            # Search across all lenders with higher limit for better coverage
            result = table.search(query_embedding, vector_column_name='embedding').limit(num_results)
        
        # Convert to pandas and sort by relevance score
        df = result.to_pandas()
        if not df.empty and 'score' in df.columns:
            df = df.sort_values('score', ascending=False)
        
        return df
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return pd.DataFrame()

def get_context_from_results(results_df: pd.DataFrame) -> str:
    """Extract context from search results with clean formatting."""
    if results_df.empty:
        return "No relevant criteria found."
    
    context_parts = []
    
    for _, row in results_df.iterrows():
        metadata = row['metadata']
        lender_name = metadata['lender_name']
        criteria_section = metadata['criteria_section'] or 'General Criteria'
        text_content = row['text']
        
        # Clean up the lender name (remove file extensions and formatting)
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

def get_chat_response(messages: List[Dict], context: str, query: str) -> str:
    """Get AI response with comprehensive mortgage criteria context."""
    
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
        # Create streaming response
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_context,
            temperature=0.1,  # Very low temperature for more accurate, consistent responses
            stream=True,
        )

        # Use Streamlit's streaming capability
        response = st.write_stream(stream)
        return response
        
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏦 All-in-One Mortgage Criteria AI</h1>
        <p>Comprehensive mortgage criteria search across 30+ UK lenders with 100% accuracy</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize database
    table = init_db()
    if not table:
        st.error("❌ Cannot connect to lender criteria database. Please ensure you've run the setup scripts.")
        st.info("💡 Run the scripts in order: 1-extraction.py → 2-chunking.py → 3-embedding.py")
        return
    
    # Load lender config
    lender_config = load_lender_config()
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Search Options")
        
        # Lender filter
        if lender_config:
            all_lenders = []
            for category, lenders in lender_config['lender_categories'].items():
                all_lenders.extend(lenders)
            
            # Extract clean lender names
            lender_names = []
            for filename in all_lenders:
                name = filename.replace('_residential.txt', '').replace('_residential.pdf', '')
                name = name.replace('_res', '').replace('_bank', '').replace('_building_society', '')
                name = name.replace('_mortgage', '').replace('_criteria', '')
                name = name.replace('_', ' ').title()
                lender_names.append(name)
            
            lender_names = sorted(list(set(lender_names)))
            selected_lender = st.selectbox(
                "🎯 Filter by Lender (Optional)",
                ["All Lenders"] + lender_names
            )
        else:
            selected_lender = "All Lenders"
        
        # Number of results
        num_results = st.slider("📊 Number of Results", 5, 20, 15)
        
        # Database stats
        st.header("📊 Database Info")
        try:
            total_chunks = table.count_rows()
            st.metric("Total Criteria Chunks", total_chunks)
            
            if lender_config:
                st.metric("Total Lenders", len(lender_config['lender_categories']['major_banks']) + 
                         len(lender_config['lender_categories']['building_societies']) + 
                         len(lender_config['lender_categories']['specialist_lenders']) + 
                         len(lender_config['lender_categories']['other_banks']))
        except:
            st.info("Database statistics unavailable")
        
        # Quick search examples
        st.header("💡 Quick Search Examples")
        example_queries = [
            "maximum age for mortgage applications",
            "LTV limits for first time buyers",
            "income requirements for self employed",
            "minimum deposit requirements",
            "foreign national mortgage criteria",
            "buy to let mortgage rules"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{query}"):
                st.session_state.user_query = query
                st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask About Mortgage Criteria")
        
        # Chat input
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Ask about mortgage criteria (e.g., 'What's the maximum age for mortgage applications?')"):
            # Display user message
            with st.chat_message("user"):
                st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Search for relevant criteria
            with st.status("🔍 Searching lender criteria...", expanded=False) as status:
                lender_filter = None if selected_lender == "All Lenders" else selected_lender
                results = search_lender_criteria(table, prompt, num_results, lender_filter)
                
                if not results.empty:
                    status.update(label="📚 Found relevant criteria, generating response...", state="running")
                    
                    # Get context from results
                    context = get_context_from_results(results)
                    
                    # Generate AI response
                    with st.chat_message("assistant"):
                        response = get_chat_response(st.session_state.messages, context, prompt)
                        st.markdown(f'<div class="chat-message assistant-message">{response}</div>', unsafe_allow_html=True)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    status.update(label="✅ Response generated!", state="complete")
                else:
                    st.warning("❌ No relevant criteria found. Try rephrasing your question or check if the criteria exists.")
                    status.update(label="❌ No results found", state="error")
    
    with col2:
        st.header("🔍 Search Results")
        
        if 'last_search_results' in st.session_state and not st.session_state.last_search_results.empty:
            results_df = st.session_state.last_search_results
            
            for _, row in results_df.iterrows():
                metadata = row['metadata']
                lender_name = metadata['lender_name']
                criteria_section = metadata['criteria_section'] or 'General Criteria'
                
                with st.expander(f"🏦 {lender_name} - {criteria_section}"):
                    st.markdown(f"**Source:** {metadata['filename']}")
                    st.markdown(f"**Section:** {criteria_section}")
                    
                    # Display text content
                    text_content = row['text']
                    if len(text_content) > 200:
                        text_content = text_content[:200] + "..."
                    
                    st.markdown(f"**Content:** {text_content}")
                    
                    # Show metadata
                    with st.expander("📋 Metadata"):
                        st.json(metadata)
        else:
            st.info("💡 Search results will appear here after asking a question.")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
