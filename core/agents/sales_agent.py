"""
Sales Agent - Specialized agent for sales pipeline management and lead handling
"""

import asyncio
from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import structlog

logger = structlog.get_logger(__name__)


class SalesAgent:
    """Specialized agent for sales operations and pipeline management"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Sales-specific tools will be added here
        self.tools = self._initialize_sales_tools()
        self.agent_executor = self._create_sales_agent()
        
        logger.info("SalesAgent initialized")
    
    def _initialize_sales_tools(self):
        """Initialize sales-specific tools"""
        from ..tools.sales_tools import (
            LeadQualificationTool,
            PipelineUpdateTool,
            DealAnalysisTool,
            ContactManagementTool
        )
        
        return [
            LeadQualificationTool(),
            PipelineUpdateTool(),
            DealAnalysisTool(),
            ContactManagementTool()
        ]
    
    def _create_sales_agent(self) -> AgentExecutor:
        """Create the sales specialist agent"""
        
        system_prompt = """
        You are a Sales Specialist AI assistant focused on sales pipeline management, 
        lead qualification, and deal progression. Your expertise includes:
        
        Key Responsibilities:
        - Lead qualification and scoring
        - Sales pipeline management and updates
        - Deal progression and forecasting
        - Contact relationship management
        - Sales activity tracking and follow-ups
        - Opportunity identification and development
        
        Sales Process Automation:
        - Automatically qualify incoming leads based on criteria
        - Update deal stages and probabilities
        - Schedule follow-up activities
        - Generate sales reports and insights
        - Identify upselling and cross-selling opportunities
        
        Communication Style:
        - Be consultative and solution-focused
        - Use sales terminology appropriately
        - Provide actionable recommendations
        - Focus on revenue impact and conversion metrics
        
        Always prioritize activities that drive revenue and improve conversion rates.
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
        """Process a sales-related task"""
        
        try:
            # Enhance task with context
            if context:
                enhanced_task = f"Context: {context}\n\nSales Task: {task}"
            else:
                enhanced_task = task
            
            result = await asyncio.to_thread(
                self.agent_executor.invoke,
                {"input": enhanced_task}
            )
            
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="sales",
                response=result["output"],
                actions_taken=self._extract_actions(result),
                metadata={"context": context, "task": task},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error in SalesAgent: {str(e)}")
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="sales",
                response=f"Error processing sales task: {str(e)}",
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
                actions.append(f"Sales: {action.tool} - {action.tool_input}")
        return actions
    
    async def qualify_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Qualify a lead based on standard criteria"""
        qualification_prompt = f"""
        Qualify this lead based on the following criteria:
        - Budget: Does the lead have budget for our solution?
        - Authority: Is the contact a decision maker?
        - Need: Does the lead have a clear need for our solution?
        - Timeline: What is their timeline for implementation?
        
        Lead Data: {lead_data}
        
        Provide a qualification score (1-10) and recommendations for next steps.
        """
        
        result = await self.process_task(qualification_prompt, {"lead_data": lead_data})
        return result
    
    async def update_deal_stage(self, deal_id: str, new_stage: str, 
                              probability: float = None) -> Dict[str, Any]:
        """Update deal stage and probability"""
        update_prompt = f"""
        Update deal {deal_id} to stage '{new_stage}'.
        {f'Set probability to {probability}%' if probability else ''}
        
        Ensure all required fields are updated and log the stage change.
        """
        
        result = await self.process_task(update_prompt, {
            "deal_id": deal_id,
            "new_stage": new_stage,
            "probability": probability
        })
        return result
    
    async def generate_sales_report(self, period: str = "month") -> Dict[str, Any]:
        """Generate sales performance report"""
        report_prompt = f"""
        Generate a comprehensive sales report for the last {period} including:
        - Pipeline value and changes
        - Conversion rates by stage
        - Top performing deals
        - Activities completed
        - Forecast for next period
        
        Format the report with key metrics and actionable insights.
        """
        
        result = await self.process_task(report_prompt, {"period": period})
        return result
