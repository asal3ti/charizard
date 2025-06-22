"""
Content Agent for generating social media posts and content
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent

class ContentAgent(BaseAgent):
    """Agent for generating social media content based on analytics"""
    
    def __init__(self, model_name: str = "gemma3:latest"):
        super().__init__(model_name)
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content based on analytics data"""
        try:
            analytics_data = data.get('analytics_data', {})
            content_type = data.get('content_type', 'social_post')
            
            self.log_activity("Generating content", {"content_type": content_type})
            
            # Generate content based on analytics
            content = self.generate_content(analytics_data, content_type)
            
            # Generate image description for the content
            image_prompt = self.generate_image_prompt(content, analytics_data)
            
            return {
                "content": content,
                "image_prompt": image_prompt,
                "content_type": content_type,
                "metadata": {
                    "generated_at": "2024-01-01T00:00:00Z",
                    "model_used": self.ai_service.model_name
                }
            }
            
        except Exception as e:
            return self.handle_error(e, "Content generation")
    
    def generate_content(self, analytics_data: Dict[str, Any], content_type: str) -> str:
        """Generate content based on analytics"""
        context = f"""
        Analytics Summary:
        - Video performance: {analytics_data.get('video_analytics', {})}
        - Comment insights: {analytics_data.get('comment_analysis', {})}
        - Transcript analysis: {analytics_data.get('transcript_analysis', {})}
        """
        
        return self.ai_service.generate_content(context, content_type)
    
    def generate_image_prompt(self, content: str, analytics_data: Dict[str, Any]) -> str:
        """Generate image prompt for the content"""
        prompt = f"""
        Based on this content and analytics, create an image prompt for generating a relevant image:
        
        Content: {content[:500]}...
        Analytics: {analytics_data}
        
        Generate a clear, descriptive image prompt that would create an engaging visual for this content.
        """
        
        return self.ai_service.generate_content(prompt, "image prompt") 