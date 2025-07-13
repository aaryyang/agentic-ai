"""
Core AI Agent - Simplified for Render Deployment
Direct Groq API integration without langchain dependencies
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
import structlog

# Import settings first
from config.settings import settings

# Initialize logger
logger = structlog.get_logger(__name__)

# Try to import Groq with error handling
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError as e:
    logger.error(f"Groq library not available: {e}")
    GROQ_AVAILABLE = False
    Groq = None

from pydantic import BaseModel


class AgentResponse(BaseModel):
    """Response from the AI agent"""
    response: str
    agent_type: str = "core"
    success: bool = True
    metadata: Dict[str, Any] = {}


class CoreAIAgent:
    """
    Core AI Agent using direct Groq API
    Simplified for reliable deployment
    """
    
    def __init__(self):
        """Initialize the core agent with Groq client"""
        try:
            if not GROQ_AVAILABLE:
                raise ValueError("Groq library is not available")
                
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required")
                
            # Initialize Groq client using environment variable approach
            # This is more compatible across different Groq client versions
            import os
            os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
            
            try:
                # Try simple initialization first
                self.groq_client = Groq()
                logger.info("Groq client initialized successfully (env var method)")
            except Exception as fallback_error:
                try:
                    # Fallback: try with explicit API key parameter
                    self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                    logger.info("Groq client initialized successfully (direct method)")
                except Exception as final_error:
                    logger.error(f"Both Groq initialization methods failed: {final_error}")
                    raise final_error
                    
            self.model = settings.GROQ_MODEL or "mixtral-8x7b-32768"
            self.conversation_memory = {}
            
            logger.info("Core AI Agent initialized successfully", model=self.model)
            
        except Exception as e:
            logger.error(f"Failed to initialize Core AI Agent: {str(e)}")
            # Don't raise the exception to allow the service to start
            self.groq_client = None
            self.model = "mixtral-8x7b-32768"
            self.conversation_memory = {}
            logger.warning("Core AI Agent initialized in fallback mode")
    
    async def process_message(
        self, 
        message: str, 
        user_id: str = "default", 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a message using the core AI agent
        
        Args:
            message: User's message
            user_id: Unique identifier for the user
            context: Optional context information
            
        Returns:
            AgentResponse with the AI's response
        """
        try:
            # Prepare conversation context
            conversation_context = self._build_conversation_context(message, user_id, context)
            
            # Call Groq API
            response = await self._call_groq_api(conversation_context)
            
            # Store in memory
            self._update_conversation_memory(user_id, message, response)
            
            # Determine agent type based on content
            agent_type = self._determine_agent_type(message, response)
            
            return AgentResponse(
                response=response,
                agent_type=agent_type,
                success=True,
                metadata={
                    "user_id": user_id,
                    "model": self.model,
                    "context_provided": bool(context)
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return AgentResponse(
                response=f"I apologize, but I encountered an error: {str(e)}",
                agent_type="core",
                success=False,
                metadata={"error": str(e)}
            )
    
    async def delegate_to_agent(
        self,
        agent_type: str,
        task: str,
        data: Optional[Dict[str, Any]] = None,
        user_id: str = "default"
    ) -> AgentResponse:
        """
        Delegate a task to a specialist agent
        
        Args:
            agent_type: Type of agent (sales, operations, quote, scheduler)
            task: Specific task to perform
            data: Additional data for the task
            user_id: User identifier
            
        Returns:
            AgentResponse from the specialist agent
        """
        try:
            # Create specialized prompt based on agent type
            specialist_prompt = self._create_specialist_prompt(agent_type, task, data)
            
            # Process with specialist context
            response = await self.process_message(
                specialist_prompt,
                user_id=user_id,
                context={"agent_type": agent_type, "task": task, "data": data}
            )
            
            # Update agent type in response
            response.agent_type = agent_type
            response.metadata.update({
                "delegated_task": task,
                "specialist_agent": agent_type
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Error delegating to {agent_type} agent: {str(e)}")
            return AgentResponse(
                response=f"Error in {agent_type} agent: {str(e)}",
                agent_type=agent_type,
                success=False,
                metadata={"error": str(e)}
            )
    
    def _build_conversation_context(
        self, 
        message: str, 
        user_id: str, 
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Build conversation context for the AI model"""
        
        # Get conversation history
        history = self.conversation_memory.get(user_id, [])
        
        # Build system prompt
        system_prompt = """You are an intelligent AI assistant specialized in CRM automation and business processes. You help with:

1. Sales: Lead qualification, pipeline management, deal analysis
2. Operations: Process automation, workflow optimization, task management  
3. Quotes: Pricing calculations, proposal generation, quote creation
4. Scheduling: Meeting coordination, calendar management, follow-ups

Provide helpful, professional responses tailored to business needs."""
        
        # Build conversation
        conversation = f"System: {system_prompt}\n\n"
        
        # Add context if provided
        if context:
            conversation += f"Context: {json.dumps(context, indent=2)}\n\n"
        
        # Add recent conversation history
        for entry in history[-5:]:  # Last 5 exchanges
            conversation += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n\n"
        
        # Add current message
        conversation += f"User: {message}\nAssistant:"
        
        return conversation
    
    async def _call_groq_api(self, conversation_context: str) -> str:
        """Call Groq API directly"""
        try:
            if not self.groq_client:
                raise Exception("Groq client not initialized - check API key configuration")
                
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": conversation_context}
                ],
                temperature=0.7,
                max_tokens=1500,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}")
            raise Exception(f"AI service temporarily unavailable: {str(e)}")
    
    def _update_conversation_memory(self, user_id: str, user_message: str, ai_response: str):
        """Update conversation memory for the user"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            "user": user_message,
            "assistant": ai_response
        })
        
        # Keep only last 10 exchanges to manage memory
        if len(self.conversation_memory[user_id]) > 10:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]
    
    def _determine_agent_type(self, message: str, response: str) -> str:
        """Determine which type of agent this interaction represents"""
        message_lower = message.lower()
        response_lower = response.lower()
        
        # Sales keywords
        if any(word in message_lower for word in ['lead', 'prospect', 'sale', 'deal', 'customer', 'revenue']):
            return 'sales'
        
        # Operations keywords  
        if any(word in message_lower for word in ['process', 'workflow', 'automate', 'task', 'operation']):
            return 'operations'
        
        # Quote keywords
        if any(word in message_lower for word in ['quote', 'price', 'cost', 'proposal', 'estimate']):
            return 'quote'
        
        # Scheduling keywords
        if any(word in message_lower for word in ['schedule', 'meeting', 'calendar', 'appointment', 'time']):
            return 'scheduler'
        
        return 'core'
    
    def _create_specialist_prompt(
        self, 
        agent_type: str, 
        task: str, 
        data: Optional[Dict[str, Any]]
    ) -> str:
        """Create a specialized prompt for different agent types"""
        
        prompts = {
            'sales': f"""As a Sales AI specialist, help with this task: {task}
            
            Focus on:
            - Lead qualification and scoring
            - Pipeline management
            - Deal progression strategies
            - Revenue optimization
            - Customer relationship building
            
            Data provided: {json.dumps(data, indent=2) if data else 'None'}
            
            Provide actionable sales insights and recommendations.""",
            
            'operations': f"""As an Operations AI specialist, help with this task: {task}
            
            Focus on:
            - Process automation
            - Workflow optimization  
            - Task management
            - Efficiency improvements
            - Resource allocation
            
            Data provided: {json.dumps(data, indent=2) if data else 'None'}
            
            Provide operational recommendations and process improvements.""",
            
            'quote': f"""As a Quote AI specialist, help with this task: {task}
            
            Focus on:
            - Pricing analysis
            - Quote generation
            - Proposal creation
            - Cost calculations
            - Competitive positioning
            
            Data provided: {json.dumps(data, indent=2) if data else 'None'}
            
            Provide pricing recommendations and quote strategies.""",
            
            'scheduler': f"""As a Scheduling AI specialist, help with this task: {task}
            
            Focus on:
            - Meeting coordination
            - Calendar management
            - Appointment scheduling
            - Follow-up planning
            - Time optimization
            
            Data provided: {json.dumps(data, indent=2) if data else 'None'}
            
            Provide scheduling recommendations and calendar strategies."""
        }
        
        return prompts.get(agent_type, f"Help with this task: {task}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "status": "active",
            "model": self.model,
            "active_conversations": len(self.conversation_memory),
            "api_available": bool(self.groq_client),
            "version": "2.0.0-simplified"
        }
    
    def clear_memory(self, user_id: Optional[str] = None):
        """Clear conversation memory for a user or all users"""
        if user_id:
            if user_id in self.conversation_memory:
                del self.conversation_memory[user_id]
        else:
            self.conversation_memory.clear()
    
    async def test_groq_connection(self) -> bool:
        """Test if Groq client is working"""
        try:
            if not self.groq_client:
                return False
                
            # Simple test API call
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return bool(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Groq connection test failed: {e}")
            return False
