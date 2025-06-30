"""
Operations Agent - Specialized agent for operational task automation and process management
"""

import asyncio
from typing import Dict, List, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import structlog

logger = structlog.get_logger(__name__)


class OperationsAgent:
    """Specialized agent for operations automation and process optimization"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.tools = self._initialize_operations_tools()
        self.agent_executor = self._create_operations_agent()
        
        logger.info("OperationsAgent initialized")
    
    def _initialize_operations_tools(self):
        """Initialize operations-specific tools"""
        from ..tools.operations_tools import (
            TaskAutomationTool,
            ProcessOptimizationTool,
            DataManagementTool,
            WorkflowTool
        )
        
        return [
            TaskAutomationTool(),
            ProcessOptimizationTool(),
            DataManagementTool(),
            WorkflowTool()
        ]
    
    def _create_operations_agent(self) -> AgentExecutor:
        """Create the operations specialist agent"""
        
        system_prompt = """
        You are an Operations Specialist AI assistant focused on process automation, 
        task management, and operational efficiency. Your expertise includes:
        
        Key Responsibilities:
        - Process automation and optimization
        - Task scheduling and management
        - Data cleaning and management
        - Workflow design and implementation
        - Performance monitoring and reporting
        - Resource allocation and planning
        
        Automation Capabilities:
        - Automate repetitive tasks and workflows
        - Set up recurring processes and schedules
        - Optimize resource utilization
        - Monitor system performance and health
        - Generate operational reports and insights
        - Implement quality control measures
        
        Communication Style:
        - Be systematic and process-oriented
        - Focus on efficiency and optimization
        - Provide clear step-by-step procedures
        - Emphasize measurable improvements and KPIs
        
        Always look for opportunities to streamline processes and reduce manual effort.
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
        """Process an operations-related task"""
        
        try:
            if context:
                enhanced_task = f"Context: {context}\n\nOperations Task: {task}"
            else:
                enhanced_task = task
            
            result = await asyncio.to_thread(
                self.agent_executor.invoke,
                {"input": enhanced_task}
            )
            
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="operations",
                response=result["output"],
                actions_taken=self._extract_actions(result),
                metadata={"context": context, "task": task},
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error in OperationsAgent: {str(e)}")
            from ..core.agent import AgentResponse
            return AgentResponse(
                agent_type="operations",
                response=f"Error processing operations task: {str(e)}",
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
                actions.append(f"Operations: {action.tool} - {action.tool_input}")
        return actions
    
    async def automate_workflow(self, workflow_name: str, 
                               steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Set up an automated workflow"""
        automation_prompt = f"""
        Create an automated workflow named '{workflow_name}' with the following steps:
        {steps}
        
        Set up the necessary triggers, conditions, and actions.
        Provide monitoring and error handling for the workflow.
        """
        
        result = await self.process_task(automation_prompt, {
            "workflow_name": workflow_name,
            "steps": steps
        })
        return result
    
    async def optimize_process(self, process_name: str, 
                             current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and optimize a business process"""
        optimization_prompt = f"""
        Analyze the process '{process_name}' with current metrics:
        {current_metrics}
        
        Identify bottlenecks, inefficiencies, and improvement opportunities.
        Provide specific recommendations with expected impact.
        """
        
        result = await self.process_task(optimization_prompt, {
            "process_name": process_name,
            "current_metrics": current_metrics
        })
        return result
    
    async def schedule_recurring_task(self, task_name: str, schedule: str, 
                                    task_config: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a recurring automated task"""
        scheduling_prompt = f"""
        Set up a recurring task '{task_name}' with schedule '{schedule}'.
        Task configuration: {task_config}
        
        Configure the task to run automatically and handle any errors gracefully.
        Set up monitoring and notifications for task execution.
        """
        
        result = await self.process_task(scheduling_prompt, {
            "task_name": task_name,
            "schedule": schedule,
            "task_config": task_config
        })
        return result
