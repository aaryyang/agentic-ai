"""
Webhook API routes for external platform integrations
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from ..schemas.requests import WebhookRequest
from typing import Dict, Any
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.get("/whatsapp")
async def whatsapp_webhook_verify(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """Verify WhatsApp webhook"""
    try:
        from integrations.whatsapp_integration import WhatsAppIntegration
        from config.settings import settings
        
        whatsapp_integration = WhatsAppIntegration(
            api_token=settings.WHATSAPP_API_TOKEN,
            webhook_verify_token=settings.WHATSAPP_WEBHOOK_TOKEN
        )
        
        challenge = whatsapp_integration.verify_webhook(
            mode=hub_mode,
            token=hub_verify_token,
            challenge=hub_challenge
        )
        return challenge
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"WhatsApp webhook verification error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/whatsapp")
async def whatsapp_webhook_handler(request: Request, background_tasks: BackgroundTasks):
    """Handle WhatsApp webhook events"""
    try:
        from integrations.whatsapp_integration import WhatsAppIntegration
        from config.settings import settings
        
        whatsapp_integration = WhatsAppIntegration(
            api_token=settings.WHATSAPP_API_TOKEN,
            webhook_verify_token=settings.WHATSAPP_WEBHOOK_TOKEN
        )
        
        webhook_data = await request.json()
        
        # Process in background to return quickly
        background_tasks.add_task(
            whatsapp_integration.handle_incoming_message,
            webhook_data
        )
        
        return JSONResponse(content={"status": "received"})
        
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/telegram")
async def telegram_webhook_handler(request: Request, background_tasks: BackgroundTasks):
    """Handle Telegram webhook events"""
    try:
        from integrations.telegram_integration import TelegramIntegration
        from config.settings import settings
        
        telegram_integration = TelegramIntegration(settings.TELEGRAM_BOT_TOKEN)
        
        update_data = await request.json()
        
        # Process in background
        background_tasks.add_task(
            telegram_integration.handle_message,
            update_data
        )
        
        return JSONResponse(content={"status": "received"})
        
    except Exception as e:
        logger.error(f"Telegram webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
