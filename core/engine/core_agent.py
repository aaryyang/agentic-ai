"""
Core AI Agent Framework
Updated to use Groq's Llama model instead of OpenAI
"""

import asyncio
import re
from typing import Dict, List, Optional, Any
from groq import Groq
from langchain.schema import HumanMessage, SystemMessage
import structlog
from pydantic import BaseModel

try:
    from config import settings
except ImportError:
    from config.settings import Settings
    settings = Settings()

logger = structlog.get_logger(__name__)


class AgentResponse(BaseModel):
    """Response model for agent interactions"""
    agent_type: str
    response: str
    actions_taken: List[str]
    metadata: Dict[str, Any]
    success: bool


class CoreAIAgent:
    """
    Simplified AI Agent orchestrator for Phase 2
    Focuses on basic agent functionality with external platform integrations
    """
    
    def __init__(self):
        # Initialize default attributes first to prevent AttributeError
        self.groq_client = None
        self.model = getattr(settings, 'GROQ_MODEL', 'llama3-70b-8192')
        self.temperature = getattr(settings, 'DEFAULT_AGENT_TEMPERATURE', 0.7)
        self.max_tokens = getattr(settings, 'MAX_TOKENS', 1000)
        self.conversation_memory: Dict[str, List[Dict[str, str]]] = {}
        self.agents = {"sales": {}, "operations": {}, "quote": {}, "scheduler": {}}
        
        try:
            # Initialize Groq client 
            if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
                try:
                    # Initialize Groq client with the updated version
                    self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                    logger.info("Groq client initialized successfully")
                except Exception as e:
                    logger.error(f"Groq client initialization failed: {e}")
                    self.groq_client = None
            else:
                logger.warning("GROQ_API_KEY not configured")
                self.groq_client = None
            
            # Initialize specialized agents (simplified)
            self.agents = {
                "sales": self._create_sales_agent(),
                "operations": self._create_operations_agent(),
                "quote": self._create_quote_agent(),
                "scheduler": self._create_scheduler_agent()
            }
            
            if self.groq_client is not None:
                logger.info("CoreAIAgent initialized successfully with Groq API")
            else:
                logger.info("CoreAIAgent initialized successfully in mock mode")
            
        except Exception as e:
            logger.error(f"Error initializing CoreAIAgent: {str(e)}")
            # groq_client is already None from default initialization
            logger.warning("Using mock mode due to initialization error")
    
    async def _call_groq_llm(self, messages: List[Dict[str, str]]) -> str:
        """Call Groq API with message history"""
        try:
            if self.groq_client is None:
                return "Mock response - Please configure GROQ_API_KEY for real responses"
            
            # Convert messages to Groq format
            groq_messages = []
            for msg in messages:
                if hasattr(msg, 'content'):
                    if hasattr(msg, 'type') and msg.type == 'system':
                        groq_messages.append({"role": "system", "content": msg.content})
                    else:
                        groq_messages.append({"role": "user", "content": msg.content})
                else:
                    groq_messages.append(msg)
            
            # Call Groq API
            completion = self.groq_client.chat.completions.create(
                model=getattr(self, 'model', 'llama3-70b-8192'),
                messages=groq_messages,
                temperature=getattr(self, 'temperature', 0.7),
                max_tokens=getattr(self, 'max_tokens', 1000),
                stream=False  # For now, using non-streaming
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            return f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"
    
    def _create_sales_agent(self) -> Dict[str, str]:
        """Create sales agent configuration"""
        return {
            "role": "Sales Specialist",
            "expertise": "Lead qualification, pipeline management, deal analysis",
            "tools": ["crm_query", "lead_qualification", "pipeline_update"]
        }
    
    def _create_operations_agent(self) -> Dict[str, str]:
        """Create operations agent configuration"""
        return {
            "role": "Operations Specialist", 
            "expertise": "Process automation, workflow optimization, task management",
            "tools": ["workflow_automation", "process_optimization", "task_management"]
        }
    
    def _create_quote_agent(self) -> Dict[str, str]:
        """Create quote agent configuration"""
        return {
            "role": "Quote Specialist",
            "expertise": "Pricing calculations, quote generation, proposal creation",
            "tools": ["pricing_calculator", "quote_generator", "proposal_creator"]
        }
    
    def _create_scheduler_agent(self) -> Dict[str, str]:
        """Create scheduler agent configuration"""
        return {
            "role": "Scheduler Specialist",
            "expertise": "Meeting scheduling, calendar management, follow-ups",
            "tools": ["calendar_management", "meeting_scheduler", "followup_automation"]
        }
    
    
    async def process_message(self, message: str, user_id: str = None, 
                            context: Dict[str, Any] = None) -> AgentResponse:
        """
        Process an incoming message and return a structured response
        """
        
        try:
            logger.info(f"Processing message from user {user_id}: {message[:100]}...")
            
            # If using mock mode (placeholder API key)
            if self.groq_client is None:
                return self._mock_response(message, user_id, context)
            
            # Add to conversation memory
            if user_id:
                if user_id not in self.conversation_memory:
                    self.conversation_memory[user_id] = []
                
                self.conversation_memory[user_id].append({
                    "role": "user",
                    "content": message,
                    "timestamp": "2025-06-28T10:00:00Z"
                })
                
                # Keep only last 10 messages
                if len(self.conversation_memory[user_id]) > 10:
                    self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]
            
            # Create system prompt
            system_prompt = self._get_system_prompt(context)
            
            # Get recent conversation for context
            recent_messages = []
            if user_id and user_id in self.conversation_memory:
                recent_messages = self.conversation_memory[user_id][-5:]  # Last 5 messages
            
            # Create messages for the LLM
            messages = [SystemMessage(content=system_prompt)]
            
            # Add recent conversation context
            for msg in recent_messages[:-1]:  # Exclude the current message
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Call Groq LLM
            response_content = await self._call_groq_llm(messages)
            
            # Format the response for better readability
            formatted_response = self._format_response(response_content)
            
            # Store response in memory
            if user_id:
                self.conversation_memory[user_id].append({
                    "role": "assistant", 
                    "content": formatted_response,
                    "timestamp": "2025-06-28T10:00:00Z"
                })
            
            # Determine actions taken based on message content (but don't show them)
            actions_taken = []  # Hide actions from user
            
            agent_response = AgentResponse(
                agent_type="core",
                response=formatted_response,
                actions_taken=actions_taken,
                metadata={
                    "user_id": user_id,
                    "context": context,
                    "model_used": getattr(self, 'model', 'unknown')
                },
                success=True
            )
            
            logger.info(f"Successfully processed message for user {user_id}")
            return agent_response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return AgentResponse(
                agent_type="core",
                response=f"I apologize, but I encountered an error while processing your request: {str(e)}",
                actions_taken=[],
                metadata={"error": str(e), "user_id": user_id},
                success=False
            )
    
    def _get_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """Generate system prompt based on context"""
        
        base_prompt = """
        You are AVA, an intelligent CRM assistant designed to help users automate workflows, 
        manage tasks, and streamline operations. You coordinate with specialized agents to 
        handle different aspects of CRM management.

        Your capabilities include:
        - Sales pipeline management and lead qualification
        - Operations task automation and process optimization  
        - Quote generation and pricing calculations
        - Meeting scheduling and calendar management
        - CRM data retrieval and updates

        When handling requests:
        1. Analyze the user's intent and determine the best approach
        2. Provide clear, actionable responses with proper formatting
        3. Use bullet points for lists (starting with -)
        4. Use numbered lists for step-by-step processes
        5. Ask follow-up questions when needed
        6. Be helpful, professional, and proactive
        7. Keep responses well-structured and easy to read

        Formatting guidelines:
        - Use simple text without markdown formatting
        - Start new bullet points on separate lines with -
        - Use numbered lists (1., 2., 3.) for sequences
        - Ask questions clearly and directly
        - Avoid excessive asterisks or special characters

        Available specialized areas:
        - Sales: Lead management, pipeline updates, deal tracking
        - Operations: Task automation, process workflows, data management
        - Quote: Pricing calculations, proposal generation, quote management
        - Scheduler: Meeting scheduling, calendar management, follow-up planning
        """
        
        # Add context-specific information
        if context:
            platform = context.get("platform")
            if platform == "whatsapp":
                base_prompt += "\n\nNote: This is a WhatsApp conversation. Keep responses concise and mobile-friendly."
            elif platform == "telegram":
                base_prompt += "\n\nNote: This is a Telegram conversation. You can use formatting like *bold* and _italic_."
            elif platform == "webchat":
                base_prompt += "\n\nNote: This is a web chat conversation. You can provide detailed responses."
        
        return base_prompt
    
    def _analyze_actions(self, user_message: str, response: str) -> List[str]:
        """Analyze what actions were taken based on the conversation"""
        actions = []
        
        # Simple keyword-based action detection
        user_lower = user_message.lower()
        response_lower = response.lower()
        
        if any(word in user_lower for word in ["quote", "pricing", "price", "cost"]):
            actions.append("quote_inquiry_processed")
        
        if any(word in user_lower for word in ["lead", "qualify", "prospect"]):
            actions.append("lead_management_discussed")
        
        if any(word in user_lower for word in ["schedule", "meeting", "appointment", "calendar"]):
            actions.append("scheduling_request_handled")
        
        if any(word in user_lower for word in ["automate", "workflow", "process"]):
            actions.append("automation_consultation_provided")
        
        if "follow up" in response_lower or "next steps" in response_lower:
            actions.append("follow_up_recommended")
        
        return actions if actions else ["general_assistance_provided"]
    
    
    def _mock_response(self, message: str, user_id: str = None, 
                      context: Dict[str, Any] = None) -> AgentResponse:
        """Provide mock responses when API key is not configured"""
        
        message_lower = message.lower()
        
        # Generate contextual mock responses
        if any(word in message_lower for word in ["quote", "pricing", "price"]):
            response = "I'd be happy to help you with pricing and quotes. Please provide details about your requirements, and I'll generate a comprehensive quote for you."
            actions = ["quote_assistance_offered"]
        
        elif any(word in message_lower for word in ["lead", "qualify", "prospect"]):
            response = "I can help you qualify leads using BANT criteria (Budget, Authority, Need, Timeline). Please share the lead details, and I'll provide a qualification assessment."
            actions = ["lead_qualification_offered"]
        
        elif any(word in message_lower for word in ["schedule", "meeting", "appointment"]):
            response = "I can help you schedule meetings and manage your calendar. Please let me know the meeting details, participants, and preferred time slots."
            actions = ["scheduling_assistance_offered"]
        
        elif any(word in message_lower for word in ["automate", "workflow", "process"]):
            response = "I can help you automate your business processes and create efficient workflows. What specific processes would you like to optimize?"
            actions = ["automation_consultation_offered"]
        
        elif any(word in message_lower for word in ["hello", "hi", "hey", "start"]):
            response = "Hello! I'm AVA, your AI CRM assistant. I can help you with sales management, lead qualification, quote generation, scheduling, and process automation. How can I assist you today?"
            actions = ["greeting_provided"]
        
        else:
            response = "I'm here to help you with CRM operations, sales processes, quote generation, and scheduling. Please let me know what you'd like assistance with!"
            actions = ["general_assistance_offered"]
        
        # Add platform-specific note
        platform = context.get("platform") if context else None
        if platform:
            response += f"\n\n(Note: Responding via {platform.title()} - Please configure OPENAI_API_KEY for full functionality)"
        
        return AgentResponse(
            agent_type="core",
            response=response,
            actions_taken=actions,
            metadata={
                "user_id": user_id,
                "context": context,
                "mode": "mock"
            },
            success=True
        )
    
    async def delegate_to_specialist(self, agent_type: str, task: str, 
                                   context: Dict[str, Any] = None) -> AgentResponse:
        """
        Delegate a specific task to a specialized agent
        """
        
        if agent_type not in self.agents:
            return AgentResponse(
                agent_type=agent_type,
                response=f"Unknown agent type: {agent_type}. Available agents: {list(self.agents.keys())}",
                actions_taken=[],
                metadata={"error": f"Invalid agent type: {agent_type}"},
                success=False
            )
        
        try:
            agent_config = self.agents[agent_type]
            
            # Create specialized prompt for the agent
            specialist_prompt = f"""
            You are a {agent_config['role']} with expertise in {agent_config['expertise']}.
            
            Task: {task}
            Context: {context or 'No additional context provided'}
            
            Please provide a detailed response based on your specialization.
            """
            
            # If we have a real Groq client, use it
            if self.groq_client is not None:
                messages = [
                    {"role": "system", "content": specialist_prompt},
                    {"role": "user", "content": task}
                ]
                
                response_text = await self._call_groq_llm(messages)
            else:
                # Mock response for specialist
                response_text = f"As a {agent_config['role']}, I would handle this task: {task}. "
                response_text += f"I'll use my expertise in {agent_config['expertise']} to provide the best solution."
            
            return AgentResponse(
                agent_type=agent_type,
                response=response_text,
                actions_taken=[f"{agent_type}_task_processed"],
                metadata={
                    "context": context,
                    "task": task,
                    "specialist": agent_config['role']
                },
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error delegating to {agent_type} agent: {str(e)}")
            return AgentResponse(
                agent_type=agent_type,
                response=f"Error processing task with {agent_type} agent: {str(e)}",
                actions_taken=[],
                metadata={"error": str(e)},
                success=False
            )
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status information about all agents"""
        return {
            "core_agent": "active",
            "api_configured": self.groq_client is not None,
            "model": getattr(self, 'model', 'unknown'),
            "specialized_agents": {
                name: "active" for name in self.agents.keys()
            },
            "conversation_users": len(self.conversation_memory),
            "mode": "full" if self.groq_client is not None else "mock"
        }
    
    def clear_memory(self, user_id: str = None):
        """Clear conversation memory"""
        if user_id:
            if user_id in self.conversation_memory:
                del self.conversation_memory[user_id]
                logger.info(f"Cleared memory for user {user_id}")
        else:
            self.conversation_memory.clear()
            logger.info("Cleared all conversation memory")
    
    def _format_response(self, response_text: str) -> str:
        """Format the response text for better readability"""
        
        # Remove markdown formatting
        text = response_text.replace("**", "").replace("*", "")
        
        # Simple but effective formatting
        # Replace common patterns that should be on new lines
        
        # Handle bullet points
        text = text.replace(' • ', '\n• ')
        text = text.replace(' - ', '\n• ')
        
        # Handle questions that should be on new lines
        text = text.replace('? ', '?\n')
        
        # Handle numbered lists
        for i in range(1, 10):
            text = text.replace(f' {i}. ', f'\n{i}. ')
        
        # Handle "For example:" type phrases
        text = text.replace(' For example:', '\n\nFor example:')
        text = text.replace(' To better assist', '\n\nTo better assist')
        text = text.replace(' The more information', '\n\nThe more information')
        
        # Clean up multiple newlines and spaces
        while '\n\n\n' in text:
            text = text.replace('\n\n\n', '\n\n')
        
        text = text.replace('  ', ' ')
        
        return text.strip()
