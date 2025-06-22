"""
Base Agent Class for YouTube Analytics AI System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
import os
from src.services.ai_service import AIService

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model_name: Optional[str] = None):
        # Use OpenAI by default for production, fallback to Ollama if needed
        if not model_name:
            # Check if OpenAI API key is available
            if os.getenv('OPENAI_API_KEY'):
                model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
            else:
                # Fallback to Ollama
                model_name = os.getenv('OLLAMA_MODEL', 'gemma3:latest')
        
        self.ai_service = AIService(model_name)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data and return results"""
        pass
    
    def log_activity(self, activity: str, data: Optional[Dict[str, Any]] = None):
        """Log agent activity"""
        self.logger.info(f"{self.__class__.__name__}: {activity}")
        if data:
            self.logger.debug(f"Data: {data}")
    
    def handle_error(self, error: Exception, context: str = ""):
        """Handle and log errors"""
        self.logger.error(f"Error in {self.__class__.__name__} - {context}: {str(error)}")
        return {"error": str(error), "context": context} 