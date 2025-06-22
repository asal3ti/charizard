#!/bin/bash

# YouTube Analytics API Test Script
# Tests video analytics, comment analysis, and channel analytics

BASE_URL="http://localhost:8000"
API_KEY="YOUR_API_KEY"  # Replace with your actual API key

echo "🚀 YouTube Analytics API cURL Tests"
echo "=================================="

# Test 1: Health Check
echo -e "\n🏥 Testing API Health..."
curl -s -X GET "${BASE_URL}/health" | jq '.'

# Test 2: Video Analytics
echo -e "\n📊 Testing Video Analytics..."
curl -s -X POST "${BASE_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d "{
    \"video_id\": \"dQw4w9WgXcQ\",
    \"api_key\": \"${API_KEY}\"
  }" | jq '.'

# Test 3: Channel Analytics
echo -e "\n📺 Testing Channel Analytics..."
curl -s -X GET "${BASE_URL}/api/channel/UCX6OQ3DkcsbYNE6H8uQQuVA" | jq '.'

# Test 4: Channel Comparison
echo -e "\n🔍 Testing Channel Comparison..."
curl -s -X POST "${BASE_URL}/api/channel/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_ids": [
      "UCX6OQ3DkcsbYNE6H8uQQuVA",
      "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
    ]
  }' | jq '.'

# Test 5: Metrics
echo -e "\n📈 Testing Metrics..."
curl -s -X GET "${BASE_URL}/metrics" | jq '.'

# Test 6: History
echo -e "\n📚 Testing History..."
curl -s -X GET "${BASE_URL}/history" | jq '.'

echo -e "\n✅ All cURL tests completed!" 