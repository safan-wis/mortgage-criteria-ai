#!/usr/bin/env python3
"""
Test the Python backend connection
"""

import requests
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing backend connection...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: Search endpoint
    try:
        search_data = {
            "query": "maximum age for mortgage applications",
            "num_results": 5
        }
        response = requests.post(f"{base_url}/search", json=search_data, timeout=10)
        print(f"✅ Search test: {response.status_code}")
        results = response.json()
        print(f"Results count: {len(results)}")
        if results:
            print(f"First result: {results[0]['text'][:100]}...")
    except Exception as e:
        print(f"❌ Search test failed: {e}")

if __name__ == "__main__":
    test_backend()
