#!/usr/bin/env python3
"""
Quick Fix for YouTube API Quota Exceeded
"""

import os
import sys

def main():
    print("🚨 YouTube API Quota Exceeded - Quick Fix")
    print("=" * 50)
    
    print("\n❌ Problem: Your YouTube API quota has been exceeded.")
    print("   This is why you're getting 'Original video not found' errors.")
    
    print("\n🔧 Solutions:")
    print("1. Create a new API key (Recommended)")
    print("2. Wait for quota reset (24 hours)")
    print("3. Request quota increase")
    
    print("\n📋 Steps to Create New API Key:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable YouTube Data API v3")
    print("4. Create new API key")
    print("5. Set environment variable")
    
    print("\n💡 Quick Setup:")
    print("export YOUTUBE_API_KEY='your_new_api_key_here'")
    
    print("\n🧪 Test New Key:")
    print("python test_youtube_api.py")
    
    print("\n📊 Current API Key:")
    current_key = os.environ.get("YOUTUBE_API_KEY", "NOT SET")
    if current_key != "NOT SET":
        print(f"   {current_key[:10]}...{current_key[-4:]}")
    else:
        print("   No API key set")
    
    print("\n🔗 Useful Links:")
    print("• Google Cloud Console: https://console.cloud.google.com/")
    print("• YouTube API Quotas: https://console.cloud.google.com/apis/credentials")
    print("• API Documentation: https://developers.google.com/youtube/v3/getting-started")
    
    print("\n💭 Alternative Solutions:")
    print("• Use multiple API keys with rotation")
    print("• Implement caching to reduce API calls")
    print("• Request higher quota limits")
    print("• Use different video IDs for testing")

if __name__ == "__main__":
    main() 