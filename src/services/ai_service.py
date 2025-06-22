import ollama
import json
from typing import Dict, List, Any, Optional
import logging

class AIService:
    """Custom AI service using Ollama directly"""
    
    def __init__(self, model_name: str = "gemma3:latest"):
        self.model_name = model_name
        self.client = ollama.Client()
        
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response using Ollama"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat(model=self.model_name, messages=messages)
            return response['message']['content']
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        prompt = f"""
        Analyze the sentiment of the following text and return a JSON response with:
        - sentiment: positive, negative, or neutral
        - confidence: 0.0 to 1.0
        - reasoning: brief explanation
        
        Text: "{text}"
        
        Return only valid JSON.
        """
        
        try:
            response = self.generate_response(prompt)
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
        prompt = f"""
        Categorize the following YouTube comment and return a JSON response with:
        - category: question, feedback, spam, praise, criticism, suggestion, or other
        - confidence: 0.0 to 1.0
        - reasoning: brief explanation
        
        Comment: "{comment}"
        
        Return only valid JSON.
        """
        
        try:
            response = self.generate_response(prompt)
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
        prompt = f"""
        Based on the following context, generate {content_type}:
        
        Context: {context}
        
        Generate engaging and relevant {content_type}.
        """
        
        return self.generate_response(prompt)
    
    def critique_and_improve(self, content: str, feedback_type: str = "general") -> Dict[str, Any]:
        """Critique and suggest improvements"""
        prompt = f"""
        Critique the following content and provide improvement suggestions. Return JSON with:
        - score: 1-10 rating
        - strengths: list of positive aspects
        - weaknesses: list of areas for improvement
        - suggestions: specific improvement recommendations
        
        Content: {content}
        Feedback type: {feedback_type}
        
        Return only valid JSON.
        """
        
        try:
            response = self.generate_response(prompt)
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