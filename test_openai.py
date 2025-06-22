#!/usr/bin/env python3
"""
Test OpenAI Integration
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_openai_integration():
    """Test OpenAI integration"""
    print("🧪 Testing OpenAI Integration...")
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    print("✅ OpenAI API key found")
    
    try:
        # Test AI service
        from src.services.ai_service import AIService
        
        ai_service = AIService()
        print("✅ AI Service initialized")
        
        # Test basic response
        response = ai_service.generate_response("Hello, how are you?", max_tokens=50)
        print(f"✅ Basic response test: {response[:50]}...")
        
        # Test sentiment analysis
        sentiment = ai_service.analyze_sentiment("I love this video! It's amazing!")
        print(f"✅ Sentiment analysis: {sentiment}")
        
        # Test comment categorization
        category = ai_service.categorize_comment("How do you make this recipe?")
        print(f"✅ Comment categorization: {category}")
        
        # Test insights generation
        insights = ai_service.generate_insights({"views": 1000, "likes": 50}, "video performance")
        print(f"✅ Insights generation: {insights}")
        
        print("🎉 All OpenAI tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

def test_enhanced_insights():
    """Test enhanced insights service"""
    print("\n🔍 Testing Enhanced Insights Service...")
    
    try:
        from src.services.enhanced_insights_service import EnhancedInsightsService
        
        insights_service = EnhancedInsightsService()
        print("✅ Enhanced Insights Service initialized")
        
        # Test content performance prediction
        video_data = {
            "title": "Amazing Tutorial: How to Build a Website in 10 Minutes",
            "description": "Learn how to create a stunning website quickly and easily",
            "tags": ["tutorial", "web development", "coding", "beginner"]
        }
        
        performance = insights_service.analyze_content_performance_potential(video_data)
        print(f"✅ Performance prediction: Score {performance.get('performance_score', 0)}")
        
        # Test content optimization suggestions
        suggestions = insights_service.generate_content_optimization_suggestions(video_data, [])
        print(f"✅ Optimization suggestions: {len(suggestions.get('suggestions', {}).get('title_optimization', []))} suggestions")
        
        print("🎉 Enhanced insights tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced insights test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting OpenAI Integration Tests...")
    
    # Test OpenAI integration
    openai_success = test_openai_integration()
    
    # Test enhanced insights
    insights_success = test_enhanced_insights()
    
    # Summary
    print("\n📊 Test Results:")
    print(f"   OpenAI Integration: {'✅ PASS' if openai_success else '❌ FAIL'}")
    print(f"   Enhanced Insights: {'✅ PASS' if insights_success else '❌ FAIL'}")
    
    if openai_success and insights_success:
        print("\n🎉 All tests passed! OpenAI integration is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Set your OPENAI_API_KEY in .env file")
        print("   2. Set your YOUTUBE_API_KEY in .env file")
        print("   3. Run: python src/app.py")
        print("   4. Test the new enhanced insights endpoints")
    else:
        print("\n❌ Some tests failed. Please check your configuration.")

if __name__ == "__main__":
    main() 