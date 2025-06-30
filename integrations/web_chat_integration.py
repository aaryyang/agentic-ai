"""
Web Chat Integration for embedding in websites and customer portals
"""

import asyncio
from typing import Dict, Any, Optional, List
import structlog
from core.engine.core_agent import CoreAIAgent, AgentResponse

logger = structlog.get_logger(__name__)


class WebChatIntegration:
    """Integration for web-based chat widget and customer portal"""
    
    def __init__(self):
        self.agent = CoreAIAgent()
        self.active_sessions = {}  # Store active chat sessions
        
        logger.info("Web chat integration initialized")
    
    async def start_session(self, session_id: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start a new chat session"""
        try:
            session_data = {
                "session_id": session_id,
                "user_info": user_info or {},
                "start_time": "2025-06-27T10:00:00Z",
                "message_count": 0,
                "status": "active"
            }
            
            self.active_sessions[session_id] = session_data
            
            # Send welcome message
            welcome_message = await self._get_welcome_message(user_info)
            
            logger.info(f"Started web chat session: {session_id}")
            
            return {
                "session_id": session_id,
                "status": "started",
                "welcome_message": welcome_message,
                "session_data": session_data
            }
            
        except Exception as e:
            logger.error(f"Error starting chat session: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def handle_message(self, session_id: str, message: str, 
                           user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process incoming chat message"""
        try:
            if session_id not in self.active_sessions:
                await self.start_session(session_id, user_info)
            
            session = self.active_sessions[session_id]
            session["message_count"] += 1
            
            logger.info(f"Processing web chat message in session {session_id}: {message[:50]}...")
            
            # Prepare context
            context = {
                "platform": "web_chat",
                "session_id": session_id,
                "user_info": user_info or session.get("user_info", {}),
                "message_count": session["message_count"]
            }
            
            # Process with AI agent
            agent_response = await self.agent.process_message(
                message=message,
                user_id=session_id,
                context=context
            )
            
            # Update session
            session["last_message_time"] = "2025-06-27T10:00:00Z"
            
            response_data = {
                "session_id": session_id,
                "message": agent_response.response,
                "message_type": "text",
                "timestamp": "2025-06-27T10:00:00Z",
                "agent_type": agent_response.agent_type,
                "success": agent_response.success,
                "actions_taken": agent_response.actions_taken,
                "suggested_actions": await self._get_suggested_actions(message, agent_response)
            }
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error handling web chat message: {str(e)}")
            return {
                "session_id": session_id,
                "error": str(e),
                "message": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment.",
                "message_type": "error",
                "success": False
            }
    
    async def _get_welcome_message(self, user_info: Dict[str, Any] = None) -> str:
        """Generate personalized welcome message"""
        name = user_info.get("name") if user_info else None
        
        if name:
            return f"Hello {name}! 👋 I'm your AI assistant. I can help you with quotes, service information, scheduling, and general support. How can I assist you today?"
        else:
            return "Hello! 👋 Welcome to our AI assistant. I can help you with:\n\n• Getting quotes and pricing\n• Service information\n• Scheduling meetings\n• General support\n\nWhat would you like to know?"
    
    async def _get_suggested_actions(self, user_message: str, agent_response: AgentResponse) -> List[Dict[str, str]]:
        """Generate suggested actions based on conversation context"""
        
        # Analyze message intent to suggest relevant actions
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["price", "cost", "quote", "pricing"]):
            return [
                {"text": "Get Detailed Quote", "action": "get_quote"},
                {"text": "View Pricing Plans", "action": "view_pricing"},
                {"text": "Schedule Call", "action": "schedule_call"}
            ]
        elif any(word in message_lower for word in ["service", "solution", "product"]):
            return [
                {"text": "View All Services", "action": "view_services"},
                {"text": "Compare Solutions", "action": "compare_solutions"},
                {"text": "Request Demo", "action": "request_demo"}
            ]
        elif any(word in message_lower for word in ["meeting", "schedule", "call", "demo"]):
            return [
                {"text": "Schedule Meeting", "action": "schedule_meeting"},
                {"text": "Check Availability", "action": "check_availability"},
                {"text": "Calendar Integration", "action": "calendar_integration"}
            ]
        elif any(word in message_lower for word in ["help", "support", "issue", "problem"]):
            return [
                {"text": "Contact Support", "action": "contact_support"},
                {"text": "View Documentation", "action": "view_docs"},
                {"text": "Live Chat", "action": "live_chat"}
            ]
        else:
            return [
                {"text": "Get Quote", "action": "get_quote"},
                {"text": "View Services", "action": "view_services"},
                {"text": "Contact Sales", "action": "contact_sales"}
            ]
    
    async def handle_action(self, session_id: str, action: str, 
                           data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle suggested action clicks"""
        try:
            logger.info(f"Handling web chat action in session {session_id}: {action}")
            
            action_handlers = {
                "get_quote": self._handle_quote_request,
                "view_services": self._handle_services_request,
                "schedule_meeting": self._handle_meeting_request,
                "contact_support": self._handle_support_request,
                "view_pricing": self._handle_pricing_request,
                "request_demo": self._handle_demo_request
            }
            
            handler = action_handlers.get(action, self._handle_default_action)
            result = await handler(session_id, data)
            
            return {
                "session_id": session_id,
                "action": action,
                "result": result,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error handling action: {str(e)}")
            return {
                "session_id": session_id,
                "action": action,
                "error": str(e),
                "success": False
            }
    
    async def _handle_quote_request(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle quote request action"""
        return {
            "message": "I'd be happy to help you with a quote! Please provide some details about your requirements:",
            "form": {
                "fields": [
                    {"name": "company", "label": "Company Name", "type": "text", "required": True},
                    {"name": "email", "label": "Email", "type": "email", "required": True},
                    {"name": "requirements", "label": "Requirements", "type": "textarea", "required": True},
                    {"name": "timeline", "label": "Timeline", "type": "select", "options": ["ASAP", "1-3 months", "3-6 months", "6+ months"]}
                ]
            },
            "next_action": "process_quote_form"
        }
    
    async def _handle_services_request(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle services request action"""
        return {
            "message": "Here are our main services:",
            "services": [
                {
                    "name": "CRM AI Agent",
                    "description": "Intelligent CRM automation and customer support",
                    "features": ["Multi-agent architecture", "External platform integration", "Process automation"]
                },
                {
                    "name": "WhatsApp Integration",
                    "description": "Customer support via WhatsApp Business API",
                    "features": ["Automated responses", "Template messages", "Interactive buttons"]
                },
                {
                    "name": "Process Automation",
                    "description": "Streamline business workflows with AI",
                    "features": ["Task automation", "Workflow optimization", "Performance monitoring"]
                }
            ]
        }
    
    async def _handle_meeting_request(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle meeting scheduling action"""
        return {
            "message": "I'll help you schedule a meeting. Please select your preferences:",
            "calendar_widget": {
                "available_slots": [
                    "2025-06-28T10:00:00Z",
                    "2025-06-28T14:00:00Z",
                    "2025-06-29T09:00:00Z",
                    "2025-06-29T15:00:00Z"
                ],
                "meeting_types": [
                    {"type": "demo", "duration": 30, "title": "Product Demo"},
                    {"type": "consultation", "duration": 45, "title": "Consultation Call"},
                    {"type": "technical", "duration": 60, "title": "Technical Discussion"}
                ]
            }
        }
    
    async def _handle_support_request(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle support request action"""
        return {
            "message": "I'm here to help with support! Please describe your issue:",
            "support_options": [
                {"type": "technical", "title": "Technical Issue", "description": "Problems with functionality"},
                {"type": "billing", "title": "Billing Question", "description": "Questions about pricing or payments"},
                {"type": "general", "title": "General Inquiry", "description": "Other questions or feedback"}
            ],
            "escalation": {
                "available": True,
                "message": "If you need human assistance, I can connect you with our support team."
            }
        }
    
    async def _handle_pricing_request(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle pricing request action"""
        return {
            "message": "Here are our pricing plans:",
            "pricing_tiers": [
                {
                    "name": "Starter",
                    "price": "$299/month",
                    "features": ["Basic AI agent", "Up to 1000 conversations/month", "Email support"]
                },
                {
                    "name": "Professional",
                    "price": "$699/month",
                    "features": ["Advanced AI agent", "Up to 5000 conversations/month", "WhatsApp integration", "Priority support"]
                },
                {
                    "name": "Enterprise",
                    "price": "Custom",
                    "features": ["Full multi-agent system", "Unlimited conversations", "All integrations", "Dedicated support"]
                }
            ]
        }
    
    async def _handle_demo_request(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle demo request action"""
        return {
            "message": "Great! I'll set up a personalized demo for you.",
            "demo_form": {
                "fields": [
                    {"name": "name", "label": "Full Name", "type": "text", "required": True},
                    {"name": "company", "label": "Company", "type": "text", "required": True},
                    {"name": "role", "label": "Your Role", "type": "text", "required": True},
                    {"name": "use_case", "label": "Primary Use Case", "type": "select", 
                     "options": ["Customer Support", "Sales Automation", "Process Optimization", "Multi-channel Integration"]}
                ]
            },
            "next_action": "schedule_demo"
        }
    
    async def _handle_default_action(self, session_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle unknown actions"""
        return {
            "message": "I'll help you with that request. Please provide more details about what you need."
        }
    
    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """End chat session"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session["status"] = "ended"
                session["end_time"] = "2025-06-27T10:00:00Z"
                
                # Store session summary for analytics
                session_summary = {
                    "duration": "30 minutes",  # Calculate actual duration
                    "message_count": session.get("message_count", 0),
                    "resolution": "completed",
                    "satisfaction": "pending"
                }
                
                del self.active_sessions[session_id]
                
                logger.info(f"Ended web chat session: {session_id}")
                
                return {
                    "session_id": session_id,
                    "status": "ended",
                    "summary": session_summary
                }
            else:
                return {"error": "Session not found", "session_id": session_id}
                
        except Exception as e:
            logger.error(f"Error ending session: {str(e)}")
            return {"error": str(e), "session_id": session_id}
    
    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get information about active session"""
        return self.active_sessions.get(session_id, {"error": "Session not found"})
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status and health"""
        return {
            "integration": "web_chat",
            "status": "active",
            "active_sessions": len(self.active_sessions),
            "total_sessions": len(self.active_sessions)
        }
