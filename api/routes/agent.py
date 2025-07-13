"""
Core agent API routes
"""

import sys
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from ..schemas.requests import ChatRequest, DelegationRequest
from ..schemas.responses import AgentResponse, StatusResponse
import structlog

# Initialize router and logger
router = APIRouter()
logger = structlog.get_logger()

# Import auth dependency
from ..auth import verify_api_key

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Direct import of CoreAIAgent
try:
    from core.engine.core_agent import CoreAIAgent
    AGENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import CoreAIAgent: {e}")
    AGENT_AVAILABLE = False
    CoreAIAgent = None

# Initialize the core agent globally
try:
    core_agent = CoreAIAgent() if AGENT_AVAILABLE else None
    if core_agent:
        logger.info("Core agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize core agent: {e}")
    core_agent = None


@router.post("/chat", response_model=dict)
async def chat_with_agent(request: ChatRequest, _: bool = Depends(verify_api_key)):
    """
    Chat with the core AI agent
    """
    try:
        if not AGENT_AVAILABLE or core_agent is None:
            raise HTTPException(
                status_code=503, 
                detail="Core agent not available. Check server logs for import errors."
            )
            
        logger.info(f"Processing chat request from user: {request.user_id}")
        
        response = await core_agent.process_message(
            message=request.message,
            user_id=request.user_id,
            context=request.context or {}
        )
        
        return {
            "response": response.response,
            "agent_type": response.agent_type,
            "success": response.success,
            "metadata": response.metadata
        }
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.post("/delegate", response_model=dict) 
async def delegate_to_agent(request: DelegationRequest, _: bool = Depends(verify_api_key)):
    """
    Delegate a task to a specialist agent
    """
    try:
        if not AGENT_AVAILABLE or core_agent is None:
            raise HTTPException(
                status_code=503,
                detail="Core agent not available. Check server logs for import errors."
            )
            
        logger.info(f"Delegating task to {request.agent_type} agent")
        
        response = await core_agent.delegate_to_specialist(
            agent_type=request.agent_type,
            task=request.task,
            context=request.context or {}
        )
        
        return {
            "response": response.response,
            "agent_type": response.agent_type,
            "success": response.success,
            "metadata": response.metadata
        }
        
    except Exception as e:
        logger.error(f"Error delegating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error delegating task: {str(e)}")


@router.get("/status", response_model=dict)
async def get_agent_status():
    """
    Get the status of all agents
    """
    try:
        if not AGENT_AVAILABLE or core_agent is None:
            return {
                "status": "unavailable",
                "error": "Core agent not initialized",
                "core_agent": "unavailable",
                "api_configured": False,
                "mode": "error",
                "conversation_users": 0
            }
            
        # Get basic agent status
        status = {
            "status": "active",
            "core_agent": "initialized",
            "api_configured": True,
            "mode": "groq",
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "conversation_users": 0,  # Add this field for the dashboard
            "agents": {
                "sales": "available",
                "operations": "available", 
                "quote": "available",
                "scheduler": "available"
            },
            "integrations": {
                "whatsapp": "configured" if os.getenv("WHATSAPP_API_TOKEN") else "not_configured",
                "telegram": "configured" if os.getenv("TELEGRAM_BOT_TOKEN") else "not_configured",
                "web_chat": "available"
            }
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "core_agent": "error",
            "api_configured": False,
            "mode": "error",
            "conversation_users": 0
        }


@router.post("/clear-memory")
async def clear_agent_memory(user_id: str = None):
    """
    Clear conversation memory for a user or all users
    """
    try:
        if not AGENT_AVAILABLE or core_agent is None:
            raise HTTPException(
                status_code=503,
                detail="Core agent not available"
            )
            
        core_agent.clear_memory(user_id)
        
        return {
            "message": f"Memory cleared for {'user ' + user_id if user_id else 'all users'}",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error clearing memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")
