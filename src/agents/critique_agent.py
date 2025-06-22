"""
Critique Agent for reviewing and improving outputs
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent

class CritiqueAgent(BaseAgent):
    """Agent for critiquing and improving content using ReAct methodology"""
    
    def __init__(self, model_name: str = "gemma3:latest"):
        super().__init__(model_name)
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Critique and improve content"""
        try:
            content = data.get('content', {})
            content_type = data.get('content_type', 'general')
            
            self.log_activity("Starting critique", {"content_type": content_type})
            
            # Analyze the content
            critique = self.analyze_content(content, content_type)
            
            # Generate improvements
            improvements = self.generate_improvements(content, critique)
            
            # Create improved version
            improved_content = self.create_improved_version(content, improvements)
            
            return {
                "original_content": content,
                "critique": critique,
                "improvements": improvements,
                "improved_content": improved_content,
                "metadata": {
                    "critique_method": "ReAct",
                    "model_used": self.ai_service.model_name
                }
            }
            
        except Exception as e:
            return self.handle_error(e, "Content critique")
    
    def analyze_content(self, content: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Analyze content using ReAct methodology"""
        # Use our AI service to critique the content
        return self.ai_service.critique_and_improve(str(content), content_type)
    
    def generate_improvements(self, content: Dict[str, Any], critique: Dict[str, Any]) -> List[str]:
        """Generate specific improvement suggestions"""
        prompt = f"""
        Based on this critique, provide specific, actionable improvements:
        
        Content: {content}
        Critique: {critique}
        
        Provide 3-5 specific, actionable improvements that would enhance the content.
        """
        
        response = self.ai_service.generate_response(prompt)
        # Split response into individual improvements
        improvements = [line.strip() for line in response.split('\n') if line.strip()]
        return improvements
    
    def create_improved_version(self, content: Dict[str, Any], improvements: List[str]) -> Dict[str, Any]:
        """Create an improved version of the content"""
        prompt = f"""
        Create an improved version of this content incorporating these improvements:
        
        Original Content: {content}
        Improvements: {improvements}
        
        Generate the improved content that addresses all the suggested improvements.
        """
        
        improved_text = self.ai_service.generate_response(prompt)
        
        # Try to maintain the original structure
        if isinstance(content, dict):
            improved_content = content.copy()
            improved_content['improved_text'] = improved_text
            improved_content['improvements_applied'] = improvements
        else:
            improved_content = {
                'original': content,
                'improved_text': improved_text,
                'improvements_applied': improvements
            }
        
        return improved_content 