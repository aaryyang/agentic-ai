"""
Telegram Integration for external customer assistant
"""

import asyncio
from typing import Dict, Any, Optional, List
import structlog
from core.engine.core_agent import CoreAIAgent, AgentResponse

logger = structlog.get_logger(__name__)


class TelegramIntegration:
    """Integration with Telegram Bot API for customer support"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.agent = CoreAIAgent()
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
        logger.info("Telegram integration initialized")
    
    async def send_message(self, chat_id: str, text: str, 
                          parse_mode: str = "Markdown") -> Dict[str, Any]:
        """Send message via Telegram Bot API"""
        try:
            logger.info(f"Sending Telegram message to {chat_id}: {text[:50]}...")
            
            # Simulate Telegram API call
            response = {
                "ok": True,
                "result": {
                    "message_id": hash(text) % 10000,
                    "from": {
                        "id": 12345,
                        "is_bot": True,
                        "first_name": "AI Assistant",
                        "username": "ai_assistant_bot"
                    },
                    "chat": {
                        "id": int(chat_id),
                        "type": "private"
                    },
                    "date": 1719484800,
                    "text": text
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    async def handle_message(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming Telegram message"""
        try:
            message = update.get("message", {})
            chat_id = str(message.get("chat", {}).get("id"))
            user = message.get("from", {})
            text = message.get("text", "")
            message_id = message.get("message_id")
            
            logger.info(f"Processing Telegram message from {user.get('username', 'unknown')}: {text[:50]}...")
            
            # Handle commands
            if text.startswith("/"):
                return await self._handle_command(chat_id, text, user)
            
            # Process with AI agent
            context = {
                "platform": "telegram",
                "chat_id": chat_id,
                "user": user,
                "message_id": message_id
            }
            
            agent_response = await self.agent.process_message(
                message=text,
                user_id=chat_id,
                context=context
            )
            
            # Send response back
            if agent_response.success:
                await self.send_message(chat_id, agent_response.response)
            else:
                await self.send_message(
                    chat_id,
                    "I apologize, but I'm experiencing technical difficulties. Please try again in a moment."
                )
            
            return {
                "status": "processed",
                "chat_id": chat_id,
                "agent_response": agent_response.response,
                "actions_taken": agent_response.actions_taken
            }
            
        except Exception as e:
            logger.error(f"Error processing Telegram message: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _handle_command(self, chat_id: str, command: str, user: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Telegram bot commands"""
        try:
            command = command.lower().split()[0]
            
            command_responses = {
                "/start": f"Hello {user.get('first_name', 'there')}! I'm your AI assistant. How can I help you today?",
                "/help": """
Available commands:
/start - Start conversation
/help - Show this help message
/quote - Get a price quote
/services - View our services
/support - Get support
/status - Check system status

You can also just type your question and I'll do my best to help!
                """,
                "/quote": "I'd be happy to help you with a quote! Please tell me about your requirements and I'll provide pricing information.",
                "/services": """
Our main services include:
• CRM Solutions & Integration
• AI Agent Development
• Process Automation
• WhatsApp & Telegram Integration
• Custom Business Solutions

Which service interests you most?
                """,
                "/support": "I'm here to provide support! Please describe your issue or question, and I'll assist you right away.",
                "/status": "🟢 All systems operational\n📊 AI Agent: Online\n🔗 Integrations: Active\n⚡ Response time: <2 seconds"
            }
            
            response_text = command_responses.get(command, "Unknown command. Type /help to see available commands.")
            
            await self.send_message(chat_id, response_text)
            
            return {
                "status": "command_processed",
                "chat_id": chat_id,
                "command": command,
                "response_sent": True
            }
            
        except Exception as e:
            logger.error(f"Error handling command: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def send_inline_keyboard(self, chat_id: str, text: str, 
                                  keyboard: List[List[Dict[str, str]]]) -> Dict[str, Any]:
        """Send message with inline keyboard"""
        try:
            # Simulate sending inline keyboard
            response = {
                "ok": True,
                "result": {
                    "message_id": hash(text) % 10000,
                    "chat": {"id": int(chat_id)},
                    "text": text,
                    "reply_markup": {
                        "inline_keyboard": keyboard
                    }
                }
            }
            
            logger.info(f"Sent inline keyboard to {chat_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error sending inline keyboard: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    async def handle_callback_query(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Handle inline keyboard button clicks"""
        try:
            callback_query = update.get("callback_query", {})
            data = callback_query.get("data")
            chat_id = str(callback_query.get("message", {}).get("chat", {}).get("id"))
            user = callback_query.get("from", {})
            
            logger.info(f"Callback query from {user.get('username', 'unknown')}: {data}")
            
            # Answer callback query (remove loading state)
            await self._answer_callback_query(callback_query.get("id"))
            
            # Handle different callback actions
            response_text = await self._handle_callback_action(data, chat_id, user)
            
            # Send response
            await self.send_message(chat_id, response_text)
            
            return {
                "status": "callback_processed",
                "chat_id": chat_id,
                "callback_data": data,
                "response_sent": True
            }
            
        except Exception as e:
            logger.error(f"Error handling callback query: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _answer_callback_query(self, callback_query_id: str, text: str = None):
        """Answer callback query to remove loading state"""
        # In real implementation, this would call answerCallbackQuery API
        logger.info(f"Answered callback query {callback_query_id}")
    
    async def _handle_callback_action(self, data: str, chat_id: str, user: Dict[str, Any]) -> str:
        """Handle specific callback actions"""
        action_responses = {
            "get_quote": "Great! I'll help you get a quote. Please tell me about your specific requirements:",
            "view_services": "Here are our main services:\\n\\n🔧 CRM Solutions\\n🤖 AI Integration\\n⚡ Process Automation\\n📱 Chat Integration\\n\\nWhich one interests you?",
            "contact_sales": "I'll connect you with our sales team. Please provide your contact information and requirements.",
            "technical_support": "I'm here to help with technical support. What issue are you experiencing?",
            "more_info": "I'd be happy to provide more information. What specific area would you like to know more about?"
        }
        
        return action_responses.get(data, "Thank you for your selection. How can I assist you further?")
    
    async def send_document(self, chat_id: str, document_url: str, 
                           caption: str = None) -> Dict[str, Any]:
        """Send document to chat"""
        try:
            # Simulate document sending
            response = {
                "ok": True,
                "result": {
                    "message_id": hash(document_url) % 10000,
                    "chat": {"id": int(chat_id)},
                    "document": {
                        "file_name": "document.pdf",
                        "file_id": f"doc_{hash(document_url) % 1000:03d}"
                    },
                    "caption": caption
                }
            }
            
            logger.info(f"Sent document to {chat_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error sending document: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    async def send_quick_replies(self, chat_id: str, text: str) -> Dict[str, Any]:
        """Send message with quick reply options"""
        keyboard = [
            [
                {"text": "Get Quote", "callback_data": "get_quote"},
                {"text": "View Services", "callback_data": "view_services"}
            ],
            [
                {"text": "Contact Sales", "callback_data": "contact_sales"},
                {"text": "Support", "callback_data": "technical_support"}
            ],
            [
                {"text": "More Info", "callback_data": "more_info"}
            ]
        ]
        
        return await self.send_inline_keyboard(chat_id, text, keyboard)
    
    def setup_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Set up webhook for receiving updates"""
        try:
            # In real implementation, this would call setWebhook API
            logger.info(f"Setting up Telegram webhook: {webhook_url}")
            
            return {
                "ok": True,
                "result": True,
                "description": "Webhook was set"
            }
            
        except Exception as e:
            logger.error(f"Error setting up webhook: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status and health"""
        return {
            "integration": "telegram",
            "status": "active",
            "bot_token": "configured" if self.bot_token else "missing",
            "base_url": self.base_url
        }
