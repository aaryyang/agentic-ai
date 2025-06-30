"""
Agent Delegation Tool for routing tasks to specialized agents
"""

from typing import Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger(__name__)


class AgentDelegationInput(BaseModel):
    """Input schema for agent delegation"""
    agent_type: str = Field(description="Type of agent to delegate to (sales, operations, quote, scheduler)")
    task: str = Field(description="Task to delegate to the specialist agent")
    context: Dict[str, Any] = Field(default={}, description="Additional context for the task")


class AgentDelegationTool(BaseTool):
    """Tool for delegating tasks to specialized agents"""
    
    name = "delegate_to_agent"
    description = "Delegate specific tasks to specialized agents based on their expertise"
    args_schema = AgentDelegationInput
    
    def __init__(self, agents: Dict[str, Any]):
        super().__init__()
        self.agents = agents
    
    def _run(self, agent_type: str, task: str, context: Dict[str, Any] = None) -> str:
        """Delegate task to specified agent"""
        try:
            if agent_type not in self.agents:
                return f"Unknown agent type: {agent_type}. Available agents: {list(self.agents.keys())}"
            
            logger.info(f"Delegating task to {agent_type} agent: {task[:100]}...")
            
            # In a real implementation, this would be async
            # For now, we'll return a simulated response
            agent_name = agent_type.capitalize()
            
            return f"{agent_name} Agent received the task: '{task}'. The agent will process this and provide a detailed response based on their specialized expertise in {agent_type} operations."
            
        except Exception as e:
            logger.error(f"Error delegating to {agent_type} agent: {str(e)}")
            return f"Error delegating task: {str(e)}"
