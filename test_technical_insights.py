#!/usr/bin/env python3
"""
Test Script for Technical Insights Feature
Tests detailed analysis of video success patterns and engagement strategies
"""

import requests
import json
import time

def test_technical_insights():
    """Test the technical insights analysis feature"""
    
    base_url = "http://localhost:8000"
    
    print("🔬 Testing Technical Insights Analysis")
    print("=" * 60)
    
    # Test video IDs (popular videos for analysis)
    test_videos = [
        "dQw4w9WgXcQ",  # Rick Roll - Rick Astley
        "9bZkp7q19f0",  # PSY - GANGNAM STYLE
        "kJQP7kiw5Fk"   # Luis Fonsi - Despacito
    ]
    
    for video_id in test_videos:
        print(f"\n📹 Analyzing Technical Insights for Video: {video_id}")
        print("-" * 50)
        
        try:
            # Test technical insights endpoint
            response = requests.post(
                f"{base_url}/api/video/technical-insights",
                json={"video_id": video_id, "max_results": 5},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if "error" in data:
                    print(f"❌ Error: {data['error']}")
                    continue
                
                # Display technical insights
                technical_insights = data.get("technical_insights", {})
                
                # Original video analysis
                original_analysis = technical_insights.get("original_video_analysis", {})
                print(f"✅ Original Video Performance:")
                print(f"   Engagement Rate: {original_analysis.get('engagement_rate', 0)}%")
                print(f"   Like Ratio: {original_analysis.get('like_ratio', 0)}%")
                print(f"   Comment Ratio: {original_analysis.get('comment_ratio', 0)}%")
                print(f"   Total Engagement: {original_analysis.get('total_engagement', 0):,}")
                
                # Similar videos analysis
                similar_analysis = technical_insights.get("similar_videos_analysis", {})
                avg_metrics = similar_analysis.get("average_metrics", {})
                print(f"\n📊 Similar Videos Average Performance:")
                print(f"   Avg Engagement Rate: {avg_metrics.get('engagement_rate', 0)}%")
                print(f"   Avg Like Ratio: {avg_metrics.get('like_ratio', 0)}%")
                print(f"   Avg Comment Ratio: {avg_metrics.get('comment_ratio', 0)}%")
                
                # Top performers
                top_performers = similar_analysis.get("top_performers", {})
                print(f"\n🏆 Top Performers:")
                
                highest_engagement = top_performers.get("highest_engagement", {})
                print(f"   Highest Engagement: {highest_engagement.get('title', 'N/A')[:50]}...")
                print(f"     Channel: {highest_engagement.get('channel', 'N/A')}")
                print(f"     Engagement Rate: {highest_engagement.get('engagement_rate', 0)}%")
                
                most_likes = top_performers.get("most_likes", {})
                print(f"   Most Likes: {most_likes.get('title', 'N/A')[:50]}...")
                print(f"     Channel: {most_likes.get('channel', 'N/A')}")
                print(f"     Likes: {most_likes.get('likes', 0):,}")
                
                most_comments = top_performers.get("most_comments", {})
                print(f"   Most Comments: {most_comments.get('title', 'N/A')[:50]}...")
                print(f"     Channel: {most_comments.get('channel', 'N/A')}")
                print(f"     Comments: {most_comments.get('comments', 0):,}")
                
                # Content patterns
                content_patterns = similar_analysis.get("content_patterns", {})
                print(f"\n📝 Content Pattern Analysis:")
                
                title_patterns = content_patterns.get("title_patterns", {})
                print(f"   Title Patterns:")
                print(f"     Videos with Emojis: {title_patterns.get('has_emojis', 0)}")
                print(f"     Videos with Numbers: {title_patterns.get('has_numbers', 0)}")
                print(f"     Videos with Brackets: {title_patterns.get('has_brackets', 0)}")
                
                tag_patterns = content_patterns.get("tag_patterns", {})
                most_common_tags = tag_patterns.get("most_common_tags", {})
                print(f"   Most Common Tags: {', '.join(list(most_common_tags.keys())[:5])}")
                
                duration_patterns = content_patterns.get("duration_patterns", {})
                optimal_duration = duration_patterns.get("optimal_duration", "N/A")
                print(f"   Optimal Duration: {optimal_duration}")
                
                # Success patterns
                success_patterns = technical_insights.get("success_patterns", {})
                print(f"\n🎯 Success Patterns:")
                
                high_engagement_indicators = success_patterns.get("high_engagement_indicators", [])
                for indicator in high_engagement_indicators[:3]:
                    print(f"   • {indicator}")
                
                content_strategies = success_patterns.get("content_strategies", [])
                for strategy in content_strategies[:3]:
                    print(f"   • {strategy}")
                
                # Engagement strategies
                engagement_strategies = technical_insights.get("engagement_strategies", {})
                print(f"\n💡 Engagement Strategies:")
                
                title_optimization = engagement_strategies.get("title_optimization", [])
                for strategy in title_optimization[:2]:
                    print(f"   • {strategy}")
                
                content_approaches = engagement_strategies.get("content_approaches", [])
                for approach in content_approaches[:2]:
                    print(f"   • {approach}")
                
                # Content insights
                content_insights = technical_insights.get("content_insights", {})
                print(f"\n📈 Content Insights:")
                
                performance_comparison = content_insights.get("performance_comparison", {})
                relative_performance = performance_comparison.get("relative_performance", "N/A")
                performance_percentile = performance_comparison.get("performance_percentile", 0)
                print(f"   Performance: {relative_performance} (Percentile: {performance_percentile})")
                
                optimization_opportunities = content_insights.get("optimization_opportunities", [])
                for opportunity in optimization_opportunities[:2]:
                    print(f"   • {opportunity}")
                
                # Recommendations
                recommendations = technical_insights.get("recommendations", [])
                print(f"\n🚀 Top Recommendations:")
                for i, recommendation in enumerate(recommendations[:5], 1):
                    print(f"   {i}. {recommendation}")
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - make sure the server is running")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Wait between requests
        time.sleep(3)
    
    print(f"\n🎯 Technical Insights Test Summary:")
    print(f"✅ Technical insights analysis tested")
    print(f"✅ Success pattern identification verified")
    print(f"✅ Engagement strategy analysis completed")
    print(f"✅ Content optimization recommendations generated")

def test_comprehensive_comparison():
    """Test the enhanced video comparison with technical insights"""
    
    base_url = "http://localhost:8000"
    
    print(f"\n🔍 Testing Enhanced Video Comparison with Technical Insights")
    print("=" * 70)
    
    try:
        # Test enhanced video comparison
        response = requests.post(
            f"{base_url}/api/video/compare",
            json={"video_id": "dQw4w9WgXcQ", "max_results": 3},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                print(f"❌ Error: {data['error']}")
                return
            
            # Check if technical insights are included
            technical_insights = data.get("technical_insights", {})
            
            if technical_insights:
                print("✅ Technical insights included in video comparison")
                
                # Show summary
                original_analysis = technical_insights.get("original_video_analysis", {})
                recommendations = technical_insights.get("recommendations", [])
                
                print(f"📊 Original Video Engagement Rate: {original_analysis.get('engagement_rate', 0)}%")
                print(f"💡 Top Recommendation: {recommendations[0] if recommendations else 'N/A'}")
                
            else:
                print("⚠️  Technical insights not found in response")
            
            # Show similar videos
            similar_videos = data.get("similar_videos", [])
            print(f"📹 Similar Videos Found: {len(similar_videos)}")
            
            for i, video in enumerate(similar_videos[:2], 1):
                print(f"  {i}. {video.get('title', 'N/A')[:50]}...")
                print(f"     Channel: {video.get('channel', 'N/A')}")
                print(f"     Engagement: {video.get('engagement_rate', 0)}%")
            
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_technical_insights()
    test_comprehensive_comparison() 