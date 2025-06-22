"""
Analytics Agent for YouTube Video Analysis
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.agents.base_agent import BaseAgent
import importlib
import src.services.youtube_service
import src.services.enhanced_insights_service
import concurrent.futures

class AnalyticsAgent(BaseAgent):
    """Agent for analyzing YouTube video analytics and comments"""
    
    def __init__(self, api_key: str, model_name: Optional[str] = None):
        super().__init__(model_name)
        
        # Force reload the module to ensure we get the latest version
        importlib.reload(src.services.youtube_service)
        importlib.reload(src.services.enhanced_insights_service)
        from src.services.youtube_service import EnhancedYouTubeService
        from src.services.enhanced_insights_service import EnhancedInsightsService
        
        self.youtube_service = EnhancedYouTubeService(api_key)
        self.enhanced_insights = EnhancedInsightsService()
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
            try:
                blob = TextBlob(text)
                textblob_sentiment = float(blob.sentiment.polarity)
            except:
                textblob_sentiment = 0.0
            
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
        try:
            blob = TextBlob(transcript)
            sentences = list(blob.sentences)
            sentence_count = len(sentences)
        except:
            # Fallback to simple sentence counting
            sentences = transcript.split('.')
            sentence_count = len([s for s in sentences if s.strip()])
        
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
        
        word_count = len(transcript.split())
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": word_count / sentence_count if sentence_count > 0 else 0,
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

    def get_enhanced_insights(self, video_id: str) -> Dict[str, Any]:
        """Get enhanced insights using the new insights service"""
        try:
            # Get basic video data
            video_info = self.youtube_service.get_video_info(video_id)
            if not video_info:
                return {"error": "Could not fetch video info"}
            
            # Get comments for analysis
            comments = self.youtube_service.get_comments(video_id, max_results=100)
            
            # Generate enhanced insights
            enhanced_results = {}
            
            # Content performance prediction
            performance_analysis = self.enhanced_insights.analyze_content_performance_potential(video_info)
            enhanced_results["performance_prediction"] = performance_analysis
            
            # Audience behavior patterns
            if comments:
                audience_analysis = self.enhanced_insights.analyze_audience_behavior_patterns(comments)
                enhanced_results["audience_behavior"] = audience_analysis
            
            # Content optimization suggestions
            optimization_suggestions = self.enhanced_insights.generate_content_optimization_suggestions(video_info, comments or [])
            enhanced_results["optimization_suggestions"] = optimization_suggestions
            
            # AI-generated insights
            ai_insights = self.ai_service.generate_insights({
                "video_info": video_info,
                "comments_count": len(comments) if comments else 0,
                "performance_score": performance_analysis.get("performance_score", 0)
            }, "comprehensive video analytics")
            enhanced_results["ai_insights"] = ai_insights
            
            # Performance prediction
            performance_prediction = self.ai_service.predict_performance(video_info)
            enhanced_results["performance_prediction"]["ai_prediction"] = performance_prediction
            
            return enhanced_results
            
        except Exception as e:
            return {"error": f"Enhanced insights generation failed: {str(e)}"}
    
    def get_content_gap_analysis(self, channel_id: str, niche_keywords: List[str]) -> Dict[str, Any]:
        """Analyze content gaps in the niche"""
        try:
            # Get channel videos
            channel_videos = self.youtube_service.get_channel_videos(channel_id, max_results=50)
            
            # Search for videos in the niche
            niche_videos = []
            for keyword in niche_keywords[:3]:  # Limit to top 3 keywords
                search_results = self.youtube_service.search_videos_by_keywords(keyword, max_results=20)
                niche_videos.extend(search_results)
            
            # Analyze gaps
            channel_topics = set()
            niche_topics = set()
            
            # Extract topics from channel videos
            for video in channel_videos:
                title = video.get('snippet', {}).get('title', '').lower()
                description = video.get('snippet', {}).get('description', '').lower()
                channel_topics.update(title.split() + description.split())
            
            # Extract topics from niche videos
            for video in niche_videos:
                title = video.get('snippet', {}).get('title', '').lower()
                description = video.get('snippet', {}).get('description', '').lower()
                niche_topics.update(title.split() + description.split())
            
            # Find gaps
            content_gaps = niche_topics - channel_topics
            
            # Generate AI insights on gaps
            gap_analysis = self.ai_service.generate_insights({
                "channel_topics": list(channel_topics)[:20],
                "niche_topics": list(niche_topics)[:20],
                "content_gaps": list(content_gaps)[:20],
                "channel_videos_count": len(channel_videos),
                "niche_videos_count": len(niche_videos)
            }, "content gap analysis")
            
            return {
                "channel_topics": list(channel_topics)[:20],
                "niche_topics": list(niche_topics)[:20],
                "content_gaps": list(content_gaps)[:20],
                "gap_analysis": gap_analysis,
                "opportunity_score": len(content_gaps) / max(len(niche_topics), 1) * 100
            }
            
        except Exception as e:
            return {"error": f"Content gap analysis failed: {str(e)}"}
    
    def get_trend_analysis(self, keywords: List[str]) -> Dict[str, Any]:
        """Analyze trends for given keywords"""
        try:
            trend_data = {}
            
            for keyword in keywords[:5]:  # Limit to 5 keywords
                # Search for recent videos
                recent_videos = self.youtube_service.search_videos_by_keywords(keyword, max_results=20)
                
                if recent_videos:
                    # Analyze engagement patterns
                    engagement_rates = []
                    view_counts = []
                    
                    for video in recent_videos:
                        video_id = video.get('id', {}).get('videoId')
                        if video_id:
                            video_info = self.youtube_service.get_video_info(video_id)
                            if video_info:
                                views = video_info.get('view_count', 0)
                                likes = video_info.get('like_count', 0)
                                comments = video_info.get('comment_count', 0)
                                
                                if views > 0:
                                    engagement_rate = ((likes + comments) / views) * 100
                                    engagement_rates.append(engagement_rate)
                                    view_counts.append(views)
                    
                    if engagement_rates:
                        trend_data[keyword] = {
                            "avg_engagement_rate": sum(engagement_rates) / len(engagement_rates),
                            "avg_views": sum(view_counts) / len(view_counts),
                            "video_count": len(recent_videos),
                            "trend_strength": "High" if sum(engagement_rates) / len(engagement_rates) > 3 else "Medium"
                        }
            
            # Generate AI insights on trends
            trend_insights = self.ai_service.generate_insights(trend_data, "trend analysis")
            
            return {
                "trend_data": trend_data,
                "trend_insights": trend_insights,
                "top_trending_keywords": sorted(trend_data.items(), key=lambda x: x[1].get('avg_engagement_rate', 0), reverse=True)[:3]
            }
            
        except Exception as e:
            return {"error": f"Trend analysis failed: {str(e)}"}
    
    def get_competitor_analysis(self, channel_id: str, competitor_channels: List[str]) -> Dict[str, Any]:
        """Analyze performance against competitors"""
        try:
            competitor_data = {}
            
            # Analyze main channel
            main_channel = self.get_channel_analytics(channel_id)
            if "error" not in main_channel:
                competitor_data["main_channel"] = {
                    "engagement_rate": main_channel.get("metrics", {}).get("channel_engagement_rate", 0),
                    "avg_views": main_channel.get("metrics", {}).get("avg_views_per_video", 0),
                    "subscriber_count": main_channel.get("statistics", {}).get("subscriber_count", 0)
                }
            
            # Analyze competitors
            for comp_channel_id in competitor_channels[:5]:  # Limit to 5 competitors
                comp_channel = self.get_channel_analytics(comp_channel_id)
                if "error" not in comp_channel:
                    competitor_data[comp_channel_id] = {
                        "engagement_rate": comp_channel.get("metrics", {}).get("channel_engagement_rate", 0),
                        "avg_views": comp_channel.get("metrics", {}).get("avg_views_per_video", 0),
                        "subscriber_count": comp_channel.get("statistics", {}).get("subscriber_count", 0)
                    }
            
            # Generate competitive insights
            competitive_insights = self.ai_service.generate_insights(competitor_data, "competitive analysis")
            
            return {
                "competitor_data": competitor_data,
                "competitive_insights": competitive_insights,
                "market_position": self._calculate_market_position(competitor_data)
            }
            
        except Exception as e:
            return {"error": f"Competitor analysis failed: {str(e)}"}
    
    def _calculate_market_position(self, competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market position based on competitor data"""
        if not competitor_data or "main_channel" not in competitor_data:
            return {"position": "Unknown", "strengths": [], "weaknesses": []}
        
        main_channel = competitor_data["main_channel"]
        competitors = [data for key, data in competitor_data.items() if key != "main_channel"]
        
        if not competitors:
            return {"position": "No competitors analyzed", "strengths": [], "weaknesses": []}
        
        # Calculate rankings
        engagement_ranking = sorted(competitors, key=lambda x: x.get("engagement_rate", 0), reverse=True)
        views_ranking = sorted(competitors, key=lambda x: x.get("avg_views", 0), reverse=True)
        
        # Find main channel position
        engagement_position = 1
        for comp in engagement_ranking:
            if comp.get("engagement_rate", 0) > main_channel.get("engagement_rate", 0):
                engagement_position += 1
        
        views_position = 1
        for comp in views_ranking:
            if comp.get("avg_views", 0) > main_channel.get("avg_views", 0):
                views_position += 1
        
        total_competitors = len(competitors)
        
        return {
            "engagement_rank": f"{engagement_position}/{total_competitors + 1}",
            "views_rank": f"{views_position}/{total_competitors + 1}",
            "overall_position": "Leader" if engagement_position <= 2 and views_position <= 2 else "Challenger" if engagement_position <= total_competitors // 2 else "Follower",
            "strengths": ["High engagement"] if engagement_position <= 2 else [],
            "weaknesses": ["Low views"] if views_position > total_competitors // 2 else []
        } 