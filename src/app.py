"""
YouTube Analytics AI Backend API
"""

import os
import logging
from flask import Flask, request, jsonify
from src.agents.analytics_agent import AnalyticsAgent

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "YOUR_API_KEY")
analytics_agent = AnalyticsAgent(YOUTUBE_API_KEY)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "YouTube Analytics AI Backend",
        "version": "1.0.0"
    })

@app.route('/api/analytics', methods=['POST'])
def get_analytics():
    """Get video analytics only (basic stats)"""
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        if not video_id:
            return jsonify({"error": "Video ID is required"}), 400
        result = analytics_agent.process({'video_id': video_id})
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/comments', methods=['POST'])
def get_comments():
    """Get video comments analysis (sentiment and basic stats)"""
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        if not video_id:
            return jsonify({"error": "Video ID is required"}), 400
        result = analytics_agent.comment_analytics(video_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_comments: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/channel/<channel_id>', methods=['GET'])
def channel_analytics(channel_id):
    """Get comprehensive channel analytics"""
    try:
        result = analytics_agent.get_channel_analytics(channel_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in channel_analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/channel/compare', methods=['POST'])
def compare_channels():
    """Compare multiple channels"""
    try:
        data = request.get_json()
        channel_ids = data.get('channel_ids', [])
        
        if not channel_ids:
            return jsonify({"error": "No channel IDs provided"}), 400
        
        result = analytics_agent.compare_channels(channel_ids)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in compare_channels: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get aggregated analytics metrics"""
    try:
        result = analytics_agent.get_metrics()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get analysis history"""
    try:
        result = analytics_agent.get_history()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/video/compare', methods=['POST'])
def compare_videos_by_keywords():
    """Compare a video with similar videos based on keywords/tags."""
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        max_results = data.get('max_results', 5)
        
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400
        
        result = analytics_agent.compare_videos_by_keywords(video_id, max_results)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/video/technical-insights', methods=['POST'])
def get_technical_insights():
    """Get detailed technical insights and success patterns for a video."""
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        max_results = data.get('max_results', 5)
        
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400
        
        result = analytics_agent.get_technical_insights(video_id, max_results)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/video/sponsorship/<video_id>', methods=['GET'])
def analyze_video_sponsorship(video_id):
    """Analyze sponsorships in a specific video"""
    try:
        result = analytics_agent.analyze_sponsorships(video_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in analyze_video_sponsorship: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/video/search-sponsored', methods=['POST'])
def search_sponsored_videos():
    """Search for videos with keywords and analyze their sponsorship patterns"""
    try:
        data = request.get_json()
        keywords = data.get('keywords')
        max_results = data.get('max_results', 10)
        
        if not keywords:
            return jsonify({"error": "Keywords are required"}), 400
        
        result = analytics_agent.search_sponsored_videos(keywords, max_results)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in search_sponsored_videos: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 