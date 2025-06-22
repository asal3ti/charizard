"""
Analytics Agent for YouTube Video Analysis
"""

from typing import Dict, Any, List
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.agents.base_agent import BaseAgent
import importlib
import src.services.youtube_service
import concurrent.futures

class AnalyticsAgent(BaseAgent):
    """Agent for analyzing YouTube video analytics and comments"""
    
    def __init__(self, api_key: str, model_name: str = "gemma3:latest"):
        super().__init__(model_name)
        
        # Force reload the module to ensure we get the latest version
        importlib.reload(src.services.youtube_service)
        from src.services.youtube_service import EnhancedYouTubeService
        
        self.youtube_service = EnhancedYouTubeService(api_key)
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Workaround: Add missing methods to youtube_service if they don't exist
        if not hasattr(self.youtube_service, 'get_video_comments'):
            print("DEBUG: Adding get_video_comments method")
            self.youtube_service.get_video_comments = self.youtube_service.get_comments
        if not hasattr(self.youtube_service, 'get_video_transcript'):
            print("DEBUG: Adding get_video_transcript method")
            self.youtube_service.get_video_transcript = self.youtube_service.get_transcript
    
    def get_with_timeout(self, func, *args, timeout=20, **kwargs):
        """Execute a function with a timeout using ThreadPoolExecutor"""
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=timeout)
                except concurrent.futures.TimeoutError:
                    # Cancel the future if it's still running
                    future.cancel()
                    return {"error": f"Operation exceeded {timeout} seconds."}
                except Exception as e:
                    return {"error": f"Operation failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Thread pool error: {str(e)}"}
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process video analytics only (basic stats)"""
        try:
            video_id = data.get('video_id')
            if not video_id:
                return self.handle_error(ValueError("Video ID is required"), "Missing video_id")
            self.log_activity("Starting video analytics", {"video_id": video_id})
            video_analytics = self.youtube_service.get_video_info(video_id)
            if not video_analytics:
                return {"error": "Could not fetch video info"}
            return {"video_analytics": video_analytics}
        except Exception as e:
            return self.handle_error(e, "Analytics processing")

    def comment_analytics(self, video_id: str) -> Dict[str, Any]:
        """Analyze comments for a video (sentiment and basic stats)"""
        try:
            comments = self.youtube_service.get_comments(video_id, max_results=200)
            if not comments:
                return {"error": "No comments found"}
            # Simple sentiment breakdown
            sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
            for c in comments:
                sentiment = c.get("sentiment", "neutral")
                if sentiment in sentiment_counts:
                    sentiment_counts[sentiment] += 1
            return {
                "total_comments": len(comments),
                "sentiment_breakdown": sentiment_counts,
                "comments": comments[:20]  # Return only first 20 for demo
            }
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_comments(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze comments using multiple sentiment analysis methods"""
        if not comments or not isinstance(comments, list):
            return {"error": "No comments found or invalid comment data"}
        
        results = {
            "total_comments": len(comments),
            "sentiment_breakdown": {"positive": 0, "negative": 0, "neutral": 0},
            "categories": {},
            "ai_analysis": [],
            "engagement_metrics": {
                "total_likes": 0,
                "total_replies": 0,
                "avg_likes_per_comment": 0
            }
        }
        
        total_likes = 0
        total_replies = 0
        
        for comment in comments:
            text = comment.get('comment', '')
            likes = comment.get('likes', 0)
            replies = comment.get('reply_count', 0)
            
            total_likes += likes
            total_replies += replies
            
            # VADER sentiment analysis
            vader_scores = self.vader_analyzer.polarity_scores(text)
            
            # TextBlob sentiment analysis
            blob = TextBlob(text)
            textblob_sentiment = blob.sentiment.polarity
            
            # AI sentiment analysis
            ai_sentiment = self.ai_service.analyze_sentiment(text)
            
            # AI categorization
            ai_category = self.ai_service.categorize_comment(text)
            
            # Determine overall sentiment
            if vader_scores['compound'] > 0.05:
                sentiment = "positive"
            elif vader_scores['compound'] < -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            results["sentiment_breakdown"][sentiment] += 1
            
            # Track categories
            category = ai_category.get('category', 'other')
            if category not in results["categories"]:
                results["categories"][category] = 0
            results["categories"][category] += 1
            
            # Store AI analysis
            results["ai_analysis"].append({
                "comment_id": comment.get('id'),
                "text": text,
                "vader_scores": vader_scores,
                "textblob_sentiment": textblob_sentiment,
                "ai_sentiment": ai_sentiment,
                "ai_category": ai_category,
                "likes": likes,
                "replies": replies
            })
        
        # Calculate engagement metrics
        results["engagement_metrics"]["total_likes"] = total_likes
        results["engagement_metrics"]["total_replies"] = total_replies
        results["engagement_metrics"]["avg_likes_per_comment"] = total_likes / len(comments) if comments else 0
        
        return results
    
    def analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze video transcript"""
        if not transcript:
            return {"error": "No transcript found"}
        
        # Basic text analysis
        blob = TextBlob(transcript)
        
        # AI analysis of transcript
        ai_analysis = self.ai_service.generate_content(
            f"Analyze this video transcript and provide insights about: "
            f"1. Main topics discussed\n"
            f"2. Key points\n"
            f"3. Overall tone\n"
            f"4. Engagement potential\n\n"
            f"Transcript: {transcript[:2000]}...",  # Limit length
            "transcript analysis"
        )
        
        return {
            "word_count": len(transcript.split()),
            "sentence_count": len(blob.sentences),
            "avg_sentence_length": len(transcript.split()) / len(blob.sentences) if blob.sentences else 0,
            "ai_analysis": ai_analysis,
            "transcript_preview": transcript[:500] + "..." if len(transcript) > 500 else transcript
        }
    
    def generate_summary(self, video_analytics: Dict, comment_analysis: Dict, transcript_analysis: Dict) -> str:
        """Generate a summary of all analytics"""
        context = f"""
        Video Analytics: {video_analytics}
        Comment Analysis: {comment_analysis.get('total_comments', 0)} comments analyzed
        Transcript Analysis: {transcript_analysis.get('word_count', 0)} words
        """
        
        return self.ai_service.generate_content(context, "comprehensive video analytics summary")

    def get_channel_analytics(self, channel_id: str) -> Dict[str, Any]:
        """Get comprehensive channel analytics"""
        try:
            # Get channel info
            channel_info = self.youtube_service.get_channel_info(channel_id)
            if not channel_info:
                return {"error": "Channel not found"}
            
            # Get recent videos for analysis
            recent_videos = self.youtube_service.get_channel_videos(channel_id, max_results=20)
            
            # Analyze recent videos
            videos_analytics = []
            total_views = 0
            total_likes = 0
            total_comments = 0
            
            for video in recent_videos:
                video_id = video.get('id', {}).get('videoId')
                if video_id:
                    video_stats = self.youtube_service.get_video_info(video_id)
                    if video_stats:
                        views = video_stats.get('view_count', 0)
                        likes = video_stats.get('like_count', 0)
                        comments = video_stats.get('comment_count', 0)
                        
                        videos_analytics.append({
                            "video_id": video_id,
                            "title": video_stats.get('title', ''),
                            "views": views,
                            "likes": likes,
                            "comments": comments,
                            "engagement_rate": video_stats.get('engagement_rate', 0),
                            "published_at": video_stats.get('published_at', '')
                        })
                        
                        total_views += views
                        total_likes += likes
                        total_comments += comments
            
            # Calculate metrics
            avg_views_per_video = total_views / len(videos_analytics) if videos_analytics else 0
            avg_likes_per_video = total_likes / len(videos_analytics) if videos_analytics else 0
            avg_comments_per_video = total_comments / len(videos_analytics) if videos_analytics else 0
            
            # Engagement metrics
            total_engagement = total_likes + total_comments
            channel_engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0
            
            # Performance analysis
            performance_analysis = self.analyze_channel_performance(videos_analytics)
            
            return {
                "channel_info": channel_info,
                "statistics": {
                    "subscriber_count": channel_info.get('subscriber_count', 0),
                    "video_count": channel_info.get('video_count', 0),
                    "view_count": channel_info.get('view_count', 0),
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_comments": total_comments
                },
                "metrics": {
                    "avg_views_per_video": round(avg_views_per_video, 0),
                    "avg_likes_per_video": round(avg_likes_per_video, 0),
                    "avg_comments_per_video": round(avg_comments_per_video, 0),
                    "channel_engagement_rate": round(channel_engagement_rate, 2),
                    "views_per_subscriber": round(channel_info.get('view_count', 0) / channel_info.get('subscriber_count', 1), 2),
                    "videos_per_month": round(channel_info.get('video_count', 0) / 12, 1)
                },
                "performance_analysis": performance_analysis,
                "recent_videos": videos_analytics[:10]
            }
            
        except Exception as e:
            return {"error": str(e)}

    def analyze_channel_performance(self, videos_analytics: List[Dict]) -> Dict[str, Any]:
        """Analyze channel performance patterns"""
        if not videos_analytics:
            return {"insights": ["No video data available"]}
        
        insights = []
        
        # Sort videos by different metrics
        by_views = sorted(videos_analytics, key=lambda x: x.get('views', 0), reverse=True)
        by_engagement = sorted(videos_analytics, key=lambda x: x.get('engagement_rate', 0), reverse=True)
        
        # Top performing videos
        top_viewed = by_views[0] if by_views else None
        top_engaged = by_engagement[0] if by_engagement else None
        
        if top_viewed:
            insights.append(f"Most viewed video: '{top_viewed.get('title', '')[:50]}...' ({top_viewed.get('views', 0):,} views)")
        
        if top_engaged:
            insights.append(f"Highest engagement: '{top_engaged.get('title', '')[:50]}...' ({top_engaged.get('engagement_rate', 0)}% engagement)")
        
        # Performance patterns
        avg_engagement = sum(v.get('engagement_rate', 0) for v in videos_analytics) / len(videos_analytics)
        if avg_engagement > 5:
            insights.append("High average engagement rate across videos")
        elif avg_engagement < 1:
            insights.append("Low average engagement rate - consider content strategy")
        
        # Consistency analysis
        view_counts = [v.get('views', 0) for v in videos_analytics]
        if view_counts and min(view_counts) > 0:
            view_variance = max(view_counts) / min(view_counts)
            if view_variance > 10:
                insights.append("High view variance - content performance is inconsistent")
            else:
                insights.append("Consistent view performance across videos")
        
        return {"insights": insights}

    def compare_channels(self, channel_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple channels"""
        comparison = {}
        
        for channel_id in channel_ids:
            channel_data = self.get_channel_analytics(channel_id)
            if 'error' not in channel_data:
                comparison[channel_id] = {
                    "title": channel_data.get('channel_info', {}).get('title', ''),
                    "subscribers": channel_data.get('statistics', {}).get('subscriber_count', 0),
                    "total_views": channel_data.get('statistics', {}).get('view_count', 0),
                    "engagement_rate": channel_data.get('metrics', {}).get('channel_engagement_rate', 0),
                    "avg_views_per_video": channel_data.get('metrics', {}).get('avg_views_per_video', 0)
                }
        
        return comparison

    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated analytics metrics"""
        try:
            # This would typically query a database for aggregated metrics
            # For now, return sample metrics
            return {
                "total_videos": 0,
                "total_comments": 0,
                "avg_engagement_rate": 0.0,
                "avg_sentiment_score": 0.0,
                "last_updated": "2024-01-01T00:00:00Z"
            }
        except Exception as e:
            return {"error": str(e)}

    def get_history(self) -> Dict[str, Any]:
        """Get analysis history"""
        try:
            # This would typically query a database for analysis history
            # For now, return sample history
            return {
                "analytics": [
                    {
                        "video_id": "sample_video_id",
                        "title": "Sample Video",
                        "analyzed_at": "2024-01-01T00:00:00Z",
                        "views": 100000,
                        "engagement_rate": 5.2
                    }
                ],
                "total_analyses": 1
            }
        except Exception as e:
            return {"error": str(e)}

    def compare_videos_by_keywords(self, video_id: str, max_results: int = 5) -> Dict[str, Any]:
        """Compare a video with similar videos based on keywords/tags and analyze sponsorships."""
        try:
            result = self.youtube_service.compare_videos_by_keywords(video_id, max_results)
            return result
        except Exception as e:
            return {"error": str(e)}

    def get_technical_insights(self, video_id: str, max_results: int = 5) -> Dict[str, Any]:
        """Get detailed technical insights and success patterns for a video."""
        try:
            # Get video comparison with technical insights
            comparison_result = self.youtube_service.compare_videos_by_keywords(video_id, max_results)
            
            if "error" in comparison_result:
                return comparison_result
            
            # Extract technical insights
            technical_insights = comparison_result.get("technical_insights", {})
            
            return {
                "video_id": video_id,
                "technical_insights": technical_insights,
                "summary": {
                    "original_performance": technical_insights.get("original_video_analysis", {}),
                    "comparison_metrics": technical_insights.get("similar_videos_analysis", {}).get("average_metrics", {}),
                    "top_recommendations": technical_insights.get("recommendations", [])[:3]
                }
            }
            
        except Exception as e:
            return {"error": str(e)}

    def analyze_sponsorships(self, video_id: str) -> Dict[str, Any]:
        """Analyze sponsorships in a specific video."""
        try:
            # Get video info
            video_info = self.youtube_service.get_video_info(video_id)
            if not video_info:
                return {"error": "Video not found"}
            
            # Get transcript
            transcript = self.youtube_service.get_transcript(video_id)
            
            # Detect sponsorships
            sponsorship_analysis = self.youtube_service.detect_sponsorships(
                transcript or "",
                video_info.get('title', ""),
                video_info.get('description', "")
            )
            
            return {
                "video_id": video_id,
                "title": video_info.get('title', ''),
                "channel": video_info.get('channel', ''),
                "sponsorship_analysis": sponsorship_analysis,
                "transcript_length": len(transcript) if transcript else 0
            }
            
        except Exception as e:
            return {"error": str(e)}

    def search_sponsored_videos(self, keywords: str, max_results: int = 10) -> Dict[str, Any]:
        """Search for videos with keywords and analyze their sponsorship patterns."""
        try:
            # Search for videos
            videos = self.youtube_service.search_videos_by_keywords(keywords, max_results)
            
            # Analyze each video for sponsorships
            analyzed_videos = []
            for video in videos:
                video_id = video['id']
                
                # Get detailed video info
                video_details = self.youtube_service.get_video_info(video_id)
                if not video_details:
                    continue
                
                # Get transcript
                transcript = self.youtube_service.get_transcript(video_id)
                
                # Detect sponsorships
                sponsorship_analysis = self.youtube_service.detect_sponsorships(
                    transcript or "",
                    video_details.get('title', ""),
                    video_details.get('description', "")
                )
                
                # Calculate engagement metrics
                view_count = video_details.get('view_count', 0)
                like_count = video_details.get('like_count', 0)
                comment_count = video_details.get('comment_count', 0)
                engagement_rate = ((like_count + comment_count) / view_count * 100) if view_count > 0 else 0
                
                analyzed_video = {
                    "video_id": video_id,
                    "title": video_details.get('title', ''),
                    "channel": video_details.get('channel', ''),
                    "published_at": video_details.get('published_at', ''),
                    "view_count": view_count,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "engagement_rate": round(engagement_rate, 2),
                    "sponsorship_analysis": sponsorship_analysis,
                    "thumbnail": video_details.get('thumbnail', '')
                }
                
                analyzed_videos.append(analyzed_video)
            
            # Generate sponsorship summary
            sponsorship_summary = self.youtube_service.generate_sponsorship_summary(analyzed_videos)
            
            return {
                "search_keywords": keywords,
                "total_videos": len(analyzed_videos),
                "videos": analyzed_videos,
                "sponsorship_summary": sponsorship_summary
            }
            
        except Exception as e:
            return {"error": str(e)} 