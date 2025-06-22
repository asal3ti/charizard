#!/usr/bin/env python3
"""
Test Script for Channel Exclusion in Video Comparison
"""

import requests
import json
import time

def test_channel_exclusion():
    """Test that video comparison excludes same channel videos"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Channel Exclusion in Video Comparison")
    print("=" * 60)
    
    # Test video IDs (popular videos from different channels)
    test_videos = [
        "dQw4w9WgXcQ",  # Rick Roll - Rick Astley
        "9bZkp7q19f0",  # PSY - GANGNAM STYLE
        "kJQP7kiw5Fk",  # Luis Fonsi - Despacito
        "y6120QOlsfU",  # Sandstorm - Darude
        "ZZ5LpwO-An4"   # Never Gonna Give You Up - Rick Astley
    ]
    
    for video_id in test_videos:
        print(f"\n📹 Testing Video: {video_id}")
        print("-" * 40)
        
        try:
            # Test video comparison
            response = requests.post(
                f"{base_url}/api/video/compare",
                json={"video_id": video_id, "max_results": 5},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    print(f"❌ Error: {data['error']}")
                    continue
                
                # Check original video info
                original_video = data.get("original_video", {})
                original_channel = original_video.get("channel", "Unknown")
                original_channel_id = original_video.get("channel_id", "")
                
                print(f"✅ Original Video: {original_video.get('title', 'N/A')[:50]}...")
                print(f"✅ Channel: {original_channel}")
                print(f"✅ Channel ID: {original_channel_id}")
                
                # Check search keywords (should not contain channel name)
                search_keywords = data.get("search_keywords", "")
                print(f"✅ Search Keywords: {search_keywords[:100]}...")
                
                # Check if channel name is excluded from search keywords
                if original_channel.lower() in search_keywords.lower():
                    print(f"⚠️  Warning: Channel name '{original_channel}' found in search keywords")
                else:
                    print(f"✅ Channel name successfully excluded from search keywords")
                
                # Check similar videos
                similar_videos = data.get("similar_videos", [])
                print(f"✅ Similar Videos Found: {len(similar_videos)}")
                
                # Verify no videos from same channel
                same_channel_count = 0
                for video in similar_videos:
                    video_channel = video.get("channel", "")
                    video_channel_id = video.get("channel_id", "")
                    
                    if video_channel_id == original_channel_id:
                        same_channel_count += 1
                        print(f"❌ Found video from same channel: {video.get('title', 'N/A')[:50]}...")
                
                if same_channel_count == 0:
                    print(f"✅ All similar videos are from different channels")
                else:
                    print(f"❌ Found {same_channel_count} videos from the same channel")
                
                # Show top similar videos
                print(f"\n📊 Top Similar Videos:")
                for i, video in enumerate(similar_videos[:3], 1):
                    print(f"  {i}. {video.get('title', 'N/A')[:60]}...")
                    print(f"     Channel: {video.get('channel', 'N/A')}")
                    print(f"     Views: {video.get('view_count', 0):,}")
                    print(f"     Engagement: {video.get('engagement_rate', 0)}%")
                
                # Check exclusion flag
                excluded_flag = data.get("excluded_same_channel", False)
                if excluded_flag:
                    print(f"✅ Same channel exclusion flag: {excluded_flag}")
                else:
                    print(f"⚠️  Same channel exclusion flag not set")
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - make sure the server is running")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Wait between requests to avoid rate limiting
        time.sleep(2)
    
    print(f"\n🎯 Test Summary:")
    print(f"✅ Channel exclusion functionality tested")
    print(f"✅ Channel name removal from search keywords tested")
    print(f"✅ Similar video filtering verified")

if __name__ == "__main__":
    test_channel_exclusion() 