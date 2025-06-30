"""
WhatsApp Integration for external customer assistant
"""

import asyncio
from typing import Dict, Any, Optional, List
import structlog
from core.engine.core_agent import CoreAIAgent, AgentResponse

logger = structlog.get_logger(__name__)


class WhatsAppIntegration:
    """Integration with WhatsApp Business API for customer support"""
    
    def __init__(self, api_token: str, webhook_verify_token: str = None):
        self.api_token = api_token
        self.webhook_verify_token = webhook_verify_token
        self.agent = CoreAIAgent()
        self.base_url = "https://graph.facebook.com/v17.0"
        
        logger.info("WhatsApp integration initialized")
    
    async def send_message(self, phone_number: str, message: str, 
                          message_type: str = "text") -> Dict[str, Any]:
        """Send message via WhatsApp Business API"""
        try:
            # Simulate WhatsApp API call
            logger.info(f"Sending WhatsApp message to {phone_number}: {message[:50]}...")
            
            # In a real implementation, this would make an API call to Facebook Graph API
            response = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": message_type,
                "text": {"body": message} if message_type == "text" else message,
                "status": "sent",
                "message_id": f"wamid.{hash(message) % 10000:04d}"
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def handle_incoming_message(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming WhatsApp message"""
        try:
            # Extract message data from webhook
            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return {"status": "no_messages"}
            
            message = messages[0]
            phone_number = message.get("from")
            message_text = message.get("text", {}).get("body", "")
            message_id = message.get("id")
            
            logger.info(f"Processing WhatsApp message from {phone_number}: {message_text[:50]}...")
            
            # Process with AI agent
            context = {
                "platform": "whatsapp",
                "phone_number": phone_number,
                "message_id": message_id,
                "timestamp": message.get("timestamp")
            }
            
            agent_response = await self.agent.process_message(
                message=message_text,
                user_id=phone_number,
                context=context
            )
            
            # Send response back via WhatsApp
            if agent_response.success:
                await self.send_message(phone_number, agent_response.response)
            else:
                await self.send_message(
                    phone_number, 
                    "I apologize, but I'm experiencing technical difficulties. Please try again in a moment."
                )
            
            return {
                "status": "processed",
                "phone_number": phone_number,
                "agent_response": agent_response.response,
                "actions_taken": agent_response.actions_taken
            }
            
        except Exception as e:
            logger.error(f"Error processing WhatsApp message: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def send_template_message(self, phone_number: str, template_name: str, 
                                   parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send WhatsApp template message"""
        try:
            logger.info(f"Sending template {template_name} to {phone_number}")
            
            template_message = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "en"},
                    "components": []
                }
            }
            
            # Add parameters if provided
            if parameters:
                template_message["template"]["components"] = [
                    {
                        "type": "body",
                        "parameters": [{"type": "text", "text": str(value)} for value in parameters.values()]
                    }
                ]
            
            # Simulate API call
            response = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "message_id": f"wamid.template_{hash(template_name) % 1000:03d}",
                "status": "sent"
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending template message: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """Verify WhatsApp webhook"""
        if mode == "subscribe" and token == self.webhook_verify_token:
            logger.info("WhatsApp webhook verified successfully")
            return challenge
        else:
            logger.warning("WhatsApp webhook verification failed")
            return None
    
    async def send_interactive_message(self, phone_number: str, message_text: str, 
                                     buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        """Send interactive message with buttons"""
        try:
            interactive_message = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phone_number,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": message_text},
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": button["id"],
                                    "title": button["title"]
                                }
                            } for button in buttons[:3]  # WhatsApp supports max 3 buttons
                        ]
                    }
                }
            }
            
            # Simulate sending interactive message
            response = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "message_id": f"wamid.interactive_{hash(message_text) % 1000:03d}",
                "status": "sent"
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending interactive message: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    async def handle_button_response(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle button click responses"""
        try:
            # Extract button response data
            entry = webhook_data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return {"status": "no_messages"}
            
            message = messages[0]
            phone_number = message.get("from")
            interactive = message.get("interactive", {})
            button_reply = interactive.get("button_reply", {})
            button_id = button_reply.get("id")
            button_title = button_reply.get("title")
            
            logger.info(f"Button clicked by {phone_number}: {button_id} - {button_title}")
            
            # Process button response with appropriate action
            response_text = await self._handle_button_action(button_id, phone_number)
            
            # Send response
            await self.send_message(phone_number, response_text)
            
            return {
                "status": "button_processed",
                "phone_number": phone_number,
                "button_id": button_id,
                "response_sent": response_text
            }
            
        except Exception as e:
            logger.error(f"Error handling button response: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _handle_button_action(self, button_id: str, phone_number: str) -> str:
        """Handle specific button actions"""
        button_actions = {
            "get_quote": "I'll help you get a quote. Please tell me about your requirements.",
            "speak_to_agent": "Connecting you to a human agent. Please wait a moment.",
            "view_services": "Here are our main services: CRM Solutions, AI Integration, Process Automation.",
            "support": "I'm here to help! What support do you need today?",
            "more_info": "I'd be happy to provide more information. What would you like to know about?"
        }
        
        return button_actions.get(button_id, "Thank you for your selection. How can I assist you further?")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status and health"""
        return {
            "integration": "whatsapp",
            "status": "active",
            "api_token": "configured" if self.api_token else "missing",
            "webhook_token": "configured" if self.webhook_verify_token else "missing",
            "base_url": self.base_url
        }
