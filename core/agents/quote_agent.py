"""
Quote Agent - Specialized agent for pricing, quotations, and proposal generation
"""

import asyncio
from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import structlog

logger = structlog.get_logger(__name__)


class QuoteAgent:
    """Specialized agent for pricing and quote generation"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.tools = self._initialize_quote_tools()
        self.agent_executor = self._create_quote_agent()
        
        logger.info("QuoteAgent initialized")
    
    def _initialize_quote_tools(self):
        """Initialize quote-specific tools"""
        from ..tools.quote_tools import (
            PricingCalculatorTool,
            QuoteGeneratorTool,
            ProposalTool,
            DiscountTool
        )
        
        return [
            PricingCalculatorTool(),
            QuoteGeneratorTool(),
            ProposalTool(),
            DiscountTool()
        ]
    
    def _create_quote_agent(self) -> AgentExecutor:
        """Create the quote specialist agent"""
        
        system_prompt = """
        You are a Quote Specialist AI assistant focused on pricing, quotations, 
        and proposal generation. Your expertise includes:
        
        Key Responsibilities:
        - Dynamic pricing calculations based on multiple factors
        - Professional quote and proposal generation
        - Discount and pricing strategy optimization
        - Competitive pricing analysis
        - Contract terms and conditions management
        - Revenue optimization and margin analysis
        
        Pricing Capabilities:
        - Calculate complex pricing with multiple variables
        - Apply volume discounts and promotional pricing
        - Generate detailed cost breakdowns
        - Create professional proposals and quotes
        - Manage pricing approval workflows
        - Track quote conversion and win rates
        
        Communication Style:
        - Be precise and detail-oriented with numbers
        - Present pricing clearly and transparently
        - Focus on value proposition and ROI
        - Provide professional, polished documents
        
        Always ensure pricing accuracy and compliance with company policies.
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
        """Process a quote-related task"""
        
        try:
            if context:
                enhanced_task = f"Context: {context}\n\nQuote Task: {task}"
            else:
                enhanced_task = task
            
            result = await asyncio.to_thread(
                self.agent_executor.invoke,
                {"input": enhanced_task}
            )
            
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="quote",
                response=result["output"],
                actions_taken=self._extract_actions(result),
                metadata={"context": context, "task": task},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error in QuoteAgent: {str(e)}")
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="quote",
                response=f"Error processing quote task: {str(e)}",
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
                actions.append(f"Quote: {action.tool} - {action.tool_input}")
        return actions
    
    async def generate_quote(self, quote_request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed quote based on requirements"""
        quote_prompt = f"""
        Generate a comprehensive quote for the following request:
        {quote_request}
        
        Include:
        - Itemized pricing breakdown
        - Terms and conditions
        - Validity period
        - Payment terms
        - Delivery schedule
        - Total cost summary
        
        Ensure the quote is professional and competitive.
        """
        
        result = await self.process_task(quote_prompt, {"quote_request": quote_request})
        return result
    
    async def calculate_pricing(self, products: List[Dict[str, Any]], 
                              volume: int = 1, discount_type: str = None) -> Dict[str, Any]:
        """Calculate pricing for products with volume and discounts"""
        pricing_prompt = f"""
        Calculate pricing for the following products:
        Products: {products}
        Volume: {volume}
        Discount Type: {discount_type}
        
        Apply appropriate volume discounts and calculate total cost.
        Provide detailed breakdown of pricing components.
        """
        
        result = await self.process_task(pricing_prompt, {
            "products": products,
            "volume": volume,
            "discount_type": discount_type
        })
        return result
    
    async def create_proposal(self, client_info: Dict[str, Any], 
                            solution_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive business proposal"""
        proposal_prompt = f"""
        Create a business proposal for:
        Client: {client_info}
        Solution: {solution_details}
        
        Include:
        - Executive summary
        - Solution overview
        - Implementation timeline
        - Pricing and investment
        - Terms and next steps
        
        Make it compelling and professional.
        """
        
        result = await self.process_task(proposal_prompt, {
            "client_info": client_info,
            "solution_details": solution_details
        })
        return result
