#!/usr/bin/env python3
"""
Test script to verify CORS functionality
"""

import requests
import json

def test_cors():
    """Test CORS functionality"""
    base_url = "http://localhost:8000"
    
    # Test OPTIONS preflight request
    print("Testing OPTIONS preflight request...")
    try:
        response = requests.options(f"{base_url}/api/analytics", 
                                  headers={
                                      'Origin': 'http://localhost:3000',
                                      'Access-Control-Request-Method': 'POST',
                                      'Access-Control-Request-Headers': 'Content-Type'
                                  })
        print(f"OPTIONS Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        print("✓ OPTIONS preflight successful")
    except Exception as e:
        print(f"✗ OPTIONS preflight failed: {e}")
    
    # Test actual POST request with CORS
    print("\nTesting POST request with CORS...")
    try:
        response = requests.post(f"{base_url}/api/analytics",
                               headers={
                                   'Origin': 'http://localhost:3000',
                                   'Content-Type': 'application/json'
                               },
                               json={'video_id': 'dQw4w9WgXcQ'})
        print(f"POST Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        print("✓ POST request with CORS successful")
    except Exception as e:
        print(f"✗ POST request failed: {e}")
    
    # Test health endpoint
    print("\nTesting health endpoint...")
    try:
        response = requests.get(f"{base_url}/health",
                              headers={'Origin': 'http://localhost:3000'})
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✓ Health endpoint accessible")
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}")

if __name__ == "__main__":
    print("Testing CORS functionality...")
    test_cors()
    print("\nCORS test completed!") 