#!/usr/bin/env python3
"""
Test setup for YouTube Analytics AI System
"""

import os
import sys
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_environment_variables():
    """Test environment variables"""
    print("🔍 Testing environment variables...")
    
    required_vars = ['YOUTUBE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_ollama_connection():
    """Test Ollama connection"""
    print("🤖 Testing Ollama connection...")
    
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            print(f"✅ Ollama connected. Available models: {model_names}")
            
            # Check for Gemma3
            if 'gemma3:latest' in model_names:
                print("✅ Gemma3 model found")
                return True
            else:
                print("⚠️  Gemma3 model not found. Available models:", model_names)
                print("   Please run: ollama pull gemma3")
                return False
        else:
            print("❌ Ollama not responding")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def test_youtube_api():
    """Test YouTube API"""
    print("📺 Testing YouTube API...")
    
    try:
        # Test with a known video ID
        test_video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
        
        # Simple test - just check if we can make a request
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            print("❌ YouTube API key not found")
            return False
        
        url = f"https://www.googleapis.com/youtube/v3/videos"
        params = {
            'part': 'snippet',
            'id': test_video_id,
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('items'):
                title = data['items'][0]['snippet']['title']
                print(f"✅ YouTube API working. Test video: {title}")
                return True
            else:
                print("❌ No video data returned")
                return False
        else:
            print(f"❌ YouTube API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API test failed: {e}")
        return False

def test_imports():
    """Test imports"""
    print("📦 Testing imports...")
    
    try:
        # Test basic imports
        import flask
        import requests
        import pandas
        import numpy
        import textblob
        import vaderSentiment
        
        # Test our custom modules
        sys.path.append('src')
        from services.ai_service import AIService
        from agents.base_agent import BaseAgent
        from agents.analytics_agent import AnalyticsAgent
        from agents.content_agent import ContentAgent
        from agents.critique_agent import CritiqueAgent
        from agents.orchestrator_agent import OrchestratorAgent
        
        print("✅ All imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    print("🤖 Testing agent initialization...")
    
    try:
        sys.path.append('src')
        from agents.orchestrator_agent import OrchestratorAgent
        
        # Test agent initialization
        orchestrator = OrchestratorAgent()
        print("✅ Agent initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_ai_service():
    """Test AI service"""
    print("🧠 Testing AI service...")
    
    try:
        sys.path.append('src')
        from services.ai_service import AIService
        
        # Test AI service initialization
        ai_service = AIService()
        
        # Test basic response generation
        response = ai_service.generate_response("Hello, how are you?")
        if response and not response.startswith("Error"):
            print("✅ AI service working")
            return True
        else:
            print(f"❌ AI service error: {response}")
            return False
            
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 YouTube Analytics AI System - Setup Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Ollama Connection", test_ollama_connection),
        ("YouTube API", test_youtube_api),
        ("Imports", test_imports),
        ("Agent Initialization", test_agent_initialization),
        ("AI Service", test_ai_service),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Results Summary:")
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check your .env file has the correct API keys")
        print("3. Install missing dependencies: pip install -r requirements.txt")
        print("4. Download Ollama models: ollama pull gemma3")

if __name__ == "__main__":
    main() 