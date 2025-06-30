"""
Core agent API routes
"""

from fastapi import APIRouter, HTTPException
from ..schemas.requests import ChatRequest, DelegationRequest
from ..schemas.responses import AgentResponse, StatusResponse
import structlog
import importlib
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/agent", tags=["Core Agent"])


def import_core_agent():
    """Import CoreAIAgent with fallback paths"""
    import_paths = [
        "core.engine.core_agent",
        "core.agents.core_agent"
    ]
    
    for path in import_paths:
        try:
            module = importlib.import_module(path)
            return getattr(module, 'CoreAIAgent')
        except (ImportError, AttributeError):
            continue
    
    raise ImportError("Could not import CoreAIAgent from any expected location")


def import_integrations():
    """Import integrations with fallback paths"""
    import_paths = [
        "integrations"
    ]
    
    for base_path in import_paths:
        try:
            whatsapp_module = importlib.import_module(f"{base_path}.whatsapp_integration")
            telegram_module = importlib.import_module(f"{base_path}.telegram_integration")
            webchat_module = importlib.import_module(f"{base_path}.web_chat_integration")
            
            return (
                getattr(whatsapp_module, 'WhatsAppIntegration'),
                getattr(telegram_module, 'TelegramIntegration'),
                getattr(webchat_module, 'WebChatIntegration')
            )
        except (ImportError, AttributeError):
            continue
    
    return None, None, None


def import_settings():
    """Import settings with fallback paths"""
    import_paths = [
        "config",
        "config.settings"
    ]
    
    for path in import_paths:
        try:
            if path == "config.settings":
                module = importlib.import_module(path)
                Settings = getattr(module, 'Settings')
                return Settings()
            else:
                module = importlib.import_module(path)
                return getattr(module, 'settings')
        except (ImportError, AttributeError):
            continue
    
    # Fallback: create basic settings
    class BasicSettings:
        WHATSAPP_API_TOKEN = "not_configured"
        WHATSAPP_WEBHOOK_TOKEN = "not_configured"
        TELEGRAM_BOT_TOKEN = "not_configured"
    
    return BasicSettings()


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: ChatRequest):
    """Direct interaction with the core AI agent"""
    try:
        CoreAIAgent = import_core_agent()
        core_agent = CoreAIAgent()
        logger.info(f"Chat request from user {request.user_id}")
        
        response = await core_agent.process_message(
            message=request.message,
            user_id=request.user_id,
            context=request.context
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delegate", response_model=AgentResponse)
async def delegate_to_agent(request: DelegationRequest):
    """Delegate task to specialized agent"""
    try:
        CoreAIAgent = import_core_agent()
        core_agent = CoreAIAgent()
        logger.info(f"Delegation request: {request.agent_type}")
        
        response = await core_agent.delegate_to_agent(
            agent_type=request.agent_type,
            task=request.task,
            context=request.context
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error delegating to agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=StatusResponse)
async def get_agent_status():
    """Get agent system status"""
    try:
        # Import integrations and settings using helper functions
        WhatsAppIntegration, TelegramIntegration, WebChatIntegration = import_integrations()
        settings = import_settings()
        
        if not all([WhatsAppIntegration, TelegramIntegration, WebChatIntegration]):
            # Fallback: return basic status without integrations
            return StatusResponse(
                status="active",
                message="Agent system is running (integrations not available)",
                details={"note": "Integration modules not found"}
            )
        
        # Initialize integrations
        whatsapp_integration = WhatsAppIntegration(
            api_token=getattr(settings, 'WHATSAPP_API_TOKEN', 'not_configured'),
            webhook_verify_token=getattr(settings, 'WHATSAPP_WEBHOOK_TOKEN', 'not_configured')
        )
        telegram_integration = TelegramIntegration(getattr(settings, 'TELEGRAM_BOT_TOKEN', 'not_configured'))
        web_chat_integration = WebChatIntegration()
        
        # Get status from all integrations
        integrations_status = {
            "whatsapp": whatsapp_integration.get_integration_status(),
            "telegram": telegram_integration.get_integration_status(),
            "web_chat": web_chat_integration.get_integration_status()
        }
        
        return StatusResponse(
            status="active",
            message="Agent system is running",
            details={"integrations": integrations_status}
        )
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
