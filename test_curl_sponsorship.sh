#!/bin/bash

# Video Comparison and Sponsorship Analysis API Test Script
# Tests video comparison by keywords, sponsorship detection, and sponsored video search

BASE_URL="http://localhost:8000"
API_KEY="YOUR_API_KEY"  # Replace with your actual API key

echo "🚀 Video Comparison and Sponsorship Analysis API Tests"
echo "====================================================="

# Test 1: Health Check
echo -e "\n🏥 Testing API Health..."
curl -s -X GET "${BASE_URL}/health" | jq '.'

# Test 2: Video Comparison by Keywords
echo -e "\n🔍 Testing Video Comparison by Keywords..."
curl -s -X POST "${BASE_URL}/api/video/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "max_results": 5
  }' | jq '.'

# Test 3: Video Sponsorship Analysis
echo -e "\n💰 Testing Video Sponsorship Analysis..."
curl -s -X GET "${BASE_URL}/api/video/sponsorship/dQw4w9WgXcQ" | jq '.'

# Test 4: Search Sponsored Videos
echo -e "\n🔎 Testing Sponsored Video Search..."
curl -s -X POST "${BASE_URL}/api/video/search-sponsored" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "tech review",
    "max_results": 5
  }' | jq '.'

# Test 5: Multiple Video Sponsorship Analysis
echo -e "\n📊 Testing Multiple Video Sponsorship Analysis..."
echo "Analyzing video 1: dQw4w9WgXcQ"
curl -s -X GET "${BASE_URL}/api/video/sponsorship/dQw4w9WgXcQ" | jq '.sponsorship_analysis.has_sponsorship, .sponsorship_analysis.sponsorship_level, .sponsorship_analysis.detected_companies'

echo -e "\nAnalyzing video 2: 9bZkp7q19f0"
curl -s -X GET "${BASE_URL}/api/video/sponsorship/9bZkp7q19f0" | jq '.sponsorship_analysis.has_sponsorship, .sponsorship_analysis.sponsorship_level, .sponsorship_analysis.detected_companies'

echo -e "\nAnalyzing video 3: kJQP7kiw5Fk"
curl -s -X GET "${BASE_URL}/api/video/sponsorship/kJQP7kiw5Fk" | jq '.sponsorship_analysis.has_sponsorship, .sponsorship_analysis.sponsorship_level, .sponsorship_analysis.detected_companies'

# Test 6: Search with Different Keywords
echo -e "\n🎮 Testing Search with Gaming Keywords..."
curl -s -X POST "${BASE_URL}/api/video/search-sponsored" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "gaming review",
    "max_results": 3
  }' | jq '.sponsorship_summary'

# Test 7: Search with Tech Keywords
echo -e "\n💻 Testing Search with Tech Keywords..."
curl -s -X POST "${BASE_URL}/api/video/search-sponsored" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "smartphone review",
    "max_results": 3
  }' | jq '.sponsorship_summary'

echo -e "\n✅ All sponsorship analysis tests completed!"
echo -e "\n📋 Available Endpoints:"
echo "  • POST /api/video/compare - Compare videos by keywords"
echo "  • GET /api/video/sponsorship/{video_id} - Analyze video sponsorships"
echo "  • POST /api/video/search-sponsored - Search for sponsored videos" 