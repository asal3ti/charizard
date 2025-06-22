# YouTube Analytics AI Backend - Testing Guide

This guide provides comprehensive testing instructions for the YouTube Analytics AI Backend API.

## Quick Start

### Prerequisites
- Server running on `http://localhost:8000`
- Ollama with Gemma3 model running
- YouTube API key configured
- `jq` installed for JSON formatting (optional): `brew install jq`

### Test Files Available

1. **`test_api.py`** - Comprehensive Python test script
2. **`test_curl.sh`** - Shell script with cURL commands
3. **`test_api.js`** - JavaScript test script for frontend testing

## Running Tests

### 1. Python Tests (Recommended)
```bash
python test_api.py
```

### 2. cURL Tests
```bash
./test_curl.sh
```

### 3. JavaScript Tests
```bash
node test_api.js
```

## Individual Test Requests

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Agent Capabilities
```bash
curl http://localhost:8000/api/agents
```

### 3. Workflow Status
```bash
curl -X POST http://localhost:8000/api/workflow
```

### 4. Video Analytics
```bash
curl -X POST http://localhost:8000/api/analytics \
  -H "Content-Type: application/json" \
  -d '{"video_id": "dQw4w9WgXcQ"}'
```

### 5. Comments Analysis
```bash
curl -X POST http://localhost:8000/api/comments \
  -H "Content-Type: application/json" \
  -d '{"video_id": "dQw4w9WgXcQ"}'
```

### 6. Transcript Analysis
```bash
curl -X POST http://localhost:8000/api/transcript \
  -H "Content-Type: application/json" \
  -d '{"video_id": "dQw4w9WgXcQ"}'
```

### 7. Channel Analysis
```bash
curl -X POST http://localhost:8000/api/channel \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw"}'
```

### 8. Video Comparison
```bash
curl -X POST http://localhost:8000/api/compare \
  -H "Content-Type: application/json" \
  -d '{"video_ids": ["dQw4w9WgXcQ", "9bZkp7q19f0", "kJQP7kiw5Fk"]}'
```

### 9. Content Generation
```bash
curl -X POST http://localhost:8000/api/content \
  -H "Content-Type: application/json" \
  -d '{
    "analytics_data": {
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
    },
    "content_type": "social_post"
  }'
```

### 10. Content Critique
```bash
curl -X POST http://localhost:8000/api/critique \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "content": "This is a test social media post about our latest video. Check it out!",
      "image_prompt": "A professional image showing analytics dashboard"
    },
    "content_type": "social_post"
  }'
```

### 11. Full Analysis - Analytics Only
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics"]
  }'
```

### 12. Full Analysis - Analytics + Content (Task-based)
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "social_post"
  }'
```

### 13. Full Analysis - Complete Workflow (Task-based)
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content", "critique"],
    "content_type": "social_post"
  }'
```

### 14. Task Management - Check Task Status
```bash
# First start a task (use response from step 12 or 13)
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "social_post"
  }'

# Then check status using the returned task_id
curl http://localhost:8000/api/task/task_1234567890_dQw4w9WgXcQ
```

### 15. Content Generation with Task Management
```bash
curl -X POST http://localhost:8000/api/content \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "content_type": "social_post"
  }'
```

### 16. List All Tasks
```bash
curl http://localhost:8000/api/tasks
```

### 17. Cleanup Old Tasks
```bash
curl -X POST http://localhost:8000/api/tasks/cleanup
```

### 18. Error Handling - Invalid Video ID
```bash
curl -X POST http://localhost:8000/api/analytics \
  -H "Content-Type: application/json" \
  -d '{"video_id": "invalid_video_id"}'
```

### 19. Error Handling - Missing Video ID
```bash
curl -X POST http://localhost:8000/api/analytics \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 20. Different Content Types
```bash
# Social Post
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "social_post"
  }'

# Blog Post
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "blog_post"
  }'

# Newsletter
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "newsletter"
  }'

# Tweet
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "tweet"
  }'
```

## JavaScript/React Integration

### Basic Usage
```javascript
// Health check
const checkHealth = async () => {
  const response = await fetch('http://localhost:8000/health');
  const data = await response.json();
  console.log('Service status:', data.status);
};

// Video analysis
const analyzeVideo = async (videoId) => {
  const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      video_id: videoId,
      workflow_steps: ['analytics', 'content', 'critique'],
      content_type: 'social_post'
    })
  });
  
  return await response.json();
};

// Usage
const videoId = 'dQw4w9WgXcQ';
const results = await analyzeVideo(videoId);
console.log('Analysis results:', results);
```

### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

function VideoAnalyzer() {
  const [videoId, setVideoId] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeVideo = async () => {
    if (!videoId) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_id: videoId,
          workflow_steps: ['analytics', 'content', 'critique'],
          content_type: 'social_post'
        })
      });
      
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={videoId}
        onChange={(e) => setVideoId(e.target.value)}
        placeholder="Enter YouTube Video ID"
      />
      <button onClick={analyzeVideo} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Video'}
      </button>
      
      {results && (
        <div>
          <h3>Analysis Results</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

## Python Integration

### Basic Usage
```python
import requests
import json

def analyze_video(video_id):
    url = 'http://localhost:8000/api/analyze'
    payload = {
        'video_id': video_id,
        'workflow_steps': ['analytics', 'content', 'critique'],
        'content_type': 'social_post'
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage
video_id = 'dQw4w9WgXcQ'
results = analyze_video(video_id)
print(json.dumps(results, indent=2))
```

## Test Video IDs

Use these test video IDs for testing:

- `dQw4w9WgXcQ` - Rick Astley - Never Gonna Give You Up
- `9bZkp7q19f0` - PSY - GANGNAM STYLE
- `kJQP7kiw5Fk` - Luis Fonsi - Despacito

## Test Channel IDs

- `UC_x5XG1OV2P6uZZ5FSM9Ttw` - Google Developers

## Expected Responses

### Success Response Format
```json
{
  "status": "success",
  "data": {
    // Response data varies by endpoint
  }
}
```

### Error Response Format
```json
{
  "error": "Error description"
}
```

## Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (missing required parameters)
- `404` - Not Found
- `500` - Internal Server Error

## Troubleshooting

### Server Not Running
```bash
# Start the server
python src/app.py
```

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Check if Gemma3 is available
ollama list
```

### YouTube API Issues
- Ensure `YOUTUBE_API_KEY` is set in environment
- Check API quota limits
- Verify video ID format

### CORS Issues (Frontend)
The API has CORS enabled for all origins, but if you encounter issues:
```bash
# Test CORS headers
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS http://localhost:8000/api/analyze
```

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test health endpoint
ab -n 100 -c 10 http://localhost:8000/health

# Test analytics endpoint
ab -n 50 -c 5 -p test_payload.json -T application/json http://localhost:8000/api/analytics
```

### Test Payload File (test_payload.json)
```json
{
  "video_id": "dQw4w9WgXcQ"
}
```

## Monitoring

### Check Server Logs
```bash
# If running with Python
python src/app.py 2>&1 | tee server.log

# Monitor logs in real-time
tail -f server.log
```

### Health Monitoring
```bash
# Continuous health check
watch -n 5 'curl -s http://localhost:8000/health | jq .'
```

## Advanced Testing

### Custom Test Scenarios
```python
# Test with custom video IDs
custom_videos = [
    "your_video_id_1",
    "your_video_id_2",
    "your_video_id_3"
]

for video_id in custom_videos:
    result = analyze_video(video_id)
    print(f"Video {video_id}: {result.get('status', 'unknown')}")
```

### Batch Testing
```bash
# Test multiple videos in parallel
for video_id in "dQw4w9WgXcQ" "9bZkp7q19f0" "kJQP7kiw5Fk"; do
    curl -X POST http://localhost:8000/api/analytics \
      -H "Content-Type: application/json" \
      -d "{\"video_id\": \"$video_id\"}" &
done
wait
```

## Task Management System

The API now includes a task management system to handle long-running operations like content generation. This prevents request timeouts and allows for better user experience.

### How It Works

1. **Immediate Response**: When you request content generation, the API immediately returns a task ID
2. **Background Processing**: Content generation runs in the background
3. **Status Checking**: Use the task ID to check progress and get results
4. **Automatic Cleanup**: Old tasks are automatically cleaned up after 24 hours

### Task Status Types

- `processing`: Task is currently running
- `completed`: Task finished successfully with results
- `failed`: Task encountered an error

### Example Workflow

```bash
# 1. Start content generation
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "social_post"
  }'

# Response:
{
  "task_id": "task_1234567890_dQw4w9WgXcQ",
  "status": "processing",
  "message": "Content generation started. Use /api/task/{task_id} to check status.",
  "video_id": "dQw4w9WgXcQ"
}

# 2. Check status
curl http://localhost:8000/api/task/task_1234567890_dQw4w9WgXcQ

# Response (processing):
{
  "task_id": "task_1234567890_dQw4w9WgXcQ",
  "status": "processing",
  "message": "Content generation in progress...",
  "metadata": {
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "social_post",
    "started_at": 1234567890,
    "duration": 15.5
  }
}

# Response (completed):
{
  "task_id": "task_1234567890_dQw4w9WgXcQ",
  "status": "completed",
  "results": {
    "analytics": { ... },
    "content": { ... }
  },
  "metadata": {
    "video_id": "dQw4w9WgXcQ",
    "workflow_steps": ["analytics", "content"],
    "content_type": "social_post",
    "started_at": 1234567890,
    "completed_at": 1234567910,
    "duration": 20.0
  }
}
```

### Task Management Endpoints

- `GET /api/task/{task_id}` - Check task status and get results
- `GET /api/tasks` - List all active and completed tasks
- `POST /api/tasks/cleanup` - Clean up old completed tasks

### Frontend Integration with Tasks

```javascript
// Start content generation
const startContentGeneration = async (videoId) => {
  const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      video_id: videoId,
      workflow_steps: ['analytics', 'content'],
      content_type: 'social_post'
    })
  });
  
  const data = await response.json();
  return data.task_id;
};

// Monitor task progress
const monitorTask = async (taskId, onProgress, onComplete, onError) => {
  const checkStatus = async () => {
    const response = await fetch(`http://localhost:8000/api/task/${taskId}`);
    const data = await response.json();
    
    if (data.status === 'processing') {
      onProgress(data);
      // Check again in 2 seconds
      setTimeout(checkStatus, 2000);
    } else if (data.status === 'completed') {
      onComplete(data);
    } else if (data.status === 'failed') {
      onError(data);
    }
  };
  
  checkStatus();
};

// Usage
const taskId = await startContentGeneration('dQw4w9WgXcQ');
monitorTask(
  taskId,
  (progress) => console.log('Progress:', progress),
  (results) => console.log('Completed:', results),
  (error) => console.error('Failed:', error)
);
```

This comprehensive testing guide covers all aspects of testing the YouTube Analytics AI Backend API. Use the provided test files and individual commands to verify functionality and integrate with your applications. 