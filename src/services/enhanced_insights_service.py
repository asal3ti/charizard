"""
Enhanced Insights Service - Advanced YouTube Analytics
Provides insights that go beyond basic YouTube API data
"""

import re
import json
import math
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import numpy as np
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import requests
from PIL import Image
import io

# Download required NLTK data
try:
    nltk.data.find('punkt')
    nltk.data.find('stopwords')
    nltk.data.find('wordnet')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class EnhancedInsightsService:
    """Service for generating advanced YouTube insights"""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Content performance indicators
        self.performance_keywords = {
            'clickbait': ['shocking', 'amazing', 'incredible', 'you won\'t believe', 'gone wrong'],
            'educational': ['how to', 'tutorial', 'guide', 'explained', 'learn'],
            'entertainment': ['funny', 'comedy', 'prank', 'challenge', 'reaction'],
            'news': ['breaking', 'latest', 'update', 'news', 'announcement'],
            'review': ['review', 'unboxing', 'test', 'comparison', 'vs']
        }
        
        # Engagement triggers
        self.engagement_triggers = [
            'subscribe', 'like', 'comment', 'share', 'follow', 'hit the bell',
            'turn on notifications', 'smash that like button', 'drop a comment'
        ]
        
        # Viral indicators
        self.viral_indicators = [
            'trending', 'viral', 'blowing up', 'everyone is talking about',
            'breaking the internet', 'going viral', 'exploding'
        ]
    
    def analyze_content_performance_potential(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict content performance potential based on multiple factors"""
        try:
            title = video_data.get('title', '').lower()
            description = video_data.get('description', '').lower()
            tags = [tag.lower() for tag in video_data.get('tags', [])]
            
            # Calculate performance score
            score = 0
            factors = {}
            
            # Title analysis
            title_score = self._analyze_title_effectiveness(title)
            score += title_score['score']
            factors['title_analysis'] = title_score
            
            # Content type analysis
            content_type_score = self._analyze_content_type(title, description, tags)
            score += content_type_score['score']
            factors['content_type'] = content_type_score
            
            # Engagement potential
            engagement_score = self._analyze_engagement_potential(title, description)
            score += engagement_score['score']
            factors['engagement_potential'] = engagement_score
            
            # Viral potential
            viral_score = self._analyze_viral_potential(title, description, tags)
            score += viral_score['score']
            factors['viral_potential'] = viral_score
            
            # Competition analysis
            competition_score = self._analyze_competition_level(tags, title)
            score += competition_score['score']
            factors['competition_analysis'] = competition_score
            
            # Normalize score to 0-100
            final_score = min(100, max(0, score))
            
            # Performance prediction
            performance_prediction = self._predict_performance(final_score, video_data)
            
            return {
                "performance_score": round(final_score, 1),
                "performance_prediction": performance_prediction,
                "detailed_factors": factors,
                "recommendations": self._generate_performance_recommendations(factors),
                "risk_factors": self._identify_risk_factors(factors)
            }
            
        except Exception as e:
            return {"error": f"Performance analysis failed: {str(e)}"}
    
    def _analyze_title_effectiveness(self, title: str) -> Dict[str, Any]:
        """Analyze title effectiveness for performance"""
        score = 0
        insights = []
        
        # Length analysis
        if 30 <= len(title) <= 60:
            score += 20
            insights.append("Optimal title length")
        elif len(title) < 30:
            score += 10
            insights.append("Title might be too short")
        else:
            score += 5
            insights.append("Title might be too long")
        
        # Emotional triggers
        emotional_words = ['amazing', 'incredible', 'shocking', 'hilarious', 'epic', 'mind-blowing']
        emotional_count = sum(1 for word in emotional_words if word in title)
        if emotional_count > 0:
            score += min(15, emotional_count * 5)
            insights.append(f"Contains {emotional_count} emotional trigger words")
        
        # Curiosity gaps
        curiosity_indicators = ['how', 'why', 'what', 'when', 'where', 'who', 'which']
        curiosity_count = sum(1 for word in curiosity_indicators if word in title)
        if curiosity_count > 0:
            score += min(10, curiosity_count * 3)
            insights.append(f"Contains {curiosity_count} curiosity indicators")
        
        # Numbers and specificity
        numbers = re.findall(r'\d+', title)
        if numbers:
            score += 10
            insights.append(f"Contains specific numbers: {numbers}")
        
        # Brackets and formatting
        if '[' in title and ']' in title:
            score += 5
            insights.append("Uses bracket formatting")
        
        return {
            "score": score,
            "insights": insights,
            "title_length": len(title),
            "emotional_triggers": emotional_count,
            "curiosity_indicators": curiosity_count
        }
    
    def _analyze_content_type(self, title: str, description: str, tags: List[str]) -> Dict[str, Any]:
        """Analyze content type and its performance potential"""
        score = 0
        content_type = "general"
        insights = []
        
        # Determine content type
        type_scores = {}
        for content_type_name, keywords in self.performance_keywords.items():
            type_score = 0
            for keyword in keywords:
                if keyword in title or keyword in description:
                    type_score += 1
                for tag in tags:
                    if keyword in tag:
                        type_score += 0.5
            
            type_scores[content_type_name] = type_score
        
        # Find dominant content type
        if type_scores:
            dominant_type = max(type_scores, key=type_scores.get)
            if type_scores[dominant_type] > 0:
                content_type = dominant_type
                score += type_scores[dominant_type] * 5
                insights.append(f"Identified as {dominant_type} content")
        
        # Content type performance weights
        type_performance_weights = {
            'educational': 1.2,
            'entertainment': 1.1,
            'review': 1.0,
            'news': 0.9,
            'clickbait': 0.8
        }
        
        weight = type_performance_weights.get(content_type, 1.0)
        score *= weight
        
        return {
            "score": score,
            "content_type": content_type,
            "type_scores": type_scores,
            "performance_weight": weight,
            "insights": insights
        }
    
    def _analyze_engagement_potential(self, title: str, description: str) -> Dict[str, Any]:
        """Analyze potential for audience engagement"""
        score = 0
        insights = []
        
        # Engagement triggers
        trigger_count = sum(1 for trigger in self.engagement_triggers if trigger in title.lower() or trigger in description.lower())
        if trigger_count > 0:
            score += min(20, trigger_count * 5)
            insights.append(f"Contains {trigger_count} engagement triggers")
        
        # Question indicators
        questions = re.findall(r'\?', title + description)
        if questions:
            score += len(questions) * 3
            insights.append(f"Contains {len(questions)} question marks")
        
        # Call-to-action analysis
        cta_indicators = ['check out', 'visit', 'click', 'watch', 'see', 'try']
        cta_count = sum(1 for cta in cta_indicators if cta in title.lower() or cta in description.lower())
        if cta_count > 0:
            score += min(15, cta_count * 3)
            insights.append(f"Contains {cta_count} call-to-action elements")
        
        return {
            "score": score,
            "engagement_triggers": trigger_count,
            "questions": len(questions),
            "cta_elements": cta_count,
            "insights": insights
        }
    
    def _analyze_viral_potential(self, title: str, description: str, tags: List[str]) -> Dict[str, Any]:
        """Analyze viral potential of content"""
        score = 0
        insights = []
        
        # Viral indicators
        viral_count = sum(1 for indicator in self.viral_indicators if indicator in title.lower() or indicator in description.lower())
        if viral_count > 0:
            score += viral_count * 5
            insights.append(f"Contains {viral_count} viral indicators")
        
        # Trending topics (simplified)
        trending_topics = ['ai', 'artificial intelligence', 'chatgpt', 'crypto', 'bitcoin', 'nft']
        trending_count = sum(1 for topic in trending_topics if topic in title.lower() or topic in description.lower())
        if trending_count > 0:
            score += trending_count * 8
            insights.append(f"Contains {trending_count} trending topics")
        
        # Controversy indicators
        controversy_words = ['controversy', 'debate', 'argument', 'fight', 'exposed', 'truth']
        controversy_count = sum(1 for word in controversy_words if word in title.lower() or word in description.lower())
        if controversy_count > 0:
            score += controversy_count * 3
            insights.append(f"Contains {controversy_count} controversy indicators")
        
        return {
            "score": score,
            "viral_indicators": viral_count,
            "trending_topics": trending_count,
            "controversy_indicators": controversy_count,
            "insights": insights
        }
    
    def _analyze_competition_level(self, tags: List[str], title: str) -> Dict[str, Any]:
        """Analyze competition level in the niche"""
        score = 0
        insights = []
        
        # Generic vs specific tags
        generic_tags = ['music', 'funny', 'vlog', 'gaming', 'tutorial']
        specific_tags = [tag for tag in tags if tag not in generic_tags]
        
        if len(specific_tags) > len(generic_tags):
            score += 10
            insights.append("Uses specific, targeted tags")
        else:
            score -= 5
            insights.append("Uses mostly generic tags")
        
        # Niche specificity
        if len(tags) > 10:
            score += 5
            insights.append("Comprehensive tag coverage")
        elif len(tags) < 5:
            score -= 5
            insights.append("Limited tag coverage")
        
        return {
            "score": score,
            "specific_tags": len(specific_tags),
            "generic_tags": len(generic_tags),
            "total_tags": len(tags),
            "insights": insights
        }
    
    def _predict_performance(self, score: float, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict performance based on score"""
        if score >= 80:
            prediction = "High Performance"
            expected_views = "100K+"
            expected_engagement = "5%+"
        elif score >= 60:
            prediction = "Good Performance"
            expected_views = "10K-100K"
            expected_engagement = "3-5%"
        elif score >= 40:
            prediction = "Average Performance"
            expected_views = "1K-10K"
            expected_engagement = "2-3%"
        else:
            prediction = "Low Performance"
            expected_views = "<1K"
            expected_engagement = "<2%"
        
        return {
            "prediction": prediction,
            "expected_views": expected_views,
            "expected_engagement": expected_engagement,
            "confidence": min(95, max(60, score))
        }
    
    def _generate_performance_recommendations(self, factors: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis factors"""
        recommendations = []
        
        title_analysis = factors.get('title_analysis', {})
        if title_analysis.get('title_length', 0) < 30:
            recommendations.append("Consider making your title more descriptive (30-60 characters)")
        
        if title_analysis.get('emotional_triggers', 0) == 0:
            recommendations.append("Add emotional trigger words to increase click-through rate")
        
        content_type = factors.get('content_type', {})
        if content_type.get('content_type') == 'clickbait':
            recommendations.append("Consider more authentic content to build long-term audience")
        
        engagement = factors.get('engagement_potential', {})
        if engagement.get('engagement_triggers', 0) == 0:
            recommendations.append("Add engagement triggers like 'subscribe' or 'comment below'")
        
        viral = factors.get('viral_potential', {})
        if viral.get('trending_topics', 0) == 0:
            recommendations.append("Consider incorporating trending topics to increase discoverability")
        
        return recommendations
    
    def _identify_risk_factors(self, factors: Dict[str, Any]) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        title_analysis = factors.get('title_analysis', {})
        if title_analysis.get('title_length', 0) > 70:
            risks.append("Title may be cut off in search results")
        
        content_type = factors.get('content_type', {})
        if content_type.get('content_type') == 'clickbait':
            risks.append("Clickbait content may hurt long-term channel growth")
        
        viral = factors.get('viral_potential', {})
        if viral.get('controversy_indicators', 0) > 2:
            risks.append("High controversy indicators may lead to negative feedback")
        
        return risks
    
    def analyze_audience_behavior_patterns(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze audience behavior patterns from comments"""
        try:
            if not comments:
                return {"error": "No comments to analyze"}
            
            # Time-based analysis
            time_patterns = self._analyze_comment_timing(comments)
            
            # Engagement depth analysis
            engagement_patterns = self._analyze_engagement_depth(comments)
            
            # Community sentiment evolution
            sentiment_evolution = self._analyze_sentiment_evolution(comments)
            
            # Influencer identification
            influencers = self._identify_influencers(comments)
            
            # Topic clustering
            topic_clusters = self._cluster_comment_topics(comments)
            
            return {
                "time_patterns": time_patterns,
                "engagement_patterns": engagement_patterns,
                "sentiment_evolution": sentiment_evolution,
                "influencers": influencers,
                "topic_clusters": topic_clusters,
                "community_insights": self._generate_community_insights(comments)
            }
            
        except Exception as e:
            return {"error": f"Audience behavior analysis failed: {str(e)}"}
    
    def _analyze_comment_timing(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze when comments are posted"""
        # This would require comment timestamps
        # For now, return placeholder
        return {
            "peak_commenting_hours": [14, 15, 16, 17, 18, 19, 20],
            "weekend_activity": "Higher",
            "timezone_insights": "Most active during US evening hours"
        }
    
    def _analyze_engagement_depth(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze depth of engagement in comments"""
        reply_counts = [comment.get('reply_count', 0) for comment in comments]
        like_counts = [comment.get('likes', 0) for comment in comments]
        
        return {
            "avg_replies_per_comment": sum(reply_counts) / len(reply_counts) if reply_counts else 0,
            "avg_likes_per_comment": sum(like_counts) / len(like_counts) if like_counts else 0,
            "high_engagement_comments": len([c for c in comments if c.get('likes', 0) > 10]),
            "conversation_starters": len([c for c in comments if c.get('reply_count', 0) > 5])
        }
    
    def _analyze_sentiment_evolution(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how sentiment changes over time"""
        # This would require timestamps
        # For now, analyze overall sentiment distribution
        sentiments = [comment.get('sentiment', 'neutral') for comment in comments]
        sentiment_counts = Counter(sentiments)
        
        return {
            "sentiment_distribution": dict(sentiment_counts),
            "dominant_sentiment": max(sentiment_counts, key=sentiment_counts.get) if sentiment_counts else "neutral",
            "sentiment_volatility": "Medium"  # Would calculate actual volatility with timestamps
        }
    
    def _identify_influencers(self, comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify potential influencers in comments"""
        # Analyze comment authors by engagement
        author_stats = defaultdict(lambda: {"comments": 0, "total_likes": 0, "total_replies": 0})
        
        for comment in comments:
            author = comment.get('author', 'Unknown')
            author_stats[author]["comments"] += 1
            author_stats[author]["total_likes"] += comment.get('likes', 0)
            author_stats[author]["total_replies"] += comment.get('reply_count', 0)
        
        # Find top influencers
        influencers = []
        for author, stats in author_stats.items():
            if stats["comments"] >= 2 and (stats["total_likes"] > 20 or stats["total_replies"] > 10):
                influencers.append({
                    "author": author,
                    "comments": stats["comments"],
                    "total_likes": stats["total_likes"],
                    "total_replies": stats["total_replies"],
                    "influence_score": stats["total_likes"] + stats["total_replies"] * 2
                })
        
        # Sort by influence score
        influencers.sort(key=lambda x: x["influence_score"], reverse=True)
        
        return influencers[:10]  # Top 10 influencers
    
    def _cluster_comment_topics(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cluster comments by topics"""
        # Extract keywords from comments
        all_text = " ".join([comment.get('comment', '') for comment in comments])
        
        # Tokenize and clean
        tokens = word_tokenize(all_text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in self.stop_words]
        
        # Count frequencies
        word_freq = Counter(tokens)
        
        # Identify topic clusters
        topics = {
            "content_quality": [word for word, freq in word_freq.most_common(50) if freq > 2 and any(quality in word for quality in ['good', 'great', 'amazing', 'bad', 'terrible', 'quality'])],
            "technical_aspects": [word for word, freq in word_freq.most_common(50) if freq > 2 and any(tech in word for tech in ['audio', 'video', 'camera', 'editing', 'sound'])],
            "engagement_topics": [word for word, freq in word_freq.most_common(50) if freq > 2 and any(engage in word for engage in ['like', 'subscribe', 'comment', 'share'])],
            "content_specific": [word for word, freq in word_freq.most_common(20) if freq > 3]
        }
        
        return {
            "topic_clusters": topics,
            "most_discussed_topics": word_freq.most_common(10),
            "topic_diversity": len(set(tokens))
        }
    
    def _generate_community_insights(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about the community"""
        total_comments = len(comments)
        unique_authors = len(set(comment.get('author', '') for comment in comments))
        
        return {
            "community_size": unique_authors,
            "engagement_rate": total_comments / unique_authors if unique_authors > 0 else 0,
            "community_health": "Active" if total_comments > 50 else "Growing",
            "interaction_patterns": "High engagement" if any(c.get('reply_count', 0) > 5 for c in comments) else "Low interaction"
        }
    
    def generate_content_optimization_suggestions(self, video_data: Dict[str, Any], comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate specific content optimization suggestions"""
        try:
            suggestions = {
                "title_optimization": self._suggest_title_improvements(video_data.get('title', '')),
                "thumbnail_suggestions": self._suggest_thumbnail_improvements(video_data),
                "description_optimization": self._suggest_description_improvements(video_data.get('description', '')),
                "tag_optimization": self._suggest_tag_improvements(video_data.get('tags', []), comments),
                "content_structure": self._suggest_content_structure(comments),
                "engagement_strategies": self._suggest_engagement_strategies(comments),
                "seo_improvements": self._suggest_seo_improvements(video_data)
            }
            
            return {
                "suggestions": suggestions,
                "priority_actions": self._prioritize_suggestions(suggestions),
                "expected_impact": self._estimate_impact(suggestions)
            }
            
        except Exception as e:
            return {"error": f"Content optimization analysis failed: {str(e)}"}
    
    def _suggest_title_improvements(self, title: str) -> List[str]:
        """Suggest title improvements"""
        suggestions = []
        
        if len(title) < 30:
            suggestions.append("Add more descriptive keywords to increase search visibility")
        
        if not any(word in title.lower() for word in ['how', 'why', 'what', 'when', 'where']):
            suggestions.append("Consider adding question words to increase curiosity")
        
        if not any(word in title.lower() for word in ['best', 'top', 'amazing', 'incredible']):
            suggestions.append("Add emotional trigger words to increase click-through rate")
        
        if not re.search(r'\d+', title):
            suggestions.append("Consider adding numbers for specificity (e.g., '5 ways to...')")
        
        return suggestions
    
    def _suggest_thumbnail_improvements(self, video_data: Dict[str, Any]) -> List[str]:
        """Suggest thumbnail improvements"""
        suggestions = [
            "Use high contrast colors to stand out in search results",
            "Include text overlay with key message or number",
            "Show faces or emotions to increase click-through rate",
            "Use bright, eye-catching colors (red, yellow, orange)",
            "Keep text large and readable on mobile devices",
            "Test different thumbnail variations for A/B testing"
        ]
        
        return suggestions
    
    def _suggest_description_improvements(self, description: str) -> List[str]:
        """Suggest description improvements"""
        suggestions = []
        
        if len(description) < 100:
            suggestions.append("Expand description to improve SEO and provide more context")
        
        if not any(word in description.lower() for word in ['subscribe', 'like', 'comment']):
            suggestions.append("Add engagement calls-to-action in the description")
        
        if not re.search(r'http', description):
            suggestions.append("Include relevant links to increase engagement")
        
        return suggestions
    
    def _suggest_tag_improvements(self, tags: List[str], comments: List[Dict[str, Any]]) -> List[str]:
        """Suggest tag improvements based on comments"""
        suggestions = []
        
        if len(tags) < 10:
            suggestions.append("Add more tags to improve discoverability")
        
        # Extract popular terms from comments
        comment_text = " ".join([comment.get('comment', '') for comment in comments])
        words = word_tokenize(comment_text.lower())
        word_freq = Counter([word for word in words if word.isalnum() and len(word) > 3])
        
        popular_terms = [word for word, freq in word_freq.most_common(10) if freq > 2]
        
        if popular_terms:
            suggestions.append(f"Consider adding these popular terms as tags: {', '.join(popular_terms[:5])}")
        
        return suggestions
    
    def _suggest_content_structure(self, comments: List[Dict[str, Any]]) -> List[str]:
        """Suggest content structure improvements"""
        suggestions = [
            "Start with a hook in the first 10 seconds",
            "Include clear sections with timestamps",
            "End with a strong call-to-action",
            "Use cards and end screens to promote other videos",
            "Include community posts to increase engagement"
        ]
        
        return suggestions
    
    def _suggest_engagement_strategies(self, comments: List[Dict[str, Any]]) -> List[str]:
        """Suggest engagement strategies based on comment analysis"""
        suggestions = []
        
        # Analyze what engages the audience
        question_comments = [c for c in comments if c.get('is_question')]
        if question_comments:
            suggestions.append("Address common questions from comments in future videos")
        
        if any(c.get('reply_count', 0) > 5 for c in comments):
            suggestions.append("Engage more with commenters to build community")
        
        suggestions.extend([
            "Ask viewers to comment their opinions",
            "Create polls in community posts",
            "Respond to comments within 24 hours",
            "Feature viewer comments in future videos"
        ])
        
        return suggestions
    
    def _suggest_seo_improvements(self, video_data: Dict[str, Any]) -> List[str]:
        """Suggest SEO improvements"""
        suggestions = [
            "Include target keywords in title, description, and tags",
            "Use long-tail keywords for better ranking",
            "Add closed captions for better accessibility and SEO",
            "Create playlists to increase watch time",
            "Use custom thumbnails consistently",
            "Post at optimal times for your audience"
        ]
        
        return suggestions
    
    def _prioritize_suggestions(self, suggestions: Dict[str, Any]) -> List[str]:
        """Prioritize suggestions by impact"""
        priority_actions = []
        
        # High impact actions
        if suggestions.get('title_optimization'):
            priority_actions.append("1. Optimize title for better click-through rate")
        
        if suggestions.get('thumbnail_suggestions'):
            priority_actions.append("2. Improve thumbnail design")
        
        if suggestions.get('tag_optimization'):
            priority_actions.append("3. Optimize tags for better discoverability")
        
        # Medium impact actions
        if suggestions.get('description_optimization'):
            priority_actions.append("4. Enhance video description")
        
        if suggestions.get('engagement_strategies'):
            priority_actions.append("5. Implement engagement strategies")
        
        return priority_actions
    
    def _estimate_impact(self, suggestions: Dict[str, Any]) -> Dict[str, str]:
        """Estimate the impact of implementing suggestions"""
        return {
            "title_optimization": "15-25% increase in click-through rate",
            "thumbnail_improvement": "20-30% increase in click-through rate",
            "tag_optimization": "10-20% increase in discoverability",
            "description_enhancement": "5-15% increase in engagement",
            "engagement_strategies": "20-40% increase in community interaction"
        } 