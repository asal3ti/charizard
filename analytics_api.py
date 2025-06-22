#!/usr/bin/env python3
"""
Comprehensive YouTube Analytics API
Detailed video metrics, engagement analytics, and performance indicators
"""

import os
import requests
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import ollama
import re

app = Flask(__name__)

# Configuration
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")
OLLAMA_MODEL = "llama2:7b"
DB_NAME = "youtube_analytics.db"

# Initialize services
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
ollama_client = ollama.Client()

def init_db():
    """Initialize comprehensive database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Main analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            title TEXT,
            channel TEXT,
            channel_id TEXT,
            published_at TEXT,
            duration TEXT,
            category TEXT,
            view_count INTEGER,
            like_count INTEGER,
            dislike_count INTEGER,
            comment_count INTEGER,
            engagement_rate REAL,
            like_ratio REAL,
            comment_ratio REAL,
            avg_view_duration REAL,
            retention_rate REAL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Comment analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comment_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            total_comments INTEGER,
            positive_count INTEGER,
            negative_count INTEGER,
            neutral_count INTEGER,
            question_count INTEGER,
            spam_count INTEGER,
            avg_comment_length REAL,
            top_keywords TEXT,
            sentiment_score REAL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES video_analytics (video_id)
        )
    ''')
    
    # Performance metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            views_per_day REAL,
            likes_per_day REAL,
            comments_per_day REAL,
            growth_rate REAL,
            viral_score REAL,
            audience_retention REAL,
            click_through_rate REAL,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES video_analytics (video_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_detailed_video_info(video_id):
    """Get comprehensive video information"""
    try:
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        ).execute()
        
        if not response['items']:
            return None
            
        video = response['items'][0]
        snippet = video['snippet']
        statistics = video['statistics']
        content_details = video['contentDetails']
        
        # Calculate engagement metrics
        view_count = int(statistics.get('viewCount', 0))
        like_count = int(statistics.get('likeCount', 0))
        comment_count = int(statistics.get('commentCount', 0))
        
        engagement_rate = ((like_count + comment_count) / view_count * 100) if view_count > 0 else 0
        like_ratio = (like_count / view_count * 100) if view_count > 0 else 0
        comment_ratio = (comment_count / view_count * 100) if view_count > 0 else 0
        
        # Parse duration
        duration = content_details.get('duration', 'PT0S')
        duration_seconds = parse_duration(duration)
        
        return {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'channel_id': snippet['channelId'],
            'published_at': snippet['publishedAt'],
            'duration': duration,
            'duration_seconds': duration_seconds,
            'category': snippet.get('categoryId'),
            'view_count': view_count,
            'like_count': like_count,
            'dislike_count': int(statistics.get('dislikeCount', 0)),
            'comment_count': comment_count,
            'engagement_rate': round(engagement_rate, 2),
            'like_ratio': round(like_ratio, 2),
            'comment_ratio': round(comment_ratio, 2),
            'tags': snippet.get('tags', []),
            'description': snippet.get('description', '')[:500],
            'thumbnail': snippet['thumbnails']['high']['url']
        }
    except Exception as e:
        return {"error": str(e)}

def parse_duration(duration):
    """Parse ISO 8601 duration to seconds"""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds
    return 0

def get_comprehensive_comments(video_id, max_results=100):
    """Get detailed comment analysis with categorization and overview"""
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            order="relevance"
        ).execute()
        
        if not response['items']:
            return {"total_comments": 0, "comments": []}
        
        comments = []
        positive = negative = neutral = questions = spam = 0
        total_length = 0
        keywords = {}
        
        for item in response['items']:
            comment_data = item['snippet']['topLevelComment']['snippet']
            comment_text = comment_data['textDisplay']
            
            # Sentiment analysis
            sentiment = analyze_sentiment_simple(comment_text)
            if sentiment == "POSITIVE":
                positive += 1
            elif sentiment == "NEGATIVE":
                negative += 1
            else:
                neutral += 1
            
            # Question detection
            if '?' in comment_text:
                questions += 1
            
            # Spam detection
            if is_spam_comment(comment_text):
                spam += 1
            
            # Keyword extraction
            words = re.findall(r'\b\w+\b', comment_text.lower())
            for word in words:
                if len(word) > 3:
                    keywords[word] = keywords.get(word, 0) + 1
            
            total_length += len(comment_text)
            
            comments.append({
                "text": comment_text[:200],
                "author": comment_data['authorDisplayName'],
                "likes": comment_data.get('likeCount', 0),
                "sentiment": sentiment,
                "is_question": '?' in comment_text,
                "is_spam": is_spam_comment(comment_text)
            })
        
        # Calculate basic metrics
        avg_length = total_length / len(comments) if comments else 0
        top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        sentiment_score = (positive - negative) / len(comments) if comments else 0
        
        # Generate comprehensive comment overview
        comment_overview = analyze_comment_overview(comments)
        
        return {
            "total_comments": len(comments),
            "positive_count": positive,
            "negative_count": negative,
            "neutral_count": neutral,
            "question_count": questions,
            "spam_count": spam,
            "avg_comment_length": round(avg_length, 1),
            "top_keywords": [word for word, count in top_keywords],
            "sentiment_score": round(sentiment_score, 3),
            "comments": comments[:20],  # Return first 20 for demo
            "comment_overview": comment_overview  # New comprehensive overview
        }
    except Exception as e:
        return {"error": str(e)}

def analyze_sentiment_simple(text):
    """Simple sentiment analysis using Ollama"""
    try:
        prompt = f"Analyze sentiment of this text. Return only: POSITIVE, NEGATIVE, or NEUTRAL.\n\nText: {text[:300]}\n\nSentiment:"
        response = ollama_client.chat(model=OLLAMA_MODEL, messages=[
            {"role": "user", "content": prompt}
        ])
        result = response['message']['content'].strip().upper()
        if "POSITIVE" in result:
            return "POSITIVE"
        elif "NEGATIVE" in result:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    except:
        return "NEUTRAL"

def is_spam_comment(text):
    """Detect spam comments"""
    spam_indicators = [
        'subscribe', 'like', 'comment', 'check out my channel',
        'follow me', 'watch my video', 'click here', 'free'
    ]
    text_lower = text.lower()
    return any(indicator in text_lower for indicator in spam_indicators)

def calculate_performance_metrics(video_data, comment_data):
    """Calculate performance and growth metrics"""
    try:
        # Basic metrics
        views = video_data.get('view_count', 0)
        likes = video_data.get('like_count', 0)
        comments = video_data.get('comment_count', 0)
        
        # Engagement metrics
        engagement_rate = video_data.get('engagement_rate', 0)
        
        # Viral score (simplified)
        viral_score = (engagement_rate * views) / 1000000
        
        # Growth rate (simplified - would need historical data for real calculation)
        growth_rate = engagement_rate * 0.1  # Simplified
        
        # Audience retention (simplified)
        retention_rate = min(engagement_rate * 2, 100)  # Simplified
        
        return {
            "views_per_day": views / 30,  # Simplified
            "likes_per_day": likes / 30,
            "comments_per_day": comments / 30,
            "growth_rate": round(growth_rate, 2),
            "viral_score": round(viral_score, 2),
            "audience_retention": round(retention_rate, 2),
            "click_through_rate": round(engagement_rate * 0.5, 2)
        }
    except Exception as e:
        return {"error": str(e)}

def save_comprehensive_analytics(video_id, video_data, comment_data, performance_data):
    """Save all analytics to database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Save video analytics
        cursor.execute('''
            INSERT OR REPLACE INTO video_analytics 
            (video_id, title, channel, channel_id, published_at, duration, category,
             view_count, like_count, dislike_count, comment_count, engagement_rate,
             like_ratio, comment_ratio, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_id,
            video_data.get('title'),
            video_data.get('channel'),
            video_data.get('channel_id'),
            video_data.get('published_at'),
            video_data.get('duration'),
            video_data.get('category'),
            video_data.get('view_count'),
            video_data.get('like_count'),
            video_data.get('dislike_count'),
            video_data.get('comment_count'),
            video_data.get('engagement_rate'),
            video_data.get('like_ratio'),
            video_data.get('comment_ratio'),
            datetime.now()
        ))
        
        # Save comment analytics
        cursor.execute('''
            INSERT INTO comment_analytics 
            (video_id, total_comments, positive_count, negative_count, neutral_count,
             question_count, spam_count, avg_comment_length, top_keywords, sentiment_score, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_id,
            comment_data.get('total_comments', 0),
            comment_data.get('positive_count', 0),
            comment_data.get('negative_count', 0),
            comment_data.get('neutral_count', 0),
            comment_data.get('question_count', 0),
            comment_data.get('spam_count', 0),
            comment_data.get('avg_comment_length', 0),
            ','.join(comment_data.get('top_keywords', [])),
            comment_data.get('sentiment_score', 0),
            datetime.now()
        ))
        
        # Save performance metrics
        cursor.execute('''
            INSERT INTO performance_metrics 
            (video_id, views_per_day, likes_per_day, comments_per_day, growth_rate,
             viral_score, audience_retention, click_through_rate, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_id,
            performance_data.get('views_per_day', 0),
            performance_data.get('likes_per_day', 0),
            performance_data.get('comments_per_day', 0),
            performance_data.get('growth_rate', 0),
            performance_data.get('viral_score', 0),
            performance_data.get('audience_retention', 0),
            performance_data.get('click_through_rate', 0),
            datetime.now()
        ))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def categorize_comments(comments):
    """Categorize comments into different types"""
    categories = {
        "appreciation": 0,
        "criticism": 0,
        "questions": 0,
        "suggestions": 0,
        "feedback": 0,
        "spam": 0,
        "humor": 0,
        "technical": 0,
        "personal": 0,
        "other": 0
    }
    
    question_types = {
        "how_to": 0,
        "what_is": 0,
        "when_will": 0,
        "why": 0,
        "where": 0,
        "general": 0
    }
    
    categorized_comments = []
    
    for comment in comments:
        text = comment.get("text", "").lower()
        category = "other"
        
        # Appreciation
        appreciation_words = ['great', 'awesome', 'love', 'amazing', 'perfect', 'excellent', 'fantastic', 'brilliant', 'wonderful', 'outstanding']
        if any(word in text for word in appreciation_words):
            category = "appreciation"
        
        # Criticism
        elif any(word in text for word in ['bad', 'terrible', 'awful', 'hate', 'dislike', 'worst', 'garbage', 'trash', 'boring', 'disappointing']):
            category = "criticism"
        
        # Questions
        elif '?' in text:
            category = "questions"
            question_type = categorize_question(text)
            question_types[question_type] += 1
        
        # Suggestions
        elif any(word in text for word in ['should', 'could', 'would', 'suggest', 'recommend', 'maybe', 'perhaps', 'consider', 'try']):
            category = "suggestions"
        
        # Feedback
        elif any(word in text for word in ['feedback', 'review', 'thought', 'opinion', 'think', 'feel', 'experience']):
            category = "feedback"
        
        # Spam
        elif any(word in text for word in ['subscribe', 'like', 'comment', 'check out my channel', 'follow me', 'watch my video', 'click here', 'free']):
            category = "spam"
        
        # Humor
        elif any(word in text for word in ['lol', 'haha', 'funny', 'joke', 'hilarious', 'comedy', '😂', '🤣', '😄']):
            category = "humor"
        
        # Technical
        elif any(word in text for word in ['how', 'what', 'when', 'where', 'why', 'setup', 'config', 'install', 'error', 'problem', 'solution']):
            category = "technical"
        
        # Personal
        elif any(word in text for word in ['i', 'me', 'my', 'myself', 'personal', 'experience', 'story', 'life']):
            category = "personal"
        
        categories[category] += 1
        
        # Add category to comment
        comment["category"] = category
        if category == "questions":
            comment["question_type"] = categorize_question(text)
        
        categorized_comments.append(comment)
    
    return {
        "categories": categories,
        "question_types": question_types,
        "categorized_comments": categorized_comments
    }

def categorize_question(text):
    """Categorize question types"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['how to', 'how do', 'how can', 'how would']):
        return "how_to"
    elif any(word in text_lower for word in ['what is', 'what are', 'what does', 'what do']):
        return "what_is"
    elif any(word in text_lower for word in ['when will', 'when does', 'when do', 'when is']):
        return "when_will"
    elif any(word in text_lower for word in ['why', 'why is', 'why does', 'why do']):
        return "why"
    elif any(word in text_lower for word in ['where', 'where is', 'where are', 'where can']):
        return "where"
    else:
        return "general"

def analyze_comment_overview(comments):
    """Generate comprehensive comment overview"""
    if not comments:
        return {
            "total_comments": 0,
            "overview": "No comments found",
            "categories": {},
            "questions": {},
            "engagement_insights": {}
        }
    
    # Categorize comments
    categorization = categorize_comments(comments)
    
    # Calculate engagement metrics
    total_likes = sum(c.get("likes", 0) for c in comments)
    avg_likes = total_likes / len(comments) if comments else 0
    
    # Find most engaging comments
    sorted_comments = sorted(comments, key=lambda x: x.get("likes", 0), reverse=True)
    top_comments = sorted_comments[:5]
    
    # Generate insights
    insights = generate_comment_insights(categorization, avg_likes, len(comments))
    
    return {
        "total_comments": len(comments),
        "categories": categorization["categories"],
        "question_types": categorization["question_types"],
        "engagement_metrics": {
            "total_likes": total_likes,
            "average_likes_per_comment": round(avg_likes, 1),
            "most_liked_comment": top_comments[0] if top_comments else None
        },
        "top_comments": top_comments,
        "insights": insights,
        "categorized_comments": categorization["categorized_comments"][:20]  # First 20 for demo
    }

def generate_comment_insights(categorization, avg_likes, total_comments):
    """Generate insights from comment analysis"""
    insights = []
    
    categories = categorization["categories"]
    question_types = categorization["question_types"]
    
    # Category insights
    dominant_category = max(categories.items(), key=lambda x: x[1])
    if dominant_category[1] > total_comments * 0.3:  # More than 30%
        insights.append(f"Comments are predominantly {dominant_category[0]} ({dominant_category[1]} comments)")
    
    # Question insights
    total_questions = question_types["how_to"] + question_types["what_is"] + question_types["when_will"] + question_types["why"] + question_types["where"] + question_types["general"]
    if total_questions > 0:
        most_common_question = max(question_types.items(), key=lambda x: x[1])
        insights.append(f"Most common question type: {most_common_question[0]} ({most_common_question[1]} questions)")
    
    # Engagement insights
    if avg_likes > 10:
        insights.append("High engagement: Comments receive many likes on average")
    elif avg_likes < 2:
        insights.append("Low engagement: Comments receive few likes on average")
    
    # Spam insights
    if categories["spam"] > total_comments * 0.1:  # More than 10%
        insights.append(f"High spam content: {categories['spam']} spam comments detected")
    
    # Sentiment insights
    if categories["appreciation"] > categories["criticism"] * 2:
        insights.append("Very positive community: Appreciation comments significantly outnumber criticism")
    elif categories["criticism"] > categories["appreciation"]:
        insights.append("Critical community: Criticism comments outnumber appreciation")
    
    return insights

@app.route('/')
def home():
    return """
    <h1>📊 Comprehensive YouTube Analytics API</h1>
    <p><strong>Endpoints:</strong></p>
    <ul>
        <li><code>POST /analyze</code> - Full video analytics</li>
        <li><code>GET /metrics</code> - Performance metrics</li>
        <li><code>GET /history</code> - Analysis history</li>
        <li><code>GET /health</code> - Health check</li>
    </ul>
    <p><strong>Example:</strong></p>
    <code>curl -X POST /analyze -H "Content-Type: application/json" -d '{"video_id": "dQw4w9WgXcQ"}'</code>
    """

@app.route('/analyze', methods=['POST'])
def analyze_video():
    """Comprehensive video analysis"""
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        
        if not video_id:
            return jsonify({"error": "Video ID required"}), 400
        
        print(f"🎬 Analyzing video: {video_id}")
        
        # Get comprehensive video data
        video_data = get_detailed_video_info(video_id)
        if not video_data or 'error' in video_data:
            return jsonify({"error": "Could not fetch video data"}), 400
        
        # Get comment analytics
        comment_data = get_comprehensive_comments(video_id)
        
        # Calculate performance metrics
        performance_data = calculate_performance_metrics(video_data, comment_data)
        
        # Save to database
        save_comprehensive_analytics(video_id, video_data, comment_data, performance_data)
        
        result = {
            "video_id": video_id,
            "video_analytics": video_data,
            "comment_analytics": comment_data,
            "performance_metrics": performance_data,
            "analyzed_at": datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/metrics')
def get_metrics():
    """Get performance metrics summary"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_videos,
                AVG(engagement_rate) as avg_engagement,
                AVG(view_count) as avg_views,
                AVG(like_count) as avg_likes,
                SUM(view_count) as total_views
            FROM video_analytics
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                "total_videos_analyzed": result[0],
                "average_engagement_rate": round(result[1] or 0, 2),
                "average_views": int(result[2] or 0),
                "average_likes": int(result[3] or 0),
                "total_views_analyzed": int(result[4] or 0)
            })
        else:
            return jsonify({"message": "No analytics data available"})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/history')
def get_history():
    """Get analysis history with details"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                v.video_id, v.title, v.view_count, v.like_count, v.engagement_rate,
                c.sentiment_score, c.total_comments, v.analyzed_at
            FROM video_analytics v
            LEFT JOIN comment_analytics c ON v.video_id = c.video_id
            ORDER BY v.analyzed_at DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            history.append({
                "video_id": row[0],
                "title": row[1],
                "views": row[2],
                "likes": row[3],
                "engagement_rate": row[4],
                "sentiment_score": row[5],
                "total_comments": row[6],
                "analyzed_at": row[7]
            })
        
        return jsonify({"history": history})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "model": OLLAMA_MODEL,
        "database": "connected",
        "endpoints": ["/analyze", "/metrics", "/history", "/health"]
    })

@app.route('/api/channel/<channel_id>', methods=['GET'])
def channel_analytics(channel_id):
    """Get comprehensive channel analytics"""
    try:
        result = get_channel_analytics(channel_id)
        
        # Store in database
        if 'error' not in result:
            store_channel_analytics(channel_id, result)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/channel/compare', methods=['POST'])
def compare_channels():
    """Compare multiple channels"""
    try:
        data = request.get_json()
        channel_ids = data.get('channel_ids', [])
        
        if not channel_ids:
            return jsonify({"error": "No channel IDs provided"}), 400
        
        result = get_channel_comparison(channel_ids)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_channel_analytics(channel_id):
    """Get comprehensive channel analytics"""
    try:
        # Get channel info
        channel_response = youtube.channels().list(
            part="snippet,statistics,brandingSettings",
            id=channel_id
        ).execute()
        
        if not channel_response['items']:
            return {"error": "Channel not found"}
        
        channel = channel_response['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']
        
        # Get recent videos for analysis
        videos_response = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=50
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in videos_response['items']]
        
        # Get detailed video stats
        videos_analytics = []
        total_views = 0
        total_likes = 0
        total_comments = 0
        
        for video_id in video_ids[:20]:  # Analyze first 20 videos
            video_stats = get_detailed_video_info(video_id)
            if video_stats and 'error' not in video_stats:
                views = int(video_stats.get('view_count', 0))
                likes = int(video_stats.get('like_count', 0))
                comments = int(video_stats.get('comment_count', 0))
                engagement_rate = float(video_stats.get('engagement_rate', 0))
                
                videos_analytics.append({
                    "video_id": video_id,
                    "title": video_stats.get('title', ''),
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "engagement_rate": engagement_rate,
                    "published_at": video_stats.get('published_at', '')
                })
                total_views += views
                total_likes += likes
                total_comments += comments
        
        # Calculate channel metrics
        subscriber_count = int(statistics.get('subscriberCount', 0))
        video_count = int(statistics.get('videoCount', 0))
        view_count = int(statistics.get('viewCount', 0))
        
        avg_views_per_video = total_views / len(videos_analytics) if videos_analytics else 0
        avg_likes_per_video = total_likes / len(videos_analytics) if videos_analytics else 0
        avg_comments_per_video = total_comments / len(videos_analytics) if videos_analytics else 0
        
        # Engagement metrics
        total_engagement = total_likes + total_comments
        channel_engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0
        
        # Growth metrics (simplified)
        views_per_subscriber = view_count / subscriber_count if subscriber_count > 0 else 0
        videos_per_month = video_count / 12  # Simplified calculation
        
        # Performance analysis
        performance_analysis = analyze_channel_performance(videos_analytics)
        
        return {
            "channel_info": {
                "id": channel_id,
                "title": snippet['title'],
                "description": snippet.get('description', '')[:500],
                "custom_url": snippet.get('customUrl'),
                "published_at": snippet['publishedAt'],
                "country": snippet.get('country'),
                "default_language": snippet.get('defaultLanguage'),
                "thumbnail": snippet['thumbnails']['high']['url']
            },
            "statistics": {
                "subscriber_count": subscriber_count,
                "video_count": video_count,
                "view_count": view_count,
                "total_views": total_views,
                "total_likes": total_likes,
                "total_comments": total_comments
            },
            "metrics": {
                "avg_views_per_video": round(avg_views_per_video, 0),
                "avg_likes_per_video": round(avg_likes_per_video, 0),
                "avg_comments_per_video": round(avg_comments_per_video, 0),
                "channel_engagement_rate": round(channel_engagement_rate, 2),
                "views_per_subscriber": round(views_per_subscriber, 2),
                "videos_per_month": round(videos_per_month, 1)
            },
            "performance_analysis": performance_analysis,
            "recent_videos": videos_analytics[:10]  # Top 10 recent videos
        }
        
    except Exception as e:
        return {"error": str(e)}

def analyze_channel_performance(videos_analytics):
    """Analyze channel performance patterns"""
    if not videos_analytics:
        return {"insights": ["No video data available"]}
    
    insights = []
    
    # Sort videos by different metrics
    by_views = sorted(videos_analytics, key=lambda x: x['views'], reverse=True)
    by_engagement = sorted(videos_analytics, key=lambda x: x['engagement_rate'], reverse=True)
    by_likes = sorted(videos_analytics, key=lambda x: x['likes'], reverse=True)
    
    # Top performing videos
    top_viewed = by_views[0] if by_views else None
    top_engaged = by_engagement[0] if by_engagement else None
    
    if top_viewed:
        insights.append(f"Most viewed video: '{top_viewed['title'][:50]}...' ({top_viewed['views']:,} views)")
    
    if top_engaged:
        insights.append(f"Highest engagement: '{top_engaged['title'][:50]}...' ({top_engaged['engagement_rate']}% engagement)")
    
    # Performance patterns
    avg_engagement = sum(v['engagement_rate'] for v in videos_analytics) / len(videos_analytics)
    if avg_engagement > 5:
        insights.append("High average engagement rate across videos")
    elif avg_engagement < 1:
        insights.append("Low average engagement rate - consider content strategy")
    
    # Consistency analysis
    view_counts = [v['views'] for v in videos_analytics]
    view_variance = max(view_counts) / min(view_counts) if min(view_counts) > 0 else 0
    
    if view_variance > 10:
        insights.append("High view variance - content performance is inconsistent")
    else:
        insights.append("Consistent view performance across videos")
    
    # Growth indicators
    recent_videos = videos_analytics[:5]
    older_videos = videos_analytics[-5:] if len(videos_analytics) >= 10 else []
    
    if recent_videos and older_videos:
        recent_avg_views = sum(v['views'] for v in recent_videos) / len(recent_videos)
        older_avg_views = sum(v['views'] for v in older_videos) / len(older_videos)
        
        if recent_avg_views > older_avg_views * 1.5:
            insights.append("Growing channel: Recent videos perform significantly better")
        elif recent_avg_views < older_avg_views * 0.7:
            insights.append("Declining performance: Recent videos underperform compared to older content")
    
    return {"insights": insights}

def get_channel_comparison(channel_ids):
    """Compare multiple channels"""
    comparison = {}
    
    for channel_id in channel_ids:
        channel_data = get_channel_analytics(channel_id)
        if 'error' not in channel_data and isinstance(channel_data, dict):
            channel_info = channel_data.get('channel_info', {})
            statistics = channel_data.get('statistics', {})
            metrics = channel_data.get('metrics', {})
            
            comparison[channel_id] = {
                "title": channel_info.get('title', ''),
                "subscribers": statistics.get('subscriber_count', 0),
                "total_views": statistics.get('view_count', 0),
                "engagement_rate": metrics.get('channel_engagement_rate', 0),
                "avg_views_per_video": metrics.get('avg_views_per_video', 0)
            }
    
    return comparison

def store_channel_analytics(channel_id, data):
    """Store channel analytics in database"""
    try:
        conn = sqlite3.connect('analytics.db')
        cursor = conn.cursor()
        
        # Create channel analytics table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channel_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT,
                title TEXT,
                subscriber_count INTEGER,
                video_count INTEGER,
                view_count INTEGER,
                engagement_rate REAL,
                avg_views_per_video REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert channel data
        cursor.execute('''
            INSERT INTO channel_analytics 
            (channel_id, title, subscriber_count, video_count, view_count, engagement_rate, avg_views_per_video)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            channel_id,
            data['channel_info']['title'],
            data['statistics']['subscriber_count'],
            data['statistics']['video_count'],
            data['statistics']['view_count'],
            data['metrics']['channel_engagement_rate'],
            data['metrics']['avg_views_per_video']
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error storing channel analytics: {e}")

if __name__ == '__main__':
    print("📊 Starting Comprehensive YouTube Analytics API")
    print(f"🤖 Using Ollama model: {OLLAMA_MODEL}")
    print("📈 Features: Video metrics, engagement analytics, comment analysis, performance tracking")
    print("🌐 Server: http://localhost:8000")
    
    # Initialize database
    init_db()
    
    app.run(host='0.0.0.0', port=8000, debug=True) 