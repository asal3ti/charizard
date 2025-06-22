#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.youtube_service import EnhancedYouTubeService

def test_youtube_service():
    print("Testing YouTube Service...")
    
    # Create service instance
    service = EnhancedYouTubeService("test_key")
    
    # Check if methods exist
    print(f"get_video_comments exists: {hasattr(service, 'get_video_comments')}")
    print(f"get_video_transcript exists: {hasattr(service, 'get_video_transcript')}")
    print(f"get_comments exists: {hasattr(service, 'get_comments')}")
    print(f"get_transcript exists: {hasattr(service, 'get_transcript')}")
    
    # List all methods
    methods = [m for m in dir(service) if 'video' in m.lower()]
    print(f"Video-related methods: {methods}")
    
    # Try to call the method
    try:
        result = service.get_video_comments("test")
        print("get_video_comments call successful")
    except Exception as e:
        print(f"get_video_comments call failed: {e}")

if __name__ == "__main__":
    test_youtube_service() 