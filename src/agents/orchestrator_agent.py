"""
Orchestrator Agent for coordinating all agents
"""

from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.content_agent import ContentAgent
from src.agents.critique_agent import CritiqueAgent

class OrchestratorAgent(BaseAgent):
    """Agent for orchestrating the workflow between all other agents"""
    
    def __init__(self, api_key: str, model_name: str = "gemma3:latest"):
        super().__init__(model_name)
        self.analytics_agent = AnalyticsAgent(api_key, model_name)
        self.content_agent = ContentAgent(model_name)
        self.critique_agent = CritiqueAgent(model_name)
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate the complete workflow"""
        try:
            video_id = data.get('video_id')
            workflow_steps = data.get('workflow_steps', ['analytics', 'content', 'critique'])
            
            if not video_id:
                return self.handle_error(ValueError("Video ID is required"), "Missing video_id")
            
            self.log_activity("Starting orchestration", {"video_id": video_id, "steps": workflow_steps})
            
            results = {}
            
            # Step 1: Analytics
            if 'analytics' in workflow_steps:
                self.log_activity("Running analytics agent")
                analytics_result = self.analytics_agent.process({'video_id': video_id})
                results['analytics'] = analytics_result
            
            # Step 2: Content Generation
            if 'content' in workflow_steps:
                self.log_activity("Running content agent")
                content_result = self.content_agent.process({
                    'analytics_data': results.get('analytics', {}),
                    'content_type': data.get('content_type', 'social_post')
                })
                results['content'] = content_result
            
            # Step 3: Critique and Improvement
            if 'critique' in workflow_steps:
                self.log_activity("Running critique agent")
                critique_result = self.critique_agent.process({
                    'content': results.get('content', {}),
                    'content_type': data.get('content_type', 'general')
                })
                results['critique'] = critique_result
            
            # Generate final summary
            summary = self.generate_workflow_summary(results, workflow_steps)
            
            return {
                "workflow_steps": workflow_steps,
                "results": results,
                "summary": summary,
                "metadata": {
                    "video_id": video_id,
                    "model_used": self.ai_service.model_name,
                    "workflow_completed": True
                }
            }
            
        except Exception as e:
            return self.handle_error(e, "Workflow orchestration")
    
    def generate_workflow_summary(self, results: Dict[str, Any], workflow_steps: List[str]) -> str:
        """Generate a summary of the complete workflow"""
        context = f"""
        Workflow Summary:
        Steps completed: {workflow_steps}
        
        Analytics Results: {results.get('analytics', {}).get('summary', 'No analytics data')}
        Content Generated: {results.get('content', {}).get('content', 'No content generated')}
        Critique Applied: {results.get('critique', {}).get('improvements', 'No critique applied')}
        """
        
        return self.ai_service.generate_content(context, "workflow summary")
    
    def run_analytics_only(self, video_id: str) -> Dict[str, Any]:
        """Run only the analytics workflow"""
        return self.process({
            'video_id': video_id,
            'workflow_steps': ['analytics']
        })
    
    def run_content_generation(self, video_id: str, content_type: str = 'social_post') -> Dict[str, Any]:
        """Run analytics and content generation"""
        return self.process({
            'video_id': video_id,
            'workflow_steps': ['analytics', 'content'],
            'content_type': content_type
        })
    
    def run_full_workflow(self, video_id: str, content_type: str = 'social_post') -> Dict[str, Any]:
        """Run the complete workflow with critique"""
        return self.process({
            'video_id': video_id,
            'workflow_steps': ['analytics', 'content', 'critique'],
            'content_type': content_type
        }) 