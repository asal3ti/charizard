#!/usr/bin/env python3
"""
Comprehensive Test Script for YouTube Analytics API
Tests video analytics, comment analysis, and channel analytics
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key

def test_health():
    """Test API health"""
    print("🏥 Testing API Health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_video_analytics():
    """Test comprehensive video analytics"""
    print("\n📊 Testing Video Analytics...")
    
    # Test video ID (replace with a real video ID)
    video_id = "dQw4w9WgXcQ"  # Rick Roll for testing
    
    data = {
        "video_id": video_id,
        "api_key": API_KEY
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analyze", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Video Analytics Results:")
            print(f"  Title: {result.get('title', 'N/A')}")
            print(f"  Channel: {result.get('channel', 'N/A')}")
            print(f"  Views: {result.get('view_count', 0):,}")
            print(f"  Likes: {result.get('like_count', 0):,}")
            print(f"  Comments: {result.get('comment_count', 0):,}")
            print(f"  Engagement Rate: {result.get('engagement_rate', 0)}%")
            print(f"  Like Ratio: {result.get('like_ratio', 0)}%")
            print(f"  Comment Ratio: {result.get('comment_ratio', 0)}%")
            
            # Performance metrics
            if 'performance_metrics' in result:
                perf = result['performance_metrics']
                print(f"  Growth Rate: {perf.get('growth_rate', 0)}%")
                print(f"  Viral Score: {perf.get('viral_score', 0)}")
                print(f"  Views per Day: {perf.get('views_per_day', 0)}")
            
            # Comment analytics
            if 'comment_analytics' in result:
                comments = result['comment_analytics']
                print(f"  Total Comments Analyzed: {comments.get('total_comments', 0)}")
                print(f"  Positive: {comments.get('positive_count', 0)}")
                print(f"  Negative: {comments.get('negative_count', 0)}")
                print(f"  Neutral: {comments.get('neutral_count', 0)}")
                print(f"  Questions: {comments.get('question_count', 0)}")
                print(f"  Spam: {comments.get('spam_count', 0)}")
                print(f"  Sentiment Score: {comments.get('sentiment_score', 0)}")
                
                # Comment categorization
                if 'categorization' in comments:
                    cat = comments['categorization']
                    print("  Comment Categories:")
                    for category, count in cat.items():
                        if count > 0:
                            print(f"    {category}: {count}")
                
                # Question types
                if 'question_types' in comments:
                    q_types = comments['question_types']
                    print("  Question Types:")
                    for q_type, count in q_types.items():
                        if count > 0:
                            print(f"    {q_type}: {count}")
                
                # Comment overview
                if 'overview' in comments:
                    overview = comments['overview']
                    print("  Comment Overview:")
                    for insight in overview.get('insights', []):
                        print(f"    • {insight}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_channel_analytics():
    """Test channel analytics"""
    print("\n📺 Testing Channel Analytics...")
    
    # Test channel ID (replace with a real channel ID)
    channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"  # MrBeast for testing
    
    try:
        response = requests.get(f"{BASE_URL}/api/channel/{channel_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Channel Analytics Results:")
            
            # Channel info
            if 'channel_info' in result:
                info = result['channel_info']
                print(f"  Channel: {info.get('title', 'N/A')}")
                print(f"  Published: {info.get('published_at', 'N/A')}")
                print(f"  Country: {info.get('country', 'N/A')}")
            
            # Statistics
            if 'statistics' in result:
                stats = result['statistics']
                print(f"  Subscribers: {stats.get('subscriber_count', 0):,}")
                print(f"  Total Videos: {stats.get('video_count', 0):,}")
                print(f"  Total Views: {stats.get('view_count', 0):,}")
                print(f"  Analyzed Views: {stats.get('total_views', 0):,}")
                print(f"  Analyzed Likes: {stats.get('total_likes', 0):,}")
                print(f"  Analyzed Comments: {stats.get('total_comments', 0):,}")
            
            # Metrics
            if 'metrics' in result:
                metrics = result['metrics']
                print(f"  Avg Views per Video: {metrics.get('avg_views_per_video', 0):,}")
                print(f"  Avg Likes per Video: {metrics.get('avg_likes_per_video', 0):,}")
                print(f"  Avg Comments per Video: {metrics.get('avg_comments_per_video', 0):,}")
                print(f"  Channel Engagement Rate: {metrics.get('channel_engagement_rate', 0)}%")
                print(f"  Views per Subscriber: {metrics.get('views_per_subscriber', 0)}")
                print(f"  Videos per Month: {metrics.get('videos_per_month', 0)}")
            
            # Performance analysis
            if 'performance_analysis' in result:
                perf = result['performance_analysis']
                print("  Performance Insights:")
                for insight in perf.get('insights', []):
                    print(f"    • {insight}")
            
            # Recent videos
            if 'recent_videos' in result:
                videos = result['recent_videos']
                print(f"  Recent Videos Analyzed: {len(videos)}")
                if videos:
                    print("  Top Recent Videos:")
                    for i, video in enumerate(videos[:3], 1):
                        print(f"    {i}. {video.get('title', 'N/A')[:50]}...")
                        print(f"       Views: {video.get('views', 0):,}, Engagement: {video.get('engagement_rate', 0)}%")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_channel_comparison():
    """Test channel comparison"""
    print("\n🔍 Testing Channel Comparison...")
    
    # Test channel IDs (replace with real channel IDs)
    channel_ids = [
        "UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast
        "UC-lHJZR3Gqxm24_Vd_AJ5Yw"   # PewDiePie
    ]
    
    data = {
        "channel_ids": channel_ids
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/channel/compare", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Channel Comparison Results:")
            
            for channel_id, data in result.items():
                print(f"\n  Channel: {data.get('title', 'N/A')}")
                print(f"    Subscribers: {data.get('subscribers', 0):,}")
                print(f"    Total Views: {data.get('total_views', 0):,}")
                print(f"    Engagement Rate: {data.get('engagement_rate', 0)}%")
                print(f"    Avg Views per Video: {data.get('avg_views_per_video', 0):,}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print("\n📈 Testing Metrics...")
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Metrics Results:")
            print(f"  Total Videos Analyzed: {result.get('total_videos', 0)}")
            print(f"  Total Comments Analyzed: {result.get('total_comments', 0)}")
            print(f"  Average Engagement Rate: {result.get('avg_engagement_rate', 0)}%")
            print(f"  Average Sentiment Score: {result.get('avg_sentiment_score', 0)}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_history():
    """Test history endpoint"""
    print("\n📚 Testing History...")
    try:
        response = requests.get(f"{BASE_URL}/history")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ History Results:")
            print(f"  Total Records: {len(result.get('analytics', []))}")
            
            # Show recent analyses
            for analysis in result.get('analytics', [])[:3]:
                print(f"  • {analysis.get('title', 'N/A')} - {analysis.get('analyzed_at', 'N/A')}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive YouTube Analytics API Tests")
    print("=" * 60)
    
    # Test health first
    if not test_health():
        print("❌ API is not healthy. Please check if the server is running.")
        return
    
    # Run all tests
    tests = [
        test_video_analytics,
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
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 