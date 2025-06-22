#!/usr/bin/env python3
"""
Simple YouTube API Test Script
"""

import os
from googleapiclient.discovery import build

# Get API key from environment
API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")

def test_youtube_api():
    """Test basic YouTube API functionality"""
    print("🔍 Testing YouTube API Connectivity...")
    
    try:
        # Build YouTube service
        youtube = build("youtube", "v3", developerKey=API_KEY)
        print("✅ YouTube service built successfully")
        
        # Test video info retrieval
        test_videos = [
            "dQw4w9WgXcQ",  # Rick Roll
            "9bZkp7q19f0",  # PSY - GANGNAM STYLE
            "kJQP7kiw5Fk"   # Luis Fonsi - Despacito
        ]
        
        for video_id in test_videos:
            print(f"\n📹 Testing video: {video_id}")
            
            try:
                # Get video info
                request = youtube.videos().list(
                    part="snippet,statistics",
                    id=video_id
                )
                response = request.execute()
                
                if response['items']:
                    video = response['items'][0]
                    snippet = video['snippet']
                    statistics = video['statistics']
                    
                    print(f"  ✅ Title: {snippet['title']}")
                    print(f"  ✅ Channel: {snippet['channelTitle']}")
                    print(f"  ✅ Views: {statistics.get('viewCount', 'N/A')}")
                    print(f"  ✅ Likes: {statistics.get('likeCount', 'N/A')}")
                    print(f"  ✅ Comments: {statistics.get('commentCount', 'N/A')}")
                else:
                    print(f"  ❌ Video not found or not accessible")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
        
        # Test search functionality
        print(f"\n🔍 Testing search functionality...")
        try:
            search_request = youtube.search().list(
                part="id,snippet",
                q="tech review",
                type="video",
                maxResults=3
            )
            search_response = search_request.execute()
            
            print(f"  ✅ Search successful: {len(search_response['items'])} videos found")
            
            for i, item in enumerate(search_response['items'], 1):
                print(f"    {i}. {item['snippet']['title']}")
                
        except Exception as e:
            print(f"  ❌ Search error: {str(e)}")
            
    except Exception as e:
        print(f"❌ YouTube API error: {str(e)}")
        return False
    
    return True

def test_api_quota():
    """Test API quota usage"""
    print(f"\n📊 API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print("💡 Check your quota usage at: https://console.cloud.google.com/apis/credentials")
    print("💡 Each video analysis uses ~100-200 quota units")

if __name__ == "__main__":
    test_youtube_api()
    test_api_quota() 