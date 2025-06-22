#!/usr/bin/env python3
"""
Test script for the enhanced YouTube comment analyzer integration
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_extract_video_id():
    """Test video ID extraction"""
    print("\nTesting video ID extraction...")
    try:
        response = requests.post(f"{BASE_URL}/api/extract-video-id", 
                               json={"video_url": TEST_VIDEO_URL})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_enhanced_analyze():
    """Test the enhanced video analysis"""
    print("\nTesting enhanced video analysis...")
    try:
        response = requests.post(f"{BASE_URL}/api/analyze", 
                               json={"video_url": TEST_VIDEO_URL})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis successful!")
            print(f"Video Title: {data.get('video_info', {}).get('title', 'N/A')}")
            print(f"Channel: {data.get('video_info', {}).get('channel', 'N/A')}")
            print(f"Total Comments: {data.get('analysis', {}).get('total_comments', 'N/A')}")
            print(f"English Comments: {data.get('analysis', {}).get('english_comments', 'N/A')}")
            
            # Check for enhanced features
            if 'tagged_insights' in data:
                print(f"✅ Tagged Insights: {len(data['tagged_insights'])} insights generated")
                for insight in data['tagged_insights'][:2]:  # Show first 2
                    print(f"  - {insight.get('tag', 'N/A')}: {insight.get('description', 'N/A')[:100]}...")
            
            if 'additional_metrics' in data:
                print("✅ Additional Metrics:")
                metrics = data['additional_metrics']
                print(f"  - Engagement Rate: {metrics.get('engagement_rate', 'N/A'):.2f}%")
                print(f"  - Sentiment Score: {metrics.get('sentiment_score', 'N/A'):.1f}")
                print(f"  - Community Health: {metrics.get('community_health', {}).get('status', 'N/A')}")
            
            if 'recommendations' in data:
                print(f"✅ Priority Recommendations: {len(data['recommendations'])} generated")
            
            if 'benchmark_comparison' in data:
                print("✅ Benchmark Comparison available")
                
        else:
            print(f"❌ Analysis failed: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_routes_listing():
    """Test the routes listing endpoint"""
    print("\nTesting routes listing...")
    try:
        response = requests.get(f"{BASE_URL}/routes")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Routes listing available")
            print("Available endpoints:")
            routes = response.text.split('<br>')
            for route in routes[:10]:  # Show first 10 routes
                print(f"  {route}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Enhanced YouTube Comment Analyzer Integration")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Video ID Extraction", test_extract_video_id),
        ("Enhanced Analysis", test_enhanced_analyze),
        ("Routes Listing", test_routes_listing)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Enhanced analyzer integration successful.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main() 