#!/usr/bin/env python3
"""
Simple YouTube Analytics - Command Line Tool with Database
Usage: python youtube_analytics.py VIDEO_ID
       python youtube_analytics.py --history
       python youtube_analytics.py --progress
"""

import sys
import os
import sqlite3
from datetime import datetime
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DB_NAME = "youtube_analytics.db"

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            title TEXT,
            channel TEXT,
            views INTEGER,
            likes INTEGER,
            comments INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sentiment table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            positive_count INTEGER,
            negative_count INTEGER,
            neutral_count INTEGER,
            total_comments INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos (video_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_to_database(video_id, video_data, sentiment_data):
    """Save analytics results to database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Save video data
        cursor.execute('''
            INSERT OR REPLACE INTO videos 
            (video_id, title, channel, views, likes, comments, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_id,
            video_data.get('title'),
            video_data.get('channel'),
            video_data.get('views'),
            video_data.get('likes'),
            video_data.get('comments'),
            datetime.now()
        ))
        
        # Save sentiment data
        cursor.execute('''
            INSERT INTO sentiment 
            (video_id, positive_count, negative_count, neutral_count, total_comments, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            video_id,
            sentiment_data.get('positive', 0),
            sentiment_data.get('negative', 0),
            sentiment_data.get('neutral', 0),
            sentiment_data.get('total', 0),
            datetime.now()
        ))
        
        conn.commit()
        print("💾 Saved to database")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

def show_history():
    """Show analysis history"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT v.video_id, v.title, v.views, v.likes, v.analyzed_at,
               s.positive_count, s.negative_count, s.neutral_count
        FROM videos v
        LEFT JOIN sentiment s ON v.video_id = s.video_id
        ORDER BY v.analyzed_at DESC
        LIMIT 10
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("📚 No analysis history found")
        return
    
    print("📚 Recent Analysis History:")
    print("=" * 80)
    print(f"{'Video ID':<12} {'Title':<30} {'Views':<10} {'Likes':<8} {'Sentiment':<15} {'Date':<20}")
    print("-" * 80)
    
    for row in results:
        video_id, title, views, likes, date, pos, neg, neu = row
        title_short = title[:27] + "..." if len(title) > 30 else title
        sentiment = f"{pos}+/{neg}-/{neu}~" if pos is not None else "N/A"
        date_str = date.split()[0] if date else "N/A"
        
        print(f"{video_id:<12} {title_short:<30} {views:<10,} {likes:<8,} {sentiment:<15} {date_str:<20}")

def show_progress():
    """Show current progress and stats"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Total videos analyzed
    cursor.execute("SELECT COUNT(*) FROM videos")
    total_videos = cursor.fetchone()[0]
    
    # Total comments analyzed
    cursor.execute("SELECT SUM(total_comments) FROM sentiment")
    total_comments = cursor.fetchone()[0] or 0
    
    # Average sentiment
    cursor.execute('''
        SELECT AVG(positive_count), AVG(negative_count), AVG(neutral_count)
        FROM sentiment
    ''')
    avg_sentiment = cursor.fetchone()
    
    conn.close()
    
    print("📊 Analysis Progress:")
    print("=" * 40)
    print(f"🎬 Videos analyzed: {total_videos}")
    print(f"💬 Comments analyzed: {total_comments:,}")
    if avg_sentiment[0]:
        print(f"😊 Avg positive: {avg_sentiment[0]:.1f}")
        print(f"😞 Avg negative: {avg_sentiment[1]:.1f}")
        print(f"😐 Avg neutral: {avg_sentiment[2]:.1f}")

def analyze_video(video_id):
    """Analyze a YouTube video and show stats"""
    
    # Setup
    api_key = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)
    sia = SentimentIntensityAnalyzer()
    
    print(f"🎬 Analyzing video: {video_id}")
    print("=" * 50)
    
    video_data = {}
    sentiment_data = {}
    
    # Get video info
    try:
        video_response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()
        
        if not video_response['items']:
            print("❌ Video not found!")
            return
        
        video = video_response['items'][0]
        snippet = video['snippet']
        stats = video['statistics']
        
        video_data = {
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'views': int(stats.get('viewCount', 0)),
            'likes': int(stats.get('likeCount', 0)),
            'comments': int(stats.get('commentCount', 0))
        }
        
        print(f"📺 Title: {video_data['title']}")
        print(f"👤 Channel: {video_data['channel']}")
        print(f"👀 Views: {video_data['views']:,}")
        print(f"👍 Likes: {video_data['likes']:,}")
        print(f"💬 Comments: {video_data['comments']:,}")
        
    except Exception as e:
        print(f"❌ Error getting video info: {e}")
        return
    
    # Get comments sentiment
    try:
        comments_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50,
            order="relevance"
        ).execute()
        
        if not comments_response['items']:
            print("💬 No comments found")
            sentiment_data = {'positive': 0, 'negative': 0, 'neutral': 0, 'total': 0}
        else:
            positive = negative = neutral = 0
            
            print(f"\n💬 Analyzing {len(comments_response['items'])} comments...")
            
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                scores = sia.polarity_scores(comment)
                
                if scores['compound'] > 0.05:
                    positive += 1
                elif scores['compound'] < -0.05:
                    negative += 1
                else:
                    neutral += 1
            
            total = len(comments_response['items'])
            sentiment_data = {
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'total': total
            }
            
            print(f"😊 Positive: {positive} ({positive/total*100:.1f}%)")
            print(f"😞 Negative: {negative} ({negative/total*100:.1f}%)")
            print(f"😐 Neutral: {neutral} ({neutral/total*100:.1f}%)")
        
        # Save to database
        save_to_database(video_id, video_data, sentiment_data)
        
    except Exception as e:
        print(f"❌ Error analyzing comments: {e}")

if __name__ == "__main__":
    # Initialize database
    init_database()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python youtube_analytics.py VIDEO_ID")
        print("  python youtube_analytics.py --history")
        print("  python youtube_analytics.py --progress")
        print("\nExample: python youtube_analytics.py dQw4w9WgXcQ")
        sys.exit(1)
    
    if sys.argv[1] == "--history":
        show_history()
    elif sys.argv[1] == "--progress":
        show_progress()
    else:
        video_id = sys.argv[1]
        analyze_video(video_id) 