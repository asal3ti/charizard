# YouTube Analytics API Documentation

A comprehensive API for YouTube video and channel analytics using Python Flask, Google YouTube API, and Ollama LLM.

## Features

- **Video Analytics**: Detailed metrics, engagement analysis, and performance indicators
- **Comment Analysis**: Sentiment analysis, categorization, question detection, and spam filtering
- **Channel Analytics**: Comprehensive channel statistics, performance analysis, and growth metrics
- **Performance Metrics**: Growth rate, viral score, audience retention, and more
- **SQLite Storage**: Persistent storage of analytics data
- **Lightweight LLM**: Uses Ollama with llama2:7b model for AI analysis

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export YOUTUBE_API_KEY="your_youtube_api_key"
   ```

3. **Start Ollama**:
   ```bash
   ollama pull llama2:7b
   ollama serve
   ```

4. **Run the API**:
   ```bash
   python analytics_api.py
   ```

## API Endpoints

### 1. Health Check
**GET** `/health`
Returns service status and version information.

### 2. Video Analytics
**POST** `/api/analytics`
Analyzes a YouTube video for engagement metrics, comments, and sentiment.

### 3. Comment Analytics
**POST** `/api/comments`
Analyzes comments from a YouTube video with sentiment analysis and categorization.

### 4. Video Comparison by Keywords
**POST** `/api/video/compare`
Compares a video with similar videos based on keywords/tags, excluding videos from the same channel.

**Request Body:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "max_results": 5
}
```

**Response:**
```json
{
  "original_video": {
    "video_id": "dQw4w9WgXcQ",
    "title": "Original Video Title",
    "channel": "Original Channel",
    "channel_id": "UC...",
    "view_count": 1000000,
    "like_count": 50000,
    "comment_count": 2000,
    "tags": ["tag1", "tag2", "tag3"]
  },
  "search_keywords": "video title tag1 tag2 tag3",
  "similar_videos": [
    {
      "video_id": "similar_video_id",
      "title": "Similar Video Title",
      "channel": "Different Channel",
      "channel_id": "UC...",
      "published_at": "2024-01-01T00:00:00Z",
      "view_count": 800000,
      "like_count": 40000,
      "comment_count": 1500,
      "engagement_rate": 5.0,
      "duration": "PT10M30S",
      "tags": ["tag1", "tag2"],
      "transcript_length": 1500,
      "sponsorship_analysis": {
        "has_sponsorship": true,
        "sponsorship_level": "medium",
        "confidence_score": 65,
        "detected_companies": ["nordvpn", "skillshare"]
      },
      "thumbnail": "https://..."
    }
  ],
  "total_found": 5,
  "excluded_same_channel": true,
  "sponsorship_summary": {
    "total_videos": 5,
    "sponsored_videos": 3,
    "sponsorship_rate": 60.0,
    "sponsorship_levels": {
      "high": 1,
      "medium": 2,
      "low": 0,
      "none": 2
    },
    "top_sponsors": [
      ["nordvpn", 2],
      ["skillshare", 1]
    ]
  }
}
```

**Features:**
- ✅ **Channel Exclusion**: Automatically excludes videos from the same channel as the original video
- ✅ **Channel Name Filtering**: Removes channel names from search keywords to avoid bias
- ✅ **Sponsorship Analysis**: Analyzes each similar video for sponsorship content
- ✅ **Engagement Metrics**: Calculates engagement rates and performance metrics
- ✅ **Transcript Analysis**: Analyzes video transcripts for sponsorship detection

### 5. Video Sponsorship Analysis
**POST** `/api/sponsorship`
Analyzes a specific video for sponsorship content and patterns.

### 6. Sponsored Video Search
**POST** `/api/search-sponsored`
Searches for videos with specific keywords and analyzes their sponsorship patterns.

### 7. Channel Analytics
**POST** `/api/channel`
Analyzes a YouTube channel's performance and metrics.

### 8. Channel Comparison
**POST** `/api/compare-channels`
Compares multiple YouTube channels.

### 9. Channel Metrics
**GET** `/api/channel-metrics`
Gets aggregated channel performance metrics.

### 10. Analysis History
**GET** `/api/history`
Retrieves analysis history and previous results.

### 11. Task Management
**POST** `/api/analyze`
Creates background tasks for comprehensive analysis.

**GET** `/api/task/{task_id}`
Checks task status and retrieves results.

**GET** `/api/tasks`
Lists all active tasks.

**POST** `/api/tasks/cleanup`
Cleans up old completed tasks.

## Response Examples

### Video Analytics Response
```json
{
  "title": "Video Title",
  "channel": "Channel Name",
  "view_count": 1000000,
  "like_count": 50000,
  "comment_count": 2000,
  "engagement_rate": 7.0,
  "like_ratio": 5.0,
  "comment_ratio": 0.2,
  "performance_metrics": {
    "views_per_day": 10000,
    "growth_rate": 15.5,
    "viral_score": 8.2,
    "audience_retention": 75.0
  },
  "comment_analytics": {
    "total_comments": 2000,
    "positive_count": 1200,
    "negative_count": 200,
    "neutral_count": 600,
    "question_count": 150,
    "spam_count": 50,
    "sentiment_score": 0.75,
    "categorization": {
      "appreciation": 800,
      "criticism": 150,
      "questions": 150,
      "suggestions": 100,
      "spam": 50,
      "humor": 200,
      "technical": 100,
      "personal": 100,
      "other": 350
    },
    "question_types": {
      "how-to": 45,
      "what-is": 30,
      "when-will": 20,
      "why": 25,
      "where": 10,
      "general": 20
    },
    "overview": {
      "insights": [
        "High engagement with positive sentiment",
        "Many technical questions indicate educational content",
        "Good balance of appreciation and constructive feedback"
      ]
    }
  }
}
```

### Channel Analytics Response
```json
{
  "channel_info": {
    "id": "UCX6OQ3DkcsbYNE6H8uQQuVA",
    "title": "Channel Name",
    "description": "Channel description...",
    "published_at": "2010-01-01T00:00:00Z",
    "country": "US",
    "thumbnail": "https://..."
  },
  "statistics": {
    "subscriber_count": 10000000,
    "video_count": 500,
    "view_count": 5000000000,
    "total_views": 100000000,
    "total_likes": 5000000,
    "total_comments": 200000
  },
  "metrics": {
    "avg_views_per_video": 200000,
    "avg_likes_per_video": 10000,
    "avg_comments_per_video": 400,
    "channel_engagement_rate": 5.2,
    "views_per_subscriber": 500,
    "videos_per_month": 2.5
  },
  "performance_analysis": {
    "insights": [
      "High average engagement rate across videos",
      "Consistent view performance across videos",
      "Growing channel: Recent videos perform significantly better"
    ]
  },
  "recent_videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Recent Video Title",
      "views": 250000,
      "likes": 12000,
      "comments": 500,
      "engagement_rate": 5.0,
      "published_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Channel Comparison Response
```json
{
  "UCX6OQ3DkcsbYNE6H8uQQuVA": {
    "title": "Channel 1",
    "subscribers": 10000000,
    "total_views": 5000000000,
    "engagement_rate": 5.2,
    "avg_views_per_video": 200000
  },
  "UC-lHJZR3Gqxm24_Vd_AJ5Yw": {
    "title": "Channel 2",
    "subscribers": 8000000,
    "total_views": 4000000000,
    "engagement_rate": 4.8,
    "avg_views_per_video": 180000
  }
}
```

## Database Schema

### Video Analytics Table
- `video_id`: Unique video identifier
- `title`, `channel`, `channel_id`: Basic video info
- `view_count`, `like_count`, `comment_count`: Engagement metrics
- `engagement_rate`, `like_ratio`, `comment_ratio`: Calculated metrics
- `analyzed_at`: Timestamp of analysis

### Comment Analytics Table
- `video_id`: Reference to video
- `total_comments`, `positive_count`, `negative_count`, `neutral_count`: Sentiment breakdown
- `question_count`, `spam_count`: Content categorization
- `sentiment_score`: Overall sentiment score
- `top_keywords`: Most common keywords

### Performance Metrics Table
- `video_id`: Reference to video
- `views_per_day`, `likes_per_day`, `comments_per_day`: Daily metrics
- `growth_rate`, `viral_score`: Performance indicators
- `audience_retention`, `click_through_rate`: Advanced metrics

### Channel Analytics Table
- `channel_id`: Unique channel identifier
- `title`: Channel name
- `subscriber_count`, `video_count`, `view_count`: Channel statistics
- `engagement_rate`, `avg_views_per_video`: Calculated metrics
- `created_at`: Timestamp of analysis

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing parameters)
- `404`: Resource not found
- `500`: Internal server error

Error responses include a descriptive message:
```json
{
  "error": "Video not found or API key invalid"
}
```

## Rate Limiting

- YouTube API has daily quotas (typically 10,000 units/day)
- Each video analysis uses ~100-200 quota units
- Channel analysis uses ~50-100 quota units per channel
- Monitor your quota usage in Google Cloud Console

## Testing

### Python Test Script
```bash
python test_analytics.py
```

### cURL Test Script
```bash
chmod +x test_curl.sh
./test_curl.sh
```

### JavaScript Test Script
```bash
node test_api.js
```

## Configuration

### Environment Variables
- `YOUTUBE_API_KEY`: Your YouTube Data API v3 key
- `OLLAMA_MODEL`: Ollama model to use (default: llama2:7b)
- `DB_NAME`: Database filename (default: youtube_analytics.db)

### API Configuration
- **Port**: 8000 (configurable in analytics_api.py)
- **Host**: localhost (configurable)
- **CORS**: Enabled for cross-origin requests
- **JSON**: All responses are in JSON format

## Performance Considerations

- **Video Analysis**: ~5-10 seconds per video (depending on comment count)
- **Channel Analysis**: ~30-60 seconds per channel (analyzes recent videos)
- **Database**: SQLite for simplicity, consider PostgreSQL for production
- **Caching**: No built-in caching, implement Redis for production use

## Security

- API key should be kept secure
- No authentication built-in (add for production)
- Input validation on all endpoints
- SQL injection protection via parameterized queries

## Troubleshooting

### Common Issues

1. **YouTube API Quota Exceeded**:
   - Check quota usage in Google Cloud Console
   - Implement caching for repeated requests

2. **Ollama Connection Error**:
   - Ensure Ollama is running: `