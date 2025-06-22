# YouTube Analytics AI System

A comprehensive AI-powered YouTube analytics backend API that uses multiple AI agents to analyze YouTube videos, extract insights, and generate content. Built with Flask, LangChain, and OpenAI for production-ready AI processing.

## Features

### 🤖 AI Agents
- **Analytics Agent**: Analyzes video performance, comments, and transcripts
- **Critique Agent**: Reviews and improves outputs using ReAct methodology
- **Content Agent**: Generates social media posts and images
- **Orchestrator Agent**: Coordinates all agents and manages workflows

### 📊 Analytics Capabilities
- Video performance metrics and engagement analysis
- Comment sentiment analysis with sarcasm detection
- Comment categorization (questions, feedback, appreciation, etc.)
- Video transcript analysis and topic extraction
- Channel-level analytics
- Multi-video comparison

### 🎯 Enhanced Comment Analysis (NEW!)
- **Advanced Sentiment Analysis**: VADER sentiment analysis with sarcasm detection
- **Language Detection**: Automatic English comment filtering
- **Tagged Insights**: 5-category insights (High Impact, Medium Impact, Content, Sponsorship, Comment Sentiment)
- **Community Health Assessment**: Overall community sentiment and engagement quality
- **Content Performance Metrics**: Engagement rates, comment ratios, and performance scoring
- **Priority Recommendations**: Actionable insights ranked by impact
- **Benchmark Comparisons**: Industry standard comparisons for engagement and sentiment
- **Enhanced Metrics**: Sentiment scores, community health scores, and performance assessments

### 🎯 Enhanced Insights (NEW!)
- **Content Performance Prediction**: Predict how well a video will perform
- **Audience Behavior Analysis**: Identify influencers, engagement patterns, topic clusters
- **Content Optimization Suggestions**: Title, thumbnail, tag, and SEO improvements
- **Content Gap Analysis**: Find underserved topics in your niche
- **Trend Analysis**: Identify trending topics and content patterns
- **Competitor Analysis**: Compare performance against competitors
- **Market Position Analysis**: Understand your competitive position

### 🎨 Content Generation
- AI-generated social media posts for multiple platforms
- Platform-optimized content (Twitter, Instagram, LinkedIn, Facebook)
- Hashtag optimization
- Image generation for posts
- Content critique and improvement

### 🔍 Advanced Features
- ReAct methodology for quality assurance
- Asynchronous processing
- Workflow tracking and history
- Real-time status monitoring
- Comprehensive error handling

## Prerequisites

- Python 3.8+
- OpenAI API key (for production)
- YouTube Data API v3 key
- Optional: Ollama for local development

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd charizard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

## Configuration

Create a `.env` file with the following variables:

```env
# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here

# OpenAI Configuration (Primary for production)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Ollama Configuration (Fallback for development)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3

# Flask Configuration
PORT=5000
FLASK_ENV=production
FLASK_DEBUG=False

# Logging Configuration
LOG_LEVEL=INFO

# Database Configuration (if needed)
DATABASE_URL=sqlite:///analytics.db
```

### Getting API Keys

#### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the API key to your `.env` file

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Add the API key to your `.env` file

## Usage

### Starting the Server

```bash
python src/app.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Enhanced Video Analysis (NEW!)
```bash
POST /api/analyze
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response includes:**
- Video metadata (title, channel, views, likes, comments)
- Sentiment analysis with sarcasm detection
- Tagged insights (5 categories with actionable recommendations)
- Additional metrics (engagement rate, sentiment score, community health)
- Priority recommendations ranked by impact
- Benchmark comparisons against industry standards

#### Video ID Extraction
```bash
POST /api/extract-video-id
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

#### Routes Listing
```bash
GET /routes
```

#### Basic Analytics
```bash
POST /api/analytics
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ"
}
```

#### Enhanced Insights (NEW!)
```bash
POST /api/video/enhanced-insights
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ"
}
```

#### Content Gap Analysis
```bash
POST /api/content-gap-analysis
Content-Type: application/json

{
  "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "niche_keywords": ["python", "programming", "tutorial"]
}
```

#### Trend Analysis
```bash
POST /api/trend-analysis
Content-Type: application/json

{
  "keywords": ["artificial intelligence", "machine learning", "AI"]
}
```

#### Competitor Analysis
```bash
POST /api/competitor-analysis
Content-Type: application/json

{
  "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "competitor_channels": ["UC8butISFwT-Wl7EV0hUK0BQ", "UCWv7vMbMWH4-V0ZXdmDpPBA"]
}
```

#### Comprehensive Insights Summary
```bash
POST /api/insights/summary
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ"
}
```

#### Comments Analysis
```bash
POST /api/comments
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ"
}
```

#### Channel Analytics
```bash
GET /api/channel/{channel_id}
```

#### Technical Insights
```bash
POST /api/video/technical-insights
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ",
  "max_results": 5
}
```

## Architecture

### Agent System
```