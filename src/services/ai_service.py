import openai
import json
from typing import Dict, List, Any, Optional
import logging
import os

class AIService:
    """AI service using OpenAI API for production use"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1000) -> str:
        """Generate a response using OpenAI"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            content = response.choices[0].message.content
            return content if content else "No response generated"
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        system_prompt = """You are a sentiment analysis expert. Analyze the sentiment of the given text and return a JSON response with:
        - sentiment: positive, negative, or neutral
        - confidence: 0.0 to 1.0
        - reasoning: brief explanation
        
        Return only valid JSON without any additional text."""
        
        prompt = f'Analyze the sentiment of: "{text}"'
        
        try:
            response = self.generate_response(prompt, system_prompt, max_tokens=200)
            # Try to extract JSON from response
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {
                    "sentiment": "neutral",
                    "confidence": 0.5,
                    "reasoning": "Could not parse AI response"
                }
        except Exception as e:
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "reasoning": f"Error: {str(e)}"
            }
    
    def categorize_comment(self, comment: str) -> Dict[str, Any]:
        """Categorize a comment"""
        system_prompt = """You are a YouTube comment categorization expert. Categorize the given comment and return a JSON response with:
        - category: question, feedback, spam, appreciation, criticism, suggestion, or other
        - confidence: 0.0 to 1.0
        - reasoning: brief explanation
        
        Return only valid JSON without any additional text."""
        
        prompt = f'Categorize this comment: "{comment}"'
        
        try:
            response = self.generate_response(prompt, system_prompt, max_tokens=200)
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {
                    "category": "other",
                    "confidence": 0.5,
                    "reasoning": "Could not parse AI response"
                }
        except Exception as e:
            return {
                "category": "other",
                "confidence": 0.5,
                "reasoning": f"Error: {str(e)}"
            }
    
    def generate_content(self, context: str, content_type: str) -> str:
        """Generate content based on context"""
        system_prompt = f"""You are a content creation expert specializing in {content_type}. 
        Generate engaging, relevant, and high-quality content based on the provided context.
        Be creative, informative, and audience-focused."""
        
        prompt = f"Generate {content_type} based on this context: {context}"
        
        return self.generate_response(prompt, system_prompt, max_tokens=500)
    
    def critique_and_improve(self, content: str, feedback_type: str = "general") -> Dict[str, Any]:
        """Critique and suggest improvements"""
        system_prompt = """You are a content critique expert. Analyze the given content and provide improvement suggestions. Return JSON with:
        - score: 1-10 rating
        - strengths: list of positive aspects
        - weaknesses: list of areas for improvement
        - suggestions: specific improvement recommendations
        
        Return only valid JSON without any additional text."""
        
        prompt = f"Critique this {feedback_type} content: {content}"
        
        try:
            response = self.generate_response(prompt, system_prompt, max_tokens=400)
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {
                    "score": 5,
                    "strengths": ["Content provided"],
                    "weaknesses": ["Could not analyze"],
                    "suggestions": ["Review content manually"]
                }
        except Exception as e:
            return {
                "score": 5,
                "strengths": ["Content provided"],
                "weaknesses": [f"Error: {str(e)}"],
                "suggestions": ["Review content manually"]
            }
    
    def generate_insights(self, data: Dict[str, Any], insight_type: str) -> Dict[str, Any]:
        """Generate insights from data"""
        system_prompt = f"""You are a YouTube analytics expert. Analyze the provided data and generate {insight_type} insights. 
        Return JSON with:
        - key_insights: list of main insights
        - recommendations: actionable recommendations
        - trends: identified patterns or trends
        - metrics: relevant metrics and their interpretation
        
        Return only valid JSON without any additional text."""
        
        prompt = f"Generate {insight_type} insights from this data: {json.dumps(data, indent=2)}"
        
        try:
            response = self.generate_response(prompt, system_prompt, max_tokens=600)
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {
                    "key_insights": ["Data analyzed"],
                    "recommendations": ["Review data manually"],
                    "trends": ["No trends identified"],
                    "metrics": {"status": "analysis_failed"}
                }
        except Exception as e:
            return {
                "key_insights": ["Analysis failed"],
                "recommendations": ["Review data manually"],
                "trends": ["No trends identified"],
                "metrics": {"error": str(e)}
            }
    
    def predict_performance(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict video performance based on various factors"""
        system_prompt = """You are a YouTube performance prediction expert. Analyze video data and predict performance. Return JSON with:
        - predicted_views: estimated view count range
        - predicted_engagement: estimated engagement rate
        - confidence: confidence level in prediction (0.0-1.0)
        - factors: key factors influencing prediction
        - recommendations: suggestions to improve performance
        
        Return only valid JSON without any additional text."""
        
        prompt = f"Predict performance for this video data: {json.dumps(video_data, indent=2)}"
        
        try:
            response = self.generate_response(prompt, system_prompt, max_tokens=400)
            if '{' in response and '}' in response:
                start = response.find('{')
                end = response.rfind('}') + 1
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {
                    "predicted_views": "Unknown",
                    "predicted_engagement": "Unknown",
                    "confidence": 0.5,
                    "factors": ["Limited data"],
                    "recommendations": ["Gather more data"]
                }
        except Exception as e:
            return {
                "predicted_views": "Unknown",
                "predicted_engagement": "Unknown",
                "confidence": 0.0,
                "factors": [f"Error: {str(e)}"],
                "recommendations": ["Fix data issues"]
            } 