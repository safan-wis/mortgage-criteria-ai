import lancedb
import json
from pathlib import Path

# --------------------------------------------------------------
# Connect to the lender criteria database
# --------------------------------------------------------------

def connect_to_lender_database():
    """Connect to the lender criteria database."""
    uri = "data/lancedb"
    db = lancedb.connect(uri)
    
    try:
        table = db.open_table("lender_criteria")
        print("✅ Connected to lender criteria database")
        return table
    except Exception as e:
        print(f"❌ Error connecting to database: {str(e)}")
        return None

# --------------------------------------------------------------
# Search the lender criteria database
# --------------------------------------------------------------

def search_lender_criteria(table, query, num_results=5, lender_filter=None):
    """Search lender criteria with optional lender filtering."""
    print(f"🔍 Searching for: '{query}'")
    
    if lender_filter:
        print(f"🎯 Filtering by lender: {lender_filter}")
    
    try:
        # Perform vector search
        if lender_filter:
            # Filter by specific lender
            result = table.search(query).where(f"metadata.lender_name = '{lender_filter}'").limit(num_results)
        else:
            # Search across all lenders
            result = table.search(query).limit(num_results)
        
        # Convert to pandas for easier handling
        df = result.to_pandas()
        
        if df.empty:
            print("❌ No results found")
            return []
        
        print(f"✅ Found {len(df)} relevant results")
        return df
        
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return []

# --------------------------------------------------------------
# Display search results with lender attribution
# --------------------------------------------------------------

def display_search_results(results_df):
    """Display search results with clear lender attribution."""
    if results_df.empty:
        return
    
    print("\n" + "="*80)
    print("🔍 SEARCH RESULTS")
    print("="*80)
    
    for i, (_, row) in enumerate(results_df.iterrows(), 1):
        metadata = row['metadata']
        lender_name = metadata['lender_name']
        criteria_section = metadata['criteria_section'] or 'General Criteria'
        filename = metadata['filename']
        source_type = metadata['source_type'].upper()
        
        print(f"\n📋 Result {i}:")
        print(f"🏦 Lender: {lender_name}")
        print(f"📚 Section: {criteria_section}")
        print(f"📄 Source: {filename} ({source_type})")
        
        # Display text content (truncated for readability)
        text_content = row['text']
        if len(text_content) > 300:
            text_content = text_content[:300] + "..."
        
        print(f"📝 Content: {text_content}")
        print("-" * 60)

# --------------------------------------------------------------
# Interactive search interface
# --------------------------------------------------------------

def interactive_search(table):
    """Provide interactive search interface for testing."""
    print("\n🎯 Interactive Lender Criteria Search")
    print("="*50)
    print("Commands:")
    print("  - Type your search query")
    print("  - Use 'lender:NAME' to filter by specific lender")
    print("  - Type 'quit' to exit")
    print("  - Type 'stats' to see database statistics")
    print("="*50)
    
    while True:
        try:
            query = input("\n🔍 Enter search query: ").strip()
            
            if query.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif query.lower() == 'stats':
                show_database_stats(table)
                continue
            elif not query:
                continue
            
            # Check for lender filter
            lender_filter = None
            if query.lower().startswith('lender:'):
                parts = query.split(':', 1)
                if len(parts) == 2:
                    lender_filter = parts[1].strip()
                    query = "mortgage criteria"  # Default query when filtering by lender
            
            # Perform search
            results = search_lender_criteria(table, query, num_results=5, lender_filter=lender_filter)
            
            # Display results
            display_search_results(results)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def show_database_stats(table):
    """Show database statistics."""
    try:
        total_chunks = table.count_rows()
        print(f"\n📊 Database Statistics:")
        print(f"   Total chunks: {total_chunks}")
        
        # Get unique lenders
        df = table.to_pandas()
        if not df.empty:
            lenders = df['metadata'].apply(lambda x: x['lender_name']).unique()
            print(f"   Unique lenders: {len(lenders)}")
            print(f"   Lenders: {', '.join(sorted(lenders))}")
        
    except Exception as e:
        print(f"❌ Error getting stats: {str(e)}")

# --------------------------------------------------------------
# Main execution
# --------------------------------------------------------------

if __name__ == "__main__":
    # Connect to database
    table = connect_to_lender_database()
    
    if table:
        # Show database info
        show_database_stats(table)
        
        # Example searches
        print("\n🧪 Example searches:")
        
        # Search 1: General criteria
        print("\n1️⃣ Searching for 'maximum age mortgage applications'...")
        results1 = search_lender_criteria(table, "maximum age mortgage applications", num_results=3)
        display_search_results(results1)
        
        # Search 2: Specific lender
        print("\n2️⃣ Searching Barclays criteria for 'LTV limits'...")
        results2 = search_lender_criteria(table, "LTV limits", num_results=3, lender_filter="Barclays")
        display_search_results(results2)
        
        # Interactive mode
        print("\n🎯 Starting interactive search mode...")
        interactive_search(table)
    else:
        print("❌ Cannot proceed without database connection")
        print("💡 Please run 3-embedding.py first to create the database")
