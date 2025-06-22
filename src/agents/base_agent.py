"""
Base Agent Class for YouTube Analytics AI System
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from src.services.ai_service import AIService

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model_name: str = "gemma3:latest"):
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