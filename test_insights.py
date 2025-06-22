#!/usr/bin/env python3
"""
Comprehensive Insights Test - Analyze what insights we're actually generating
"""

import os
import sys
import json
import time
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.youtube_service import EnhancedYouTubeService
from agents.analytics_agent import AnalyticsAgent
from agents.critique_agent import CritiqueAgent
from agents.content_agent import ContentAgent
from agents.orchestrator_agent import OrchestratorAgent

def load_env():
    """Load environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ YOUTUBE_API_KEY not found in environment")
        return None
    return api_key

def test_basic_insights(api_key):
    """Test basic video insights"""
    print("\n🔍 Testing Basic Video Insights...")
    
    youtube_service = EnhancedYouTubeService(api_key)
    
    # Test with a popular video
    test_video_id = "dQw4w9WgXcQ"  # Rick Roll - well known video
    
    print(f"Testing with video: {test_video_id}")
    
    # Get basic video info
    video_info = youtube_service.get_video_info(test_video_id)
    if video_info:
        print("✅ Basic video info retrieved")
        print(f"   Title: {video_info.get('title', 'N/A')}")
        print(f"   Views: {video_info.get('view_count', 0):,}")
        print(f"   Likes: {video_info.get('like_count', 0):,}")
        print(f"   Comments: {video_info.get('comment_count', 0):,}")
        
        # Calculate engagement rate
        engagement_rate = ((video_info.get('like_count', 0) + video_info.get('comment_count', 0)) / video_info.get('view_count', 1)) * 100
        print(f"   Engagement Rate: {engagement_rate:.2f}%")
    else:
        print("❌ Failed to get video info")
        return False
    
    return True

def test_comment_insights(api_key):
    """Test comment analysis insights"""
    print("\n💬 Testing Comment Analysis Insights...")
    
    youtube_service = EnhancedYouTubeService(api_key)
    test_video_id = "dQw4w9WgXcQ"
    
    # Get comments
    comments = youtube_service.get_comments(test_video_id, max_results=50)
    if not comments:
        print("❌ No comments found")
        return False
    
    print(f"✅ Retrieved {len(comments)} comments")
    
    # Analyze comment patterns
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    sarcasm_count = 0
    question_count = 0
    category_counts = {}
    
    for comment in comments:
        sentiment = comment.get('sentiment', 'neutral')
        sentiment_counts[sentiment] += 1
        
        if comment.get('sarcasm') == 'sarcastic':
            sarcasm_count += 1
        
        if comment.get('is_question'):
            question_count += 1
        
        category = comment.get('category', 'other')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("📊 Comment Analysis Results:")
    print(f"   Sentiment: {sentiment_counts}")
    print(f"   Sarcastic comments: {sarcasm_count}")
    print(f"   Questions: {question_count}")
    print(f"   Categories: {category_counts}")
    
    return True

def test_transcript_insights(api_key):
    """Test transcript analysis insights"""
    print("\n📝 Testing Transcript Analysis Insights...")
    
    youtube_service = EnhancedYouTubeService(api_key)
    test_video_id = "dQw4w9WgXcQ"
    
    # Get transcript
    transcript = youtube_service.get_transcript(test_video_id)
    if not transcript:
        print("❌ No transcript found")
        return False
    
    print(f"✅ Retrieved transcript ({len(transcript)} characters)")
    
    # Basic transcript analysis
    words = transcript.split()
    sentences = transcript.split('.')
    
    print("📊 Transcript Analysis:")
    print(f"   Word count: {len(words)}")
    print(f"   Sentence count: {len(sentences)}")
    print(f"   Average sentence length: {len(words)/len(sentences):.1f} words")
    print(f"   Preview: {transcript[:200]}...")
    
    return True

def test_sponsorship_insights(api_key):
    """Test sponsorship detection insights"""
    print("\n💰 Testing Sponsorship Analysis Insights...")
    
    youtube_service = EnhancedYouTubeService(api_key)
    test_video_id = "dQw4w9WgXcQ"
    
    # Get video info and transcript
    video_info = youtube_service.get_video_info(test_video_id)
    transcript = youtube_service.get_transcript(test_video_id)
    
    if not video_info or not transcript:
        print("❌ Missing video info or transcript")
        return False
    
    # Detect sponsorships
    sponsorship_analysis = youtube_service.detect_sponsorships(
        transcript,
        video_info.get('title', ''),
        video_info.get('description', '')
    )
    
    print("📊 Sponsorship Analysis:")
    print(f"   Has sponsorships: {sponsorship_analysis.get('has_sponsorships', False)}")
    print(f"   Sponsorship count: {sponsorship_analysis.get('sponsorship_count', 0)}")
    print(f"   Sponsorship segments: {len(sponsorship_analysis.get('sponsorship_segments', []))}")
    
    if sponsorship_analysis.get('sponsorship_segments'):
        print("   Sample sponsorship text:")
        for i, segment in enumerate(sponsorship_analysis['sponsorship_segments'][:2]):
            print(f"     {i+1}. {segment[:100]}...")
    
    return True

def test_technical_insights(api_key):
    """Test technical insights and video comparison"""
    print("\n🔧 Testing Technical Insights...")
    
    youtube_service = EnhancedYouTubeService(api_key)
    test_video_id = "dQw4w9WgXcQ"
    
    # Compare with similar videos
    comparison_result = youtube_service.compare_videos_by_keywords(test_video_id, max_results=3)
    
    if "error" in comparison_result:
        print(f"❌ Comparison failed: {comparison_result['error']}")
        return False
    
    print("✅ Video comparison completed")
    
    # Extract technical insights
    technical_insights = comparison_result.get("technical_insights", {})
    
    print("📊 Technical Insights:")
    
    # Original video analysis
    original_analysis = technical_insights.get("original_video_analysis", {})
    if original_analysis:
        print(f"   Original video engagement rate: {original_analysis.get('engagement_rate', 0)}%")
        print(f"   Original video like ratio: {original_analysis.get('like_ratio', 0)}%")
    
    # Similar videos analysis
    similar_analysis = technical_insights.get("similar_videos_analysis", {})
    if similar_analysis:
        avg_metrics = similar_analysis.get("average_metrics", {})
        print(f"   Average engagement rate (similar videos): {avg_metrics.get('engagement_rate', 0)}%")
        
        top_performers = similar_analysis.get("top_performers", {})
        if top_performers.get("highest_engagement"):
            print(f"   Top engagement video: {top_performers['highest_engagement'].get('title', 'N/A')}")
    
    # Content patterns
    content_patterns = similar_analysis.get("content_patterns", {})
    if content_patterns:
        title_patterns = content_patterns.get("title_patterns", {})
        print(f"   Videos with emojis in title: {title_patterns.get('has_emojis', 0)}")
        print(f"   Videos with numbers in title: {title_patterns.get('has_numbers', 0)}")
    
    # Recommendations
    recommendations = technical_insights.get("recommendations", [])
    if recommendations:
        print("   Top recommendations:")
        for i, rec in enumerate(recommendations[:3]):
            print(f"     {i+1}. {rec}")
    
    return True

def test_agent_insights(api_key):
    """Test insights from AI agents"""
    print("\n🤖 Testing AI Agent Insights...")
    
    analytics_agent = AnalyticsAgent(api_key)
    critique_agent = CritiqueAgent()
    content_agent = ContentAgent()
    
    test_video_id = "dQw4w9WgXcQ"
    
    # Test analytics agent
    print("📊 Analytics Agent:")
    analytics_result = analytics_agent.process({"video_id": test_video_id})
    if "error" not in analytics_result:
        print("   ✅ Analytics processing successful")
    else:
        print(f"   ❌ Analytics error: {analytics_result['error']}")
    
    # Test comment analytics
    comment_analytics = analytics_agent.comment_analytics(test_video_id)
    if "error" not in comment_analytics:
        print(f"   ✅ Comment analytics: {comment_analytics.get('total_comments', 0)} comments analyzed")
    else:
        print(f"   ❌ Comment analytics error: {comment_analytics['error']}")
    
    # Test technical insights
    technical_result = analytics_agent.get_technical_insights(test_video_id)
    if "error" not in technical_result:
        print("   ✅ Technical insights generated")
        summary = technical_result.get("summary", {})
        if summary.get("top_recommendations"):
            print(f"   📋 Top recommendations: {len(summary['top_recommendations'])} generated")
    else:
        print(f"   ❌ Technical insights error: {technical_result['error']}")
    
    return True

def test_missing_insights():
    """Identify what insights we're missing"""
    print("\n❓ Identifying Missing Insights...")
    
    missing_insights = [
        "🎯 **Content Performance Predictions**: Predict how well a video will perform based on title, tags, and content",
        "📈 **Trend Analysis**: Identify trending topics and content patterns over time",
        "🎨 **Thumbnail Analysis**: Analyze thumbnail effectiveness and suggest improvements",
        "⏰ **Optimal Upload Timing**: Determine best times to upload based on audience behavior",
        "🎵 **Audio Analysis**: Analyze audio quality, music usage, and sound patterns",
        "👥 **Audience Demographics**: Estimate audience age, location, and interests",
        "🔄 **Content Repurposing Suggestions**: Identify content that could be repurposed",
        "📊 **Competitor Analysis**: Compare performance against specific competitors",
        "🎬 **Video Quality Metrics**: Analyze video resolution, frame rate, and quality",
        "💡 **Content Gap Analysis**: Identify underserved topics in your niche",
        "📱 **Cross-Platform Performance**: Compare YouTube performance with other platforms",
        "🎯 **A/B Testing Suggestions**: Suggest title/thumbnail variations to test",
        "📈 **Growth Trajectory**: Predict channel growth based on current trends",
        "🎨 **Brand Safety Analysis**: Check for potential brand safety issues",
        "📊 **Revenue Optimization**: Suggest monetization strategies based on content type"
    ]
    
    print("Missing or could be enhanced:")
    for insight in missing_insights:
        print(f"   {insight}")
    
    return missing_insights

def generate_enhanced_insights_report(api_key):
    """Generate a comprehensive insights report"""
    print("\n📋 Generating Enhanced Insights Report...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "basic_insights": {},
        "comment_insights": {},
        "transcript_insights": {},
        "sponsorship_insights": {},
        "technical_insights": {},
        "agent_insights": {},
        "missing_insights": [],
        "recommendations": []
    }
    
    youtube_service = EnhancedYouTubeService(api_key)
    test_video_id = "dQw4w9WgXcQ"
    
    # Basic insights
    video_info = youtube_service.get_video_info(test_video_id)
    if video_info:
        engagement_rate = ((video_info.get('like_count', 0) + video_info.get('comment_count', 0)) / video_info.get('view_count', 1)) * 100
        report["basic_insights"] = {
            "title": video_info.get('title'),
            "views": video_info.get('view_count'),
            "likes": video_info.get('like_count'),
            "comments": video_info.get('comment_count'),
            "engagement_rate": round(engagement_rate, 2),
            "duration": video_info.get('duration'),
            "published_at": video_info.get('published_at')
        }
    
    # Comment insights
    comments = youtube_service.get_comments(test_video_id, max_results=100)
    if comments:
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        category_counts = {}
        for comment in comments:
            sentiment = comment.get('sentiment', 'neutral')
            sentiment_counts[sentiment] += 1
            category = comment.get('category', 'other')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        report["comment_insights"] = {
            "total_comments": len(comments),
            "sentiment_distribution": sentiment_counts,
            "category_distribution": category_counts,
            "sarcasm_count": sum(1 for c in comments if c.get('sarcasm') == 'sarcastic'),
            "question_count": sum(1 for c in comments if c.get('is_question'))
        }
    
    # Technical insights
    comparison_result = youtube_service.compare_videos_by_keywords(test_video_id, max_results=3)
    if "error" not in comparison_result:
        technical_insights = comparison_result.get("technical_insights", {})
        report["technical_insights"] = {
            "original_video_analysis": technical_insights.get("original_video_analysis", {}),
            "similar_videos_analysis": technical_insights.get("similar_videos_analysis", {}),
            "recommendations": technical_insights.get("recommendations", [])[:5]
        }
    
    # Missing insights
    report["missing_insights"] = test_missing_insights()
    
    # Recommendations
    report["recommendations"] = [
        "Implement content performance prediction using ML models",
        "Add thumbnail analysis using computer vision",
        "Create trend analysis dashboard with historical data",
        "Build audience demographics estimation",
        "Add cross-platform performance comparison",
        "Implement A/B testing framework for titles and thumbnails",
        "Create content gap analysis tool",
        "Add brand safety monitoring",
        "Build revenue optimization suggestions",
        "Implement growth trajectory predictions"
    ]
    
    return report

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive Insights Analysis...")
    
    api_key = load_env()
    if not api_key:
        return
    
    # Run all tests
    tests = [
        ("Basic Insights", lambda: test_basic_insights(api_key)),
        ("Comment Insights", lambda: test_comment_insights(api_key)),
        ("Transcript Insights", lambda: test_transcript_insights(api_key)),
        ("Sponsorship Insights", lambda: test_sponsorship_insights(api_key)),
        ("Technical Insights", lambda: test_technical_insights(api_key)),
        ("Agent Insights", lambda: test_agent_insights(api_key))
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            start_time = time.time()
            result = test_func()
            end_time = time.time()
            results[test_name] = {
                "success": result,
                "duration": round(end_time - start_time, 2)
            }
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results[test_name] = {
                "success": False,
                "error": str(e)
            }
    
    # Generate comprehensive report
    try:
        report = generate_enhanced_insights_report(api_key)
        
        # Save report
        with open("insights_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Comprehensive report saved to insights_report.json")
        
        # Print summary
        print("\n📊 Test Results Summary:")
        for test_name, result in results.items():
            status = "✅ PASS" if result.get("success") else "❌ FAIL"
            duration = f"({result.get('duration', 0)}s)" if result.get("duration") else ""
            print(f"   {test_name}: {status} {duration}")
        
        print(f"\n🎯 Key Insights Generated:")
        if report["basic_insights"]:
            print(f"   📈 Engagement Rate: {report['basic_insights'].get('engagement_rate', 0)}%")
        if report["comment_insights"]:
            print(f"   💬 Comments Analyzed: {report['comment_insights'].get('total_comments', 0)}")
        if report["technical_insights"].get("recommendations"):
            print(f"   🔧 Recommendations: {len(report['technical_insights']['recommendations'])} generated")
        
        print(f"\n❌ Missing Insights: {len(report['missing_insights'])} identified")
        print(f"💡 Recommendations: {len(report['recommendations'])} for enhancement")
        
    except Exception as e:
        print(f"❌ Report generation failed: {e}")

if __name__ == "__main__":
    main() 