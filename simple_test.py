#!/usr/bin/env python3
"""
Simple test script for the YouTube Analytics API
"""

import requests
import json

BASE_URL = "http://localhost:8000"
TEST_VIDEO = "dQw4w9WgXcQ"  # Rick Roll for testing

def test_video_analytics():
    """Test video analytics endpoint"""
    print("📺 Testing Video Analytics...")
    
    response = requests.post(
        f"{BASE_URL}/api/analytics",
        json={"video_id": TEST_VIDEO}
    )
    
    if response.status_code == 200:
        data = response.json()
        video = data.get("video_analytics", {})
        print(f"✅ Title: {video.get('title', 'N/A')}")
        print(f"✅ Views: {video.get('view_count', 0):,}")
        print(f"✅ Likes: {video.get('like_count', 0):,}")
        print(f"✅ Comments: {video.get('comment_count', 0):,}")
    else:
        print(f"❌ Error: {response.text}")

def test_comment_analytics():
    """Test comment analytics endpoint"""
    print("\n💬 Testing Comment Analytics...")
    
    response = requests.post(
        f"{BASE_URL}/api/comments",
        json={"video_id": TEST_VIDEO}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total Comments: {data.get('total_comments', 0)}")
        sentiment = data.get('sentiment_breakdown', {})
        print(f"✅ Positive: {sentiment.get('positive', 0)}")
        print(f"✅ Negative: {sentiment.get('negative', 0)}")
        print(f"✅ Neutral: {sentiment.get('neutral', 0)}")
        
        # Show first comment
        comments = data.get('comments', [])
        if comments:
            print(f"✅ Sample Comment: {comments[0].get('text', 'N/A')}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    print("🧪 Simple YouTube Analytics Test")
    print("=" * 40)
    
    test_video_analytics()
    test_comment_analytics()
    
    print("\n🎉 Test completed!") 