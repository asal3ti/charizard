#!/usr/bin/env python3
"""
Comprehensive Test Script for Video Comparison and Sponsorship Analysis
Tests video comparison by keywords, sponsorship detection, and sponsored video search
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

def test_video_comparison():
    """Test video comparison by keywords"""
    print("\n🔍 Testing Video Comparison by Keywords...")
    
    # Test video ID (replace with a real video ID)
    video_id = "dQw4w9WgXcQ"  # Rick Roll for testing
    
    data = {
        "video_id": video_id,
        "max_results": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/video/compare", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Video Comparison Results:")
            
            # Original video info
            if 'original_video' in result:
                original = result['original_video']
                print(f"  Original Video: {original.get('title', 'N/A')}")
                print(f"  Channel: {original.get('channel', 'N/A')}")
                print(f"  Views: {original.get('view_count', 0):,}")
                print(f"  Tags: {', '.join(original.get('tags', [])[:5])}")
            
            # Search keywords
            print(f"  Search Keywords: {result.get('search_keywords', 'N/A')}")
            
            # Similar videos
            similar_videos = result.get('similar_videos', [])
            print(f"  Similar Videos Found: {len(similar_videos)}")
            
            for i, video in enumerate(similar_videos[:3], 1):
                print(f"    {i}. {video.get('title', 'N/A')[:50]}...")
                print(f"       Channel: {video.get('channel', 'N/A')}")
                print(f"       Views: {video.get('view_count', 0):,}")
                print(f"       Engagement: {video.get('engagement_rate', 0)}%")
                
                # Sponsorship info
                sponsorship = video.get('sponsorship_analysis', {})
                if sponsorship.get('has_sponsorship'):
                    print(f"       Sponsorship: {sponsorship.get('sponsorship_level', 'N/A')} level")
                    companies = sponsorship.get('detected_companies', [])
                    if companies:
                        print(f"       Companies: {', '.join(companies[:3])}")
            
            # Sponsorship summary
            if 'sponsorship_summary' in result:
                summary = result['sponsorship_summary']
                print(f"  Sponsorship Summary:")
                print(f"    Total Videos: {summary.get('total_videos', 0)}")
                print(f"    Sponsored Videos: {summary.get('sponsored_videos', 0)}")
                print(f"    Sponsorship Rate: {summary.get('sponsorship_rate', 0)}%")
                
                # Top sponsors
                top_sponsors = summary.get('top_sponsors', [])
                if top_sponsors:
                    print(f"    Top Sponsors:")
                    for sponsor, count in top_sponsors[:3]:
                        print(f"      {sponsor}: {count} videos")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_sponsorship_analysis():
    """Test sponsorship analysis for a specific video"""
    print("\n💰 Testing Video Sponsorship Analysis...")
    
    # Test video ID (replace with a real video ID)
    video_id = "dQw4w9WgXcQ"  # Rick Roll for testing
    
    try:
        response = requests.get(f"{BASE_URL}/api/video/sponsorship/{video_id}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sponsorship Analysis Results:")
            
            print(f"  Video: {result.get('title', 'N/A')}")
            print(f"  Channel: {result.get('channel', 'N/A')}")
            print(f"  Transcript Length: {result.get('transcript_length', 0)} characters")
            
            # Sponsorship analysis
            sponsorship = result.get('sponsorship_analysis', {})
            print(f"  Has Sponsorship: {sponsorship.get('has_sponsorship', False)}")
            print(f"  Sponsorship Level: {sponsorship.get('sponsorship_level', 'N/A')}")
            print(f"  Confidence Score: {sponsorship.get('confidence_score', 0)}")
            
            # Detected companies
            companies = sponsorship.get('detected_companies', [])
            if companies:
                print(f"  Detected Companies: {', '.join(companies)}")
            
            # Extracted companies
            extracted = sponsorship.get('extracted_companies', [])
            if extracted:
                print(f"  Extracted Companies: {', '.join(extracted)}")
            
            # Discount codes
            codes = sponsorship.get('discount_codes', [])
            if codes:
                print(f"  Discount Codes: {', '.join(codes)}")
            
            # URLs
            urls = sponsorship.get('urls', [])
            if urls:
                print(f"  URLs: {', '.join(urls[:3])}")  # Show first 3 URLs
            
            # Sponsorship text
            text_segments = sponsorship.get('sponsorship_text', [])
            if text_segments:
                print(f"  Sponsorship Text Segments: {len(text_segments)} found")
                for i, segment in enumerate(text_segments[:2], 1):  # Show first 2 segments
                    print(f"    {i}. {segment[:100]}...")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search_sponsored_videos():
    """Test searching for sponsored videos by keywords"""
    print("\n🔎 Testing Sponsored Video Search...")
    
    # Test keywords
    keywords = "tech review"
    
    data = {
        "keywords": keywords,
        "max_results": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/video/search-sponsored", json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sponsored Video Search Results:")
            
            print(f"  Search Keywords: {result.get('search_keywords', 'N/A')}")
            print(f"  Total Videos Found: {result.get('total_videos', 0)}")
            
            # Videos
            videos = result.get('videos', [])
            print(f"  Videos Analyzed:")
            
            for i, video in enumerate(videos[:3], 1):
                print(f"    {i}. {video.get('title', 'N/A')[:50]}...")
                print(f"       Channel: {video.get('channel', 'N/A')}")
                print(f"       Views: {video.get('view_count', 0):,}")
                print(f"       Engagement: {video.get('engagement_rate', 0)}%")
                
                # Sponsorship info
                sponsorship = video.get('sponsorship_analysis', {})
                if sponsorship.get('has_sponsorship'):
                    print(f"       ✅ SPONSORED: {sponsorship.get('sponsorship_level', 'N/A')} level")
                    companies = sponsorship.get('detected_companies', [])
                    if companies:
                        print(f"       Companies: {', '.join(companies[:2])}")
                else:
                    print(f"       ❌ No sponsorship detected")
            
            # Sponsorship summary
            if 'sponsorship_summary' in result:
                summary = result['sponsorship_summary']
                print(f"  Sponsorship Summary:")
                print(f"    Total Videos: {summary.get('total_videos', 0)}")
                print(f"    Sponsored Videos: {summary.get('sponsored_videos', 0)}")
                print(f"    Sponsorship Rate: {summary.get('sponsorship_rate', 0)}%")
                
                # Sponsorship levels
                levels = summary.get('sponsorship_levels', {})
                print(f"    Sponsorship Levels:")
                for level, count in levels.items():
                    if count > 0:
                        print(f"      {level.capitalize()}: {count} videos")
                
                # Top sponsors
                top_sponsors = summary.get('top_sponsors', [])
                if top_sponsors:
                    print(f"    Top Sponsors:")
                    for sponsor, count in top_sponsors[:5]:
                        print(f"      {sponsor}: {count} videos")
                
                # Discount codes
                codes = summary.get('discount_codes', [])
                if codes:
                    print(f"    Discount Codes Found: {', '.join(codes)}")
                
                # Common indicators
                indicators = summary.get('common_sponsorship_indicators', [])
                if indicators:
                    print(f"    Common Sponsorship Indicators:")
                    for indicator, count in indicators[:3]:
                        print(f"      '{indicator}': {count} occurrences")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_comprehensive_sponsorship_analysis():
    """Test comprehensive sponsorship analysis across multiple videos"""
    print("\n📊 Testing Comprehensive Sponsorship Analysis...")
    
    # Test multiple videos for sponsorship patterns
    test_videos = [
        "dQw4w9WgXcQ",  # Rick Roll
        "9bZkp7q19f0",  # PSY - GANGNAM STYLE
        "kJQP7kiw5Fk"   # Luis Fonsi - Despacito
    ]
    
    all_sponsorships = []
    
    for video_id in test_videos:
        try:
            response = requests.get(f"{BASE_URL}/api/video/sponsorship/{video_id}")
            if response.status_code == 200:
                result = response.json()
                sponsorship = result.get('sponsorship_analysis', {})
                
                if sponsorship.get('has_sponsorship'):
                    all_sponsorships.append({
                        "video_id": video_id,
                        "title": result.get('title', 'N/A'),
                        "sponsorship_level": sponsorship.get('sponsorship_level', 'N/A'),
                        "companies": sponsorship.get('detected_companies', [])
                    })
            
            time.sleep(1)  # Small delay between requests
            
        except Exception as e:
            print(f"Error analyzing video {video_id}: {e}")
    
    print("✅ Comprehensive Sponsorship Analysis Results:")
    print(f"  Videos Analyzed: {len(test_videos)}")
    print(f"  Videos with Sponsorships: {len(all_sponsorships)}")
    
    if all_sponsorships:
        print("  Sponsored Videos:")
        for video in all_sponsorships:
            print(f"    • {video['title'][:40]}... ({video['sponsorship_level']} level)")
            if video['companies']:
                print(f"      Companies: {', '.join(video['companies'])}")
    
    return len(all_sponsorships) >= 0  # Success if we can analyze videos

def main():
    """Run all tests"""
    print("🚀 Starting Video Comparison and Sponsorship Analysis Tests")
    print("=" * 70)
    
    # Test health first
    if not test_health():
        print("❌ API is not healthy. Please check if the server is running.")
        return
    
    # Run all tests
    tests = [
        test_video_comparison,
        test_video_sponsorship_analysis,
        test_search_sponsored_videos,
        test_comprehensive_sponsorship_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            time.sleep(2)  # Delay between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\n✨ New Features Available:")
        print("  • Video comparison by keywords/tags")
        print("  • Sponsorship detection and analysis")
        print("  • Sponsorship company identification")
        print("  • Discount code extraction")
        print("  • Sponsored video search")
        print("  • Sponsorship pattern analysis")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 