# YouTube Analytics AI System

A comprehensive AI-powered YouTube analytics backend API that uses multiple AI agents to analyze YouTube videos, extract insights, and generate content. Built with Flask, LangChain, and Ollama for local LLM processing using the Gemma3 model.

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
- Ollama installed and running locally
- YouTube Data API v3 key
- macOS (for Ollama compatibility)

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

4. **Install Ollama**
   ```bash
   # On macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama
   ollama serve
   ```

5. **Download Gemma3 model**
   ```bash
   ollama pull gemma3
   ```

6. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

## Configuration

Create a `.env` file with the following variables:

```env
# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3

# Flask Configuration
PORT=5000
FLASK_ENV=development
FLASK_DEBUG=True

# Logging Configuration
LOG_LEVEL=INFO

# Optional: OpenAI API Key (for DALL-E image generation)
OPENAI_API_KEY=your_openai_api_key_here
```

### Getting YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the API key to your `.env` file

## Usage

### Starting the Server

```bash
python src/app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### Health Check
```bash
GET /api/health
```

#### Full Video Analysis
```bash
POST /api/analyze
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "generate_content": true,
  "critique_results": true
}
```

#### Get Analytics Only
```bash
POST /api/analytics
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

#### Get Comments Analysis
```bash
POST /api/comments
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "max_results": 500
}
```

#### Get Video Transcript
```bash
POST /api/transcript
Content-Type: application/json

{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

#### Analyze Channel
```bash
POST /api/channel
Content-Type: application/json

{
  "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw"
}
```

#### Compare Multiple Videos
```bash
POST /api/compare
Content-Type: application/json

{
  "video_urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=9bZkp7q19f0"
  ]
}
```

#### Workflow Status
```bash
GET /api/workflow/status/{workflow_id}
GET /api/workflow/current
GET /api/workflow/history
```

#### Agent Capabilities
```bash
GET /api/agents/capabilities
```

## Example Responses

### Full Analysis Response
```json
{
  "workflow_id": "workflow_20231201_143022_dQw4w9WgXcQ",
  "video_id": "dQw4w9WgXcQ",
  "start_time": "2023-12-01T14:30:22",
  "steps": [
    {
      "step": "analytics",
      "status": "completed",
      "result": {
        "video_id": "dQw4w9WgXcQ",
        "analytics": {
          "performance_metrics": {
            "engagement_rate": 0.045,
            "sentiment_score": 0.72,
            "comment_quality_score": 0.85
          },
          "insights": {
            "top_topics": ["music", "entertainment", "viral"],
            "audience_reaction": "Very positive",
            "content_strengths": ["catchy", "memorable"],
            "improvement_areas": ["length", "repetition"]
          },
          "recommendations": [
            "Consider shorter format for better retention",
            "Add more variety in content"
          ]
        },
        "visualizations": {
          "sentiment_distribution": "base64_chart_data",
          "comment_categories": "base64_chart_data"
        }
      }
    },
    {
      "step": "content_generation",
      "status": "completed",
      "result": {
        "engagement_post": {
          "base_content": {
            "title": "Viral Success Analysis",
            "content": "This video achieved incredible engagement...",
            "hashtags": ["#YouTube", "#Viral", "#Analytics"],
            "call_to_action": "Check out the full analysis!"
          },
          "platform_variations": {
            "twitter": {
              "content": "Shortened version for Twitter...",
              "hashtags": ["#YouTube", "#Viral"]
            }
          }
        },
        "images": {
          "engagement_post_image": "base64_image_data"
        }
      }
    }
  ],
  "end_time": "2023-12-01T14:32:15",
  "status": "completed",
  "summary": {
    "total_steps": 4,
    "completed_steps": 4,
    "key_insights": ["music", "entertainment", "viral"],
    "recommendations": ["Consider shorter format", "Add more variety"]
  }
}
```

## Architecture

### Agent System
```
OrchestratorAgent
├── AnalyticsAgent
│   ├── Video Analysis
│   ├── Comment Analysis
│   └── Transcript Analysis
├── CritiqueAgent
│   ├── Quality Assurance
│   ├── ReAct Methodology
│   └── Output Improvement
└── ContentAgent
    ├── Social Media Posts
    ├── Image Generation
    └── Platform Optimization
```

### Data Flow
1. **Input**: YouTube URL or Video ID
2. **Orchestrator**: Coordinates workflow
3. **Analytics**: Extracts video data, comments, transcript
4. **Critique**: Reviews and improves analytics
5. **Content**: Generates social media content
6. **Critique**: Reviews and improves content
7. **Output**: Comprehensive analysis with generated content

## Development

### Project Structure
```
charizard/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── analytics_agent.py
│   │   ├── critique_agent.py
│   │   ├── content_agent.py
│   │   └── orchestrator_agent.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── youtube_service.py
│   ├── app.py
│   └── main.py
├── requirements.txt
├── env.example
└── README.md
```

### Adding New Agents

1. Create new agent class inheriting from `BaseAgent`
2. Implement required methods: `process()`, `get_capabilities()`
3. Add to orchestrator agent
4. Update API endpoints if needed

### Customizing LLM

The system uses Ollama with Gemma3 for local LLM processing. You can:

1. Change the model in `.env`:
   ```env
   OLLAMA_MODEL=gemma3
   ```

2. Download different models:
   ```bash
   ollama pull gemma3
   ollama pull llama2
   ollama pull mistral
   ollama pull codellama
   ```

## Troubleshooting

### Common Issues

1. **Ollama not running**
   ```bash
   ollama serve
   ```

2. **Gemma3 model not found**
   ```bash
   ollama pull gemma3
   ```

3. **YouTube API quota exceeded**
   - Check your quota in Google Cloud Console
   - Consider implementing caching

4. **Comments disabled**
   - Some videos have comments disabled
   - Check video settings

### Logs

Check logs for detailed error information:
```bash
tail -f logs/app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## Roadmap

- [ ] Real-time analytics dashboard
- [ ] Advanced image generation with DALL-E
- [ ] Multi-language support
- [ ] Batch processing for multiple videos
- [ ] Export functionality (PDF, CSV)
- [ ] Webhook notifications
- [ ] Rate limiting and caching
- [ ] Docker containerization