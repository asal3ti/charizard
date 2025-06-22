#!/usr/bin/env python3
"""
Test script for Simple YouTube Analytics API
"""

import requests
import json

BASE_URL = "http://localhost:8000"
TEST_VIDEO = "dQw4w9WgXcQ"

def test_analyze():
    """Test video analysis"""
    print("🎬 Testing Video Analysis...")
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={"video_id": TEST_VIDEO}
    )
    
    if response.status_code == 200:
        data = response.json()
        stats = data.get("video_stats", {})
        print(f"✅ Title: {stats.get('title', 'N/A')}")
        print(f"✅ Views: {stats.get('views', 0):,}")
        print(f"✅ Likes: {stats.get('likes', 0):,}")
        print(f"✅ Sentiment: {data.get('sentiment', 'N/A')}")
        print(f"✅ Comments analyzed: {data.get('comments_analyzed', 0)}")
    else:
        print(f"❌ Error: {response.text}")

def test_history():
    """Test history endpoint"""
    print("\n📚 Testing History...")
    
    response = requests.get(f"{BASE_URL}/history")
    
    if response.status_code == 200:
        data = response.json()
        history = data.get("history", [])
        print(f"✅ Found {len(history)} recent analyses")
        
        for item in history[:3]:  # Show first 3
            print(f"   📺 {item.get('title', 'N/A')} - {item.get('sentiment', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing Health...")
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data.get('status', 'N/A')}")
        print(f"✅ Model: {data.get('model', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    print("🧪 Simple YouTube Analytics API Test")
    print("=" * 50)
    
    test_health()
    test_analyze()
    test_history()
    
    print("\n🎉 Test completed!") 