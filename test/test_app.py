#!/usr/bin/env python3
"""
Simple test script for the app.py endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

def test_health():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_video_analytics():
    """Test video analytics endpoint"""
    print("\n📊 Testing Video Analytics Endpoint...")
    try:
        data = {
            "video_id": "dQw4w9WgXcQ"
        }
        response = requests.post(f"{BASE_URL}/api/analytics", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Video Analytics Response:")
            print(f"  Title: {result.get('video_analytics', {}).get('title', 'N/A')}")
            print(f"  Views: {result.get('video_analytics', {}).get('view_count', 0):,}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_comments():
    """Test comments endpoint"""
    print("\n💬 Testing Comments Endpoint...")
    try:
        data = {
            "video_id": "dQw4w9WgXcQ"
        }
        response = requests.post(f"{BASE_URL}/api/comments", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Comments Response:")
            print(f"  Total Comments: {result.get('total_comments', 0)}")
            print(f"  Sentiment Breakdown: {result.get('sentiment_breakdown', {})}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_channel_analytics():
    """Test channel analytics endpoint"""
    print("\n📺 Testing Channel Analytics Endpoint...")
    try:
        channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"  # MrBeast
        response = requests.get(f"{BASE_URL}/api/channel/{channel_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Channel Analytics Response:")
            if 'channel_info' in result:
                print(f"  Channel: {result['channel_info'].get('title', 'N/A')}")
            if 'statistics' in result:
                print(f"  Subscribers: {result['statistics'].get('subscriber_count', 0):,}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_channel_comparison():
    """Test channel comparison endpoint"""
    print("\n🔍 Testing Channel Comparison Endpoint...")
    try:
        data = {
            "channel_ids": [
                "UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast
                "UC-lHJZR3Gqxm24_Vd_AJ5Yw"   # PewDiePie
            ]
        }
        response = requests.post(f"{BASE_URL}/api/channel/compare", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Channel Comparison Response:")
            for channel_id, data in result.items():
                print(f"  {data.get('title', 'N/A')}: {data.get('subscribers', 0):,} subscribers")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print("\n📈 Testing Metrics Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/metrics")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Metrics Response:")
            print(f"  Total Videos: {result.get('total_videos', 0)}")
            print(f"  Total Comments: {result.get('total_comments', 0)}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_history():
    """Test history endpoint"""
    print("\n📚 Testing History Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/history")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ History Response:")
            print(f"  Total Analyses: {result.get('total_analyses', 0)}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing app.py Endpoints")
    print("=" * 50)
    
    # Test health first
    if not test_health():
        print("❌ API is not healthy. Please check if the server is running.")
        return
    
    # Run all tests
    tests = [
        test_video_analytics,
        test_comments,
        test_channel_analytics,
        test_channel_comparison,
        test_metrics,
        test_history
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 