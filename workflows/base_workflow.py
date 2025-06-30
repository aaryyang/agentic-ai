"""
Base Workflow Interface for AI Agent Workflows
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Union
from pydantic import BaseModel, Field
from enum import Enum
import structlog
import asyncio

logger = structlog.get_logger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class WorkflowStep(BaseModel):
    """Individual workflow step"""
    step_id: str
    name: str
    description: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowResult(BaseModel):
    """Result from workflow execution"""
    workflow_id: str
    status: WorkflowStatus
    steps: List[WorkflowStep]
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    execution_time: Optional[float] = None


class BaseWorkflow(ABC):
    """
    Base class for all AI Agent workflows
    
    This provides a common interface for workflows that orchestrate
    multiple steps and tools to accomplish complex tasks.
    """
    
    def __init__(self, workflow_id: str, name: str, description: str):
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.logger = structlog.get_logger(f"{__name__}.{self.__class__.__name__}")
        self.steps: List[WorkflowStep] = []
        self.status = WorkflowStatus.PENDING
        
    @abstractmethod
    async def define_steps(self, **kwargs) -> List[WorkflowStep]:
        """
        Define the workflow steps
        
        Args:
            **kwargs: Workflow-specific parameters
            
        Returns:
            List[WorkflowStep]: Ordered list of workflow steps
        """
        pass
    
    @abstractmethod
    async def execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> WorkflowStep:
        """
        Execute a single workflow step
        
        Args:
            step: The step to execute
            context: Execution context and data
            
        Returns:
            WorkflowStep: Updated step with result
        """
        pass
    
    async def execute(self, **kwargs) -> WorkflowResult:
        """
        Execute the complete workflow
        
        Args:
            **kwargs: Workflow parameters
            
        Returns:
            WorkflowResult: Complete workflow execution result
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            self.status = WorkflowStatus.RUNNING
            self.logger.info(f"Starting workflow: {self.name}")
            
            # Define workflow steps
            self.steps = await self.define_steps(**kwargs)
            
            # Execution context
            context = {
                "workflow_id": self.workflow_id,
                "parameters": kwargs,
                "step_results": {}
            }
            
            # Execute steps sequentially
            for step in self.steps:
                try:
                    step.status = WorkflowStatus.RUNNING
                    self.logger.info(f"Executing step: {step.name}")
                    
                    # Execute the step
                    updated_step = await self.execute_step(step, context)
                    
                    # Update step in list
                    step_index = next(i for i, s in enumerate(self.steps) if s.step_id == step.step_id)
                    self.steps[step_index] = updated_step
                    
                    # Add result to context
                    context["step_results"][step.step_id] = updated_step.result
                    
                    if updated_step.status == WorkflowStatus.FAILED:
                        self.status = WorkflowStatus.FAILED
                        break
                        
                except Exception as e:
                    step.status = WorkflowStatus.FAILED
                    step.error = str(e)
                    self.status = WorkflowStatus.FAILED
                    self.logger.error(f"Step {step.name} failed: {str(e)}")
                    break
            
            # Determine final status
            if self.status != WorkflowStatus.FAILED:
                self.status = WorkflowStatus.COMPLETED
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Compile final result
            workflow_result = WorkflowResult(
                workflow_id=self.workflow_id,
                status=self.status,
                steps=self.steps,
                result=await self.compile_result(context),
                execution_time=execution_time,
                metadata={
                    "workflow_name": self.name,
                    "total_steps": len(self.steps),
                    "completed_steps": len([s for s in self.steps if s.status == WorkflowStatus.COMPLETED])
                }
            )
            
            self.logger.info(f"Workflow {self.name} completed with status: {self.status}")
            return workflow_result
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            self.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow {self.name} failed: {str(e)}")
            
            return WorkflowResult(
                workflow_id=self.workflow_id,
                status=WorkflowStatus.FAILED,
                steps=self.steps,
                error=str(e),
                execution_time=execution_time,
                metadata={"workflow_name": self.name}
            )
    
    async def compile_result(self, context: Dict[str, Any]) -> Any:
        """
        Compile the final workflow result from step results
        
        Args:
            context: Execution context with step results
            
        Returns:
            Any: Compiled workflow result
        """
        # Default implementation - return all step results
        return context.get("step_results", {})
    
    def get_workflow_info(self) -> Dict[str, Any]:
        """
        Get workflow information
        
        Returns:
            Dict with workflow metadata
        """
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "steps": len(self.steps),
            "class": self.__class__.__name__
        }
    
    async def pause(self):
        """Pause workflow execution"""
        self.status = WorkflowStatus.PAUSED
        self.logger.info(f"Workflow {self.name} paused")
    
    async def resume(self):
        """Resume workflow execution"""
        if self.status == WorkflowStatus.PAUSED:
            self.status = WorkflowStatus.RUNNING
            self.logger.info(f"Workflow {self.name} resumed")
    
    async def cancel(self):
        """Cancel workflow execution"""
        self.status = WorkflowStatus.CANCELLED
        self.logger.info(f"Workflow {self.name} cancelled")


class WorkflowRegistry:
    """Registry for managing available workflows"""
    
    def __init__(self):
        self.workflows: Dict[str, type] = {}
        self.logger = structlog.get_logger(__name__)
    
    def register_workflow(self, workflow_class: type, workflow_name: str = None):
        """Register a new workflow class"""
        name = workflow_name or workflow_class.__name__
        self.workflows[name] = workflow_class
        self.logger.info(f"Registered workflow: {name}")
    
    def create_workflow(self, workflow_type: str, workflow_id: str, **kwargs) -> Optional[BaseWorkflow]:
        """Create a workflow instance"""
        workflow_class = self.workflows.get(workflow_type)
        if workflow_class:
            return workflow_class(workflow_id=workflow_id, **kwargs)
        return None
    
    def list_workflows(self) -> List[str]:
        """Get list of available workflow types"""
        return list(self.workflows.keys())
    
    def get_workflows_info(self) -> List[Dict[str, Any]]:
        """Get information about all registered workflows"""
        info = []
        for name, workflow_class in self.workflows.items():
            info.append({
                "name": name,
                "class": workflow_class.__name__,
                "description": getattr(workflow_class, "__doc__", "No description available")
            })
        return info


# Global workflow registry instance
workflow_registry = WorkflowRegistry()
