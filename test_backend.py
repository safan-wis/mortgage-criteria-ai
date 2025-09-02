#!/usr/bin/env python3
"""
Simple test to check if the Python backend components work
"""

import os
from dotenv import load_dotenv
import lancedb

# Load environment variables
load_dotenv()

print("🔍 Testing backend components...")

# Test 1: Environment variables
print(f"✅ OpenAI API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Missing'}")

# Test 2: Database connection
try:
    print("🔍 Testing database connection...")
    db = lancedb.connect("data/lancedb/lender_criteria.lance")
    table = db.open_table("lender_criteria")
    print("✅ Database connection successful")
    
    # Test 3: Simple query
    print("🔍 Testing simple query...")
    result = table.search([0.1] * 1536, vector_column_name='embedding').limit(1)
    df = result.to_pandas()
    print(f"✅ Query successful, got {len(df)} results")
    
except Exception as e:
    print(f"❌ Database error: {str(e)}")

# Test 4: OpenAI connection
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("✅ OpenAI client created successfully")
except Exception as e:
    print(f"❌ OpenAI error: {str(e)}")

print("🏁 Test complete")
