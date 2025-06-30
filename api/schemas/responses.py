"""
Response schema definitions for API endpoints
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Standard response from AI agents"""
    success: bool
    response: str
    agent_type: str
    actions_taken: List[str]
    context: Dict[str, Any]


class StatusResponse(BaseModel):
    """System status response"""
    status: str
    message: str
    details: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    """Workflow execution response"""
    workflow_id: str
    status: str
    result: Dict[str, Any]
    execution_time: Optional[str] = None


class SessionResponse(BaseModel):
    """Chat session response"""
    session_id: str
    status: str
    data: Dict[str, Any]
