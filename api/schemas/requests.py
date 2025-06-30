"""
Request schema definitions for API endpoints
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Schema for chat requests to the core agent"""
    message: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class DelegationRequest(BaseModel):
    """Schema for delegating tasks to specialized agents"""
    agent_type: str
    task: str
    context: Optional[Dict[str, Any]] = None


class WorkflowRequest(BaseModel):
    """Schema for workflow automation requests"""
    workflow_name: str
    steps: List[Dict[str, Any]]
    trigger_type: str = "manual"
    parameters: Optional[Dict[str, Any]] = None


class WebhookRequest(BaseModel):
    """Schema for webhook requests from external platforms"""
    platform: str
    data: Dict[str, Any]
    verification_token: Optional[str] = None


class SessionRequest(BaseModel):
    """Schema for chat session management"""
    session_id: str
    action: str
    data: Optional[Dict[str, Any]] = None
