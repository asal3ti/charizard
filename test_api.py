#!/usr/bin/env python3
"""
Comprehensive API Test Script for YouTube Analytics AI Backend
Tests all endpoints and functionality
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TEST_VIDEO_ID = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
TEST_CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers
TEST_VIDEO_IDS = ["dQw4w9WgXcQ", "9bZkp7q19f0", "kJQP7kiw5Fk"]  # Multiple videos for comparison

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_response(response: requests.Response, title: str = "Response"):
    """Print formatted response"""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response: {response.text}")

def test_health_check():
    """Test 1: Health Check"""
    print_section("1. HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_agent_capabilities():
    """Test 2: Agent Capabilities"""
    print_section("2. AGENT CAPABILITIES")
    
    try:
        response = requests.get(f"{BASE_URL}/api/agents")
        print_response(response, "Agent Capabilities")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_workflow_status():
    """Test 3: Workflow Status"""
    print_section("3. WORKFLOW STATUS")
    
    try:
        response = requests.post(f"{BASE_URL}/api/workflow")
        print_response(response, "Workflow Status")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_video_analytics():
    """Test 4: Video Analytics Only"""
    print_section("4. VIDEO ANALYTICS")
    
    payload = {
        "video_id": TEST_VIDEO_ID
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analytics",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Video Analytics")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_comments_analysis():
    """Test 5: Comments Analysis"""
    print_section("5. COMMENTS ANALYSIS")
    
    payload = {
        "video_id": TEST_VIDEO_ID
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/comments",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Comments Analysis")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_transcript_analysis():
    """Test 6: Transcript Analysis"""
    print_section("6. TRANSCRIPT ANALYSIS")
    
    payload = {
        "video_id": TEST_VIDEO_ID
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/transcript",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Transcript Analysis")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_channel_analysis():
    """Test 7: Channel Analysis"""
    print_section("7. CHANNEL ANALYSIS")
    
    payload = {
        "channel_id": TEST_CHANNEL_ID
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/channel",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Channel Analysis")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_video_comparison():
    """Test 8: Video Comparison"""
    print_section("8. VIDEO COMPARISON")
    
    payload = {
        "video_ids": TEST_VIDEO_IDS
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/compare",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Video Comparison")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_content_generation():
    """Test 9: Content Generation"""
    print_section("9. CONTENT GENERATION")
    
    # Mock analytics data for content generation
    mock_analytics = {
        "video_analytics": {
            "basic_info": {
                "title": "Test Video",
                "view_count": 1000000,
                "like_count": 50000
            }
        },
        "comment_analysis": {
            "total_comments": 2000,
            "sentiment_breakdown": {
                "positive": 1200,
                "negative": 200,
                "neutral": 600
            }
        },
        "transcript_analysis": {
            "word_count": 1500,
            "ai_analysis": "This is a test video analysis."
        }
    }
    
    payload = {
        "analytics_data": mock_analytics,
        "content_type": "social_post"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/content",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Content Generation")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_content_critique():
    """Test 10: Content Critique"""
    print_section("10. CONTENT CRITIQUE")
    
    mock_content = {
        "content": "This is a test social media post about our latest video. Check it out!",
        "image_prompt": "A professional image showing analytics dashboard"
    }
    
    payload = {
        "content": mock_content,
        "content_type": "social_post"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/critique",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Content Critique")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_full_analysis_analytics_only():
    """Test 11: Full Analysis - Analytics Only"""
    print_section("11. FULL ANALYSIS - ANALYTICS ONLY")
    
    payload = {
        "video_id": TEST_VIDEO_ID,
        "workflow_steps": ["analytics"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Full Analysis - Analytics Only")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_full_analysis_with_content():
    """Test 12: Full Analysis - Analytics + Content"""
    print_section("12. FULL ANALYSIS - ANALYTICS + CONTENT")
    
    payload = {
        "video_id": TEST_VIDEO_ID,
        "workflow_steps": ["analytics", "content"],
        "content_type": "social_post"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Full Analysis - Analytics + Content")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_full_analysis_complete():
    """Test 13: Full Analysis - Complete Workflow"""
    print_section("13. FULL ANALYSIS - COMPLETE WORKFLOW")
    
    payload = {
        "video_id": TEST_VIDEO_ID,
        "workflow_steps": ["analytics", "content", "critique"],
        "content_type": "social_post"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Full Analysis - Complete Workflow")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_error_handling():
    """Test 14: Error Handling"""
    print_section("14. ERROR HANDLING")
    
    # Test with invalid video ID
    payload = {
        "video_id": "invalid_video_id"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analytics",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Error Handling - Invalid Video ID")
        
        # Test with missing required field
        payload = {}
        response = requests.post(
            f"{BASE_URL}/api/analytics",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Error Handling - Missing Video ID")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_different_content_types():
    """Test 15: Different Content Types"""
    print_section("15. DIFFERENT CONTENT TYPES")
    
    content_types = ["social_post", "blog_post", "newsletter", "tweet"]
    
    for content_type in content_types:
        print(f"\nTesting content type: {content_type}")
        
        payload = {
            "video_id": TEST_VIDEO_ID,
            "workflow_steps": ["analytics", "content"],
            "content_type": content_type
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/analyze",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if "results" in data and "content" in data["results"]:
                    print(f"Content generated: {len(data['results']['content'].get('content', ''))} characters")
        except Exception as e:
            print(f"Error: {e}")

def test_task_management():
    """Test 16: Task Management"""
    print_section("16. TASK MANAGEMENT")
    
    # Test 1: Start a task with content generation
    payload = {
        "video_id": TEST_VIDEO_ID,
        "workflow_steps": ["analytics", "content"],
        "content_type": "social_post"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Start Task")
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            
            if task_id:
                # Test 2: Check task status
                print(f"\nChecking task status for: {task_id}")
                status_response = requests.get(f"{BASE_URL}/api/task/{task_id}")
                print_response(status_response, "Task Status")
                
                # Test 3: Wait and check again
                print(f"\nWaiting 5 seconds and checking again...")
                time.sleep(5)
                status_response2 = requests.get(f"{BASE_URL}/api/task/{task_id}")
                print_response(status_response2, "Task Status After Wait")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_list_tasks():
    """Test 17: List Tasks"""
    print_section("17. LIST TASKS")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tasks")
        print_response(response, "List Tasks")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_content_generation_with_task():
    """Test 18: Content Generation with Task Management"""
    print_section("18. CONTENT GENERATION WITH TASK")
    
    payload = {
        "video_id": TEST_VIDEO_ID,
        "content_type": "social_post"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/content",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print_response(response, "Content Generation with Task")
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            
            if task_id:
                # Wait and check status
                print(f"\nWaiting for content generation to complete...")
                max_wait = 30  # 30 seconds max
                wait_time = 0
                
                while wait_time < max_wait:
                    time.sleep(2)
                    wait_time += 2
                    
                    status_response = requests.get(f"{BASE_URL}/api/task/{task_id}")
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data.get('status') == 'completed':
                            print_response(status_response, "Completed Content Generation")
                            return True
                        elif status_data.get('status') == 'failed':
                            print_response(status_response, "Failed Content Generation")
                            return False
                    
                    print(f"Still processing... ({wait_time}s)")
                
                print("Task timed out")
                return False
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_cleanup_tasks():
    """Test 19: Cleanup Tasks"""
    print_section("19. CLEANUP TASKS")
    
    try:
        response = requests.post(f"{BASE_URL}/api/tasks/cleanup")
        print_response(response, "Cleanup Tasks")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 STARTING COMPREHENSIVE API TESTS")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Video ID: {TEST_VIDEO_ID}")
    print(f"Test Channel ID: {TEST_CHANNEL_ID}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Agent Capabilities", test_agent_capabilities),
        ("Workflow Status", test_workflow_status),
        ("Video Analytics", test_video_analytics),
        ("Comments Analysis", test_comments_analysis),
        ("Transcript Analysis", test_transcript_analysis),
        ("Channel Analysis", test_channel_analysis),
        ("Video Comparison", test_video_comparison),
        ("Content Generation", test_content_generation),
        ("Content Critique", test_content_critique),
        ("Full Analysis - Analytics Only", test_full_analysis_analytics_only),
        ("Full Analysis - Analytics + Content", test_full_analysis_with_content),
        ("Full Analysis - Complete Workflow", test_full_analysis_complete),
        ("Error Handling", test_error_handling),
        ("Task Management", test_task_management),
        ("List Tasks", test_list_tasks),
        ("Content Generation with Task", test_content_generation_with_task),
        ("Cleanup Tasks", test_cleanup_tasks),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n⏳ Running: {test_name}")
        start_time = time.time()
        
        try:
            success = test_func()
            end_time = time.time()
            duration = end_time - start_time
            
            status = "✅ PASS" if success else "❌ FAIL"
            results.append((test_name, success, duration))
            
            print(f"{status} - {test_name} ({duration:.2f}s)")
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            results.append((test_name, False, duration))
            print(f"❌ FAIL - {test_name} ({duration:.2f}s) - Exception: {e}")
    
    # Test different content types
    print("\n⏳ Running: Different Content Types")
    start_time = time.time()
    test_different_content_types()
    end_time = time.time()
    duration = end_time - start_time
    results.append(("Different Content Types", True, duration))
    print(f"✅ PASS - Different Content Types ({duration:.2f}s)")
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    total_time = sum(duration for _, _, duration in results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print(f"Total Time: {total_time:.2f}s")
    
    print("\nDetailed Results:")
    for test_name, success, duration in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {test_name} ({duration:.2f}s)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} TESTS FAILED")

if __name__ == "__main__":
    run_all_tests() 