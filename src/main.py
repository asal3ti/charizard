#!/usr/bin/env python3
"""
Flask Backend API for YouTube Comment Sentiment Analyzer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import re
import os
import base64
import io
import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import langid
import logging
from datetime import datetime

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeCommentAnalyzer:
    def __init__(self, api_key):
        """Initialize the analyzer with YouTube API key."""
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.sia = SentimentIntensityAnalyzer()

        # Define sarcasm detection keywords and indicators
        self.negative_context_keywords = [
            'clickbait', 'waste of time', 'fake', 'scam', 'slow', 'unwatchable',
            'ads', 'noise', 'laggy', 'again', 'great job', 'thanks a lot',
            'as always', 'fell off'
        ]

        self.sarcasm_indicators = [
            'sure', 'totally', 'wow', 'thanks a lot', 'great job', 'genius',
            'lmao', 'lol', 'yeah right', 'can\'t wait', 'so helpful', 'this aged well'
        ]

        self.emoji_indicators = ['🙄', '😒', '🤡', '😂', '🤣', '😑']

    def extract_video_id(self, url):
        """Extract video ID from YouTube URL."""
        parsed_url = urlparse(url)

        # Handle youtu.be short links
        if parsed_url.hostname in ["youtu.be"]:
            return parsed_url.path.lstrip("/")

        # Handle full length YouTube links
        elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            query = parse_qs(parsed_url.query)
            return query.get("v", [None])[0]

        return None

    def get_video_info(self, video_id):
        """Get video metadata."""
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()

            if response['items']:
                video = response['items'][0]
                return {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'][:200] + '...',
                    'channel': video['snippet']['channelTitle'],
                    'published_at': video['snippet']['publishedAt'],
                    'view_count': video['statistics'].get('viewCount', 0),
                    'like_count': video['statistics'].get('likeCount', 0),
                    'comment_count': video['statistics'].get('commentCount', 0),
                    'thumbnail': video['snippet']['thumbnails']['medium']['url']
                }
        except Exception as e:
            logger.error(f"Error fetching video info: {e}")
            return None

    def get_comments(self, video_id, max_results=500):
        """Fetch comments from a YouTube video."""
        comments = []
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )

        try:
            response = request.execute()

            while response and len(comments) < max_results:
                for item in response['items']:
                    comment_data = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        "Author": comment_data['authorDisplayName'],
                        "Comment": comment_data['textDisplay'],
                        "Published": comment_data['publishedAt'],
                        "Likes": comment_data.get('likeCount', 0)
                    })

                if 'nextPageToken' in response and len(comments) < max_results:
                    request = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        pageToken=response['nextPageToken'],
                        maxResults=100
                    )
                    response = request.execute()
                else:
                    break

        except Exception as e:
            logger.error(f"Error fetching comments: {e}")

        return comments

    def is_english(self, text):
        """Check if text is in English using language detection."""
        if not isinstance(text, str) or text.strip() == '':
            return False

        try:
            lang, confidence = langid.classify(text)
            is_ascii_heavy = len([c for c in text if ord(c) < 128]) / len(text) > 0.7
            return (lang == 'en' and confidence > 0.5) or (lang == 'en' and is_ascii_heavy)
        except:
            try:
                ascii_ratio = len([c for c in text if ord(c) < 128]) / len(text)
                return ascii_ratio > 0.8
            except:
                return False

    def detect_sarcasm(self, comment):
        """Detect sarcasm in YouTube comments using rule-based approach."""
        if not isinstance(comment, str):
            return 'not sarcastic'

        text = comment.lower()
        sentiment = self.sia.polarity_scores(text)
        compound = sentiment['compound']

        contains_neg_context = any(kw in text for kw in self.negative_context_keywords)
        contains_sarcasm_clue = any(kw in text for kw in self.sarcasm_indicators)
        contains_emoji = any(e in text for e in self.emoji_indicators)
        has_caps_exaggeration = bool(re.search(r'\b[A-Z]{2,}\b', comment))

        if (compound > 0.4) and (contains_neg_context or contains_sarcasm_clue or
                                 contains_emoji or has_caps_exaggeration):
            return 'sarcastic'

        if compound < 0.4 and (contains_sarcasm_clue or contains_emoji) and contains_neg_context:
            return 'sarcastic'

        return 'not sarcastic'

    def classify_sentiment(self, text):
        """Classify sentiment using VADER sentiment analyzer."""
        if not isinstance(text, str) or text.strip() == '':
            return 'neutral'

        score = self.sia.polarity_scores(text)
        compound = score['compound']

        if compound >= 0.05:
            return 'positive'
        elif compound <= -0.05:
            return 'negative'
        else:
            return 'neutral'

    def create_visualizations_base64(self, df):
        """Create visualizations and return as base64 encoded strings."""
        # Sentiment distribution pie chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Pie chart
        sentiment_counts = df['sentiment'].value_counts()
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax1.set_title('Sentiment Distribution')

        # Bar chart for sarcasm
        sarcasm_counts = df['sarcasm_label'].value_counts()
        bars = ax2.bar(range(len(sarcasm_counts)), sarcasm_counts.values,
                       color=['#3498db', '#f39c12'])
        ax2.set_xticks(range(len(sarcasm_counts)))
        ax2.set_xticklabels([label.replace('_', ' ').title() for label in sarcasm_counts.index])
        ax2.set_title('Sarcasm Detection')
        ax2.set_ylabel('Count')

        plt.tight_layout()

        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()

        return img_base64

    def analyze_comments(self, comments):
        """Analyze comments and return comprehensive results."""
        if not comments:
            return None

        df = pd.DataFrame(comments)

        # Filter English comments
        df['is_english'] = df['Comment'].apply(self.is_english)
        df_english = df[df['is_english'] == True].copy()

        # If no English comments found, use all comments
        if len(df_english) == 0:
            df_english = df.copy()

        # Add sentiment analysis
        df_english['sentiment'] = df_english['Comment'].apply(self.classify_sentiment)
        df_english['sarcasm_label'] = df_english['Comment'].apply(self.detect_sarcasm)

        # Calculate statistics
        sentiment_stats = df_english['sentiment'].value_counts(normalize=True) * 100
        sarcasm_stats = df_english['sarcasm_label'].value_counts(normalize=True) * 100

        # Generate visualizations
        # chart_base64 = self.create_visualizations_base64(df_english)

        # Prepare sample comments
        sample_comments = df_english[['Author', 'Comment', 'sentiment', 'sarcasm_label']].head(10).to_dict('records')

        return {
            'total_comments': len(df),
            'english_comments': len(df_english),
            'sentiment_distribution': sentiment_stats.round(2).to_dict(),
            'sarcasm_distribution': sarcasm_stats.round(2).to_dict(),
            'sample_comments': sample_comments,
            'analysis_timestamp': datetime.now().isoformat()
        }


# Initialize analyzer
API_KEY = "AIzaSyDfnWlqiN27t-8OrlRZHAjjH8oL1UahToo"  # Replace with your API key
analyzer = YouTubeCommentAnalyzer(API_KEY)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analyze YouTube video comments."""
    try:
        data = request.get_json()
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({"error": "video_url is required"}), 400

        # Extract video ID
        video_id = analyzer.extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # Get video info
        video_info = analyzer.get_video_info(video_id)
        if not video_info:
            return jsonify({"error": "Video not found or private"}), 404

        # Get comments
        comments = analyzer.get_comments(video_id)
        if not comments:
            return jsonify({"error": "No comments found or comments are disabled"}), 404

        # Analyze comments
        analysis_results = analyzer.analyze_comments(comments)
        if not analysis_results:
            return jsonify({"error": "Failed to analyze comments"}), 500

        return jsonify({
            "success": True,
            "video_info": video_info,
            "analysis": analysis_results
        })

    except Exception as e:
        logger.error(f"Error in analyze_video: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route('/api/extract-video-id', methods=['POST'])
def extract_video_id():
    """Extract video ID from URL."""
    try:
        data = request.get_json()
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({"error": "video_url is required"}), 400

        video_id = analyzer.extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        return jsonify({"video_id": video_id})

    except Exception as e:
        logger.error(f"Error in extract_video_id: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)