"""
Scheduler Agent - Specialized agent for meeting scheduling and calendar management
"""

import asyncio
from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import structlog

logger = structlog.get_logger(__name__)


class SchedulerAgent:
    """Specialized agent for scheduling and calendar management"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.tools = self._initialize_scheduler_tools()
        self.agent_executor = self._create_scheduler_agent()
        
        logger.info("SchedulerAgent initialized")
    
    def _initialize_scheduler_tools(self):
        """Initialize scheduler-specific tools"""
        from ..tools.scheduler_tools import (
            CalendarTool,
            MeetingSchedulerTool,
            FollowUpTool,
            AvailabilityTool
        )
        
        return [
            CalendarTool(),
            MeetingSchedulerTool(),
            FollowUpTool(),
            AvailabilityTool()
        ]
    
    def _create_scheduler_agent(self) -> AgentExecutor:
        """Create the scheduler specialist agent"""
        
        system_prompt = """
        You are a Scheduler Specialist AI assistant focused on meeting coordination, 
        calendar management, and follow-up scheduling. Your expertise includes:
        
        Key Responsibilities:
        - Meeting scheduling and coordination
        - Calendar management and optimization
        - Follow-up task scheduling
        - Availability checking and conflict resolution
        - Meeting preparation and logistics
        - Automated reminder and notification systems
        
        Scheduling Capabilities:
        - Find optimal meeting times across multiple calendars
        - Schedule recurring meetings and follow-ups
        - Manage meeting invitations and responses
        - Handle timezone coordination
        - Set up automated reminders and notifications
        - Reschedule meetings when conflicts arise
        
        Communication Style:
        - Be organized and detail-oriented
        - Confirm all scheduling details clearly
        - Provide alternatives when conflicts exist
        - Focus on efficiency and convenience for all parties
        
        Always double-check scheduling details and confirm availability before booking.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    async def process_task(self, task: str, context: Dict[str, Any] = None):
        """Process a scheduling-related task"""
        
        try:
            if context:
                enhanced_task = f"Context: {context}\n\nScheduling Task: {task}"
            else:
                enhanced_task = task
            
            result = await asyncio.to_thread(
                self.agent_executor.invoke,
                {"input": enhanced_task}
            )
            
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="scheduler",
                response=result["output"],
                actions_taken=self._extract_actions(result),
                metadata={"context": context, "task": task},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error in SchedulerAgent: {str(e)}")
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="scheduler",
                response=f"Error processing scheduling task: {str(e)}",
                actions_taken=[],
                metadata={"error": str(e)},
                success=False
            )
    
    def _extract_actions(self, result: Dict[str, Any]) -> List[str]:
        """Extract actions from execution result"""
        actions = []
        intermediate_steps = result.get("intermediate_steps", [])
        for step in intermediate_steps:
            if len(step) >= 2:
                action = step[0]
                actions.append(f"Scheduler: {action.tool} - {action.tool_input}")
        return actions
    
    async def schedule_meeting(self, meeting_details: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a meeting with multiple participants"""
        scheduling_prompt = f"""
        Schedule a meeting with the following details:
        {meeting_details}
        
        Check availability for all participants and find the best time slot.
        Send meeting invitations with agenda and logistics.
        Set up appropriate reminders.
        """
        
        result = await self.process_task(scheduling_prompt, {"meeting_details": meeting_details})
        return result
    
    async def check_availability(self, participants: List[str], 
                               duration: int, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Check availability for multiple participants"""
        availability_prompt = f"""
        Check availability for participants: {participants}
        Meeting duration: {duration} minutes
        Date range: {date_range}
        
        Find all available time slots and recommend the best options.
        Consider timezone differences if applicable.
        """
        
        result = await self.process_task(availability_prompt, {
            "participants": participants,
            "duration": duration,
            "date_range": date_range
        })
        return result
    
    async def schedule_follow_up(self, original_meeting: str, 
                               follow_up_type: str, delay_days: int) -> Dict[str, Any]:
        """Schedule a follow-up task or meeting"""
        follow_up_prompt = f"""
        Schedule a follow-up for meeting: {original_meeting}
        Follow-up type: {follow_up_type}
        Schedule for: {delay_days} days after the original meeting
        
        Create appropriate follow-up tasks or meeting invitations.
        Include relevant context from the original meeting.
        """
        
        result = await self.process_task(follow_up_prompt, {
            "original_meeting": original_meeting,
            "follow_up_type": follow_up_type,
            "delay_days": delay_days
        })
        return result
