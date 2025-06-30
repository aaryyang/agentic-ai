"""
Workflow Automation System for AI Agent
Handles complex multi-step workflows and process automation
"""

import asyncio
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import json
import structlog

from ..core.agent import CoreAIAgent

logger = structlog.get_logger(__name__)


class WorkflowStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class WorkflowStep:
    """Individual step in a workflow"""
    
    def __init__(self, step_id: str, step_type: str, parameters: Dict[str, Any]):
        self.step_id = step_id
        self.step_type = step_type
        self.parameters = parameters
        self.status = "pending"
        self.result = None
        self.error = None
        self.executed_at = None


class Workflow:
    """Workflow definition and execution"""
    
    def __init__(self, workflow_id: str, name: str, steps: List[Dict[str, Any]], 
                 trigger_type: str = "manual", schedule: str = None):
        self.workflow_id = workflow_id
        self.name = name
        self.status = WorkflowStatus.CREATED
        self.trigger_type = trigger_type
        self.schedule = schedule
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.current_step = 0
        
        # Convert step dictionaries to WorkflowStep objects
        self.steps = []
        for i, step_data in enumerate(steps):
            step = WorkflowStep(
                step_id=f"step_{i+1}",
                step_type=step_data.get("type", "agent_task"),
                parameters=step_data.get("parameters", {})
            )
            self.steps.append(step)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary"""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "status": self.status.value,
            "trigger_type": self.trigger_type,
            "schedule": self.schedule,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "steps": [
                {
                    "step_id": step.step_id,
                    "step_type": step.step_type,
                    "status": step.status,
                    "executed_at": step.executed_at.isoformat() if step.executed_at else None
                }
                for step in self.steps
            ]
        }


class WorkflowAutomation:
    """Main workflow automation engine"""
    
    def __init__(self, ai_agent: CoreAIAgent):
        self.ai_agent = ai_agent
        self.workflows: Dict[str, Workflow] = {}
        self.running_workflows: Dict[str, asyncio.Task] = {}
        
        logger.info("WorkflowAutomation initialized")
    
    async def create_workflow(self, name: str, steps: List[Dict[str, Any]], 
                            trigger_type: str = "manual", schedule: str = None) -> str:
        """Create a new workflow"""
        try:
            workflow_id = str(uuid.uuid4())
            
            workflow = Workflow(
                workflow_id=workflow_id,
                name=name,
                steps=steps,
                trigger_type=trigger_type,
                schedule=schedule
            )
            
            self.workflows[workflow_id] = workflow
            
            logger.info(f"Created workflow: {name} ({workflow_id})")
            
            # If it's a scheduled workflow, set up the schedule
            if trigger_type == "scheduled" and schedule:
                await self._schedule_workflow(workflow_id, schedule)
            
            return workflow_id
            
        except Exception as e:
            logger.error(f"Error creating workflow: {str(e)}")
            raise
    
    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a workflow"""
        try:
            if workflow_id not in self.workflows:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            workflow = self.workflows[workflow_id]
            
            if workflow.status == WorkflowStatus.RUNNING:
                return {"status": "already_running", "workflow_id": workflow_id}
            
            # Start workflow execution
            workflow.status = WorkflowStatus.RUNNING
            workflow.started_at = datetime.now()
            workflow.current_step = 0
            
            logger.info(f"Starting workflow execution: {workflow.name}")
            
            # Execute steps sequentially
            for i, step in enumerate(workflow.steps):
                try:
                    workflow.current_step = i
                    await self._execute_step(step, workflow)
                    
                    if step.status == "failed":
                        workflow.status = WorkflowStatus.FAILED
                        logger.error(f"Workflow {workflow_id} failed at step {i+1}")
                        break
                        
                except Exception as e:
                    step.status = "failed"
                    step.error = str(e)
                    workflow.status = WorkflowStatus.FAILED
                    logger.error(f"Step {i+1} failed: {str(e)}")
                    break
            
            # Mark workflow as completed if all steps succeeded
            if all(step.status == "completed" for step in workflow.steps):
                workflow.status = WorkflowStatus.COMPLETED
                workflow.completed_at = datetime.now()
                logger.info(f"Workflow {workflow_id} completed successfully")
            
            return workflow.to_dict()
            
        except Exception as e:
            logger.error(f"Error executing workflow: {str(e)}")
            if workflow_id in self.workflows:
                self.workflows[workflow_id].status = WorkflowStatus.FAILED
            raise
    
    async def _execute_step(self, step: WorkflowStep, workflow: Workflow):
        """Execute an individual workflow step"""
        try:
            step.status = "running"
            step.executed_at = datetime.now()
            
            logger.info(f"Executing step: {step.step_id} ({step.step_type})")
            
            if step.step_type == "agent_task":
                # Delegate to AI agent
                agent_type = step.parameters.get("agent_type", "core")
                task = step.parameters.get("task", "")
                context = step.parameters.get("context", {})
                
                if agent_type == "core":
                    result = await self.ai_agent.process_message(
                        message=task,
                        user_id="workflow_system",
                        context=context
                    )
                else:
                    result = await self.ai_agent.delegate_to_specialist(
                        agent_type=agent_type,
                        task=task,
                        context=context
                    )
                
                step.result = result.dict()
                step.status = "completed" if result.success else "failed"
            
            elif step.step_type == "wait":
                # Wait for specified duration
                wait_seconds = step.parameters.get("seconds", 1)
                await asyncio.sleep(wait_seconds)
                step.result = {"waited_seconds": wait_seconds}
                step.status = "completed"
            
            elif step.step_type == "condition":
                # Conditional logic
                condition = step.parameters.get("condition", "")
                # Simple condition evaluation (in production, use safer evaluation)
                condition_result = eval(condition) if condition else True
                step.result = {"condition_met": condition_result}
                step.status = "completed"
            
            elif step.step_type == "notification":
                # Send notifications
                message = step.parameters.get("message", "")
                recipients = step.parameters.get("recipients", [])
                
                # Simulate notification sending
                step.result = {
                    "message_sent": message,
                    "recipients": recipients,
                    "sent_at": datetime.now().isoformat()
                }
                step.status = "completed"
            
            elif step.step_type == "data_operation":
                # Data operations (create, update, query)
                operation = step.parameters.get("operation", "query")
                target = step.parameters.get("target", "crm")
                data = step.parameters.get("data", {})
                
                # Use CRM tools through agent
                task = f"Perform {operation} operation on {target} with data: {data}"
                result = await self.ai_agent.process_message(
                    message=task,
                    user_id="workflow_system",
                    context={"operation": operation, "target": target, "data": data}
                )
                
                step.result = result.dict()
                step.status = "completed" if result.success else "failed"
            
            else:
                # Unknown step type
                step.status = "failed"
                step.error = f"Unknown step type: {step.step_type}"
            
            logger.info(f"Step {step.step_id} completed with status: {step.status}")
            
        except Exception as e:
            step.status = "failed"
            step.error = str(e)
            logger.error(f"Error executing step {step.step_id}: {str(e)}")
    
    async def _schedule_workflow(self, workflow_id: str, schedule: str):
        """Schedule a workflow for recurring execution"""
        # Simple scheduling implementation
        # In production, use a proper scheduler like Celery or APScheduler
        try:
            if schedule.startswith("every_"):
                interval_str = schedule.replace("every_", "")
                
                if interval_str.endswith("minutes"):
                    interval = int(interval_str.replace("minutes", "")) * 60
                elif interval_str.endswith("hours"):
                    interval = int(interval_str.replace("hours", "")) * 3600
                elif interval_str.endswith("days"):
                    interval = int(interval_str.replace("days", "")) * 86400
                else:
                    interval = 3600  # Default to 1 hour
                
                # Create background task for scheduled execution
                async def scheduled_execution():
                    while True:
                        await asyncio.sleep(interval)
                        try:
                            await self.execute_workflow(workflow_id)
                        except Exception as e:
                            logger.error(f"Scheduled workflow execution failed: {str(e)}")
                
                task = asyncio.create_task(scheduled_execution())
                self.running_workflows[workflow_id] = task
                
                logger.info(f"Scheduled workflow {workflow_id} to run {schedule}")
                
        except Exception as e:
            logger.error(f"Error scheduling workflow: {str(e)}")
    
    async def pause_workflow(self, workflow_id: str) -> bool:
        """Pause a running workflow"""
        try:
            if workflow_id in self.workflows:
                workflow = self.workflows[workflow_id]
                if workflow.status == WorkflowStatus.RUNNING:
                    workflow.status = WorkflowStatus.PAUSED
                    return True
            return False
        except Exception as e:
            logger.error(f"Error pausing workflow: {str(e)}")
            return False
    
    async def resume_workflow(self, workflow_id: str) -> bool:
        """Resume a paused workflow"""
        try:
            if workflow_id in self.workflows:
                workflow = self.workflows[workflow_id]
                if workflow.status == WorkflowStatus.PAUSED:
                    workflow.status = WorkflowStatus.RUNNING
                    # Resume from current step
                    await self.execute_workflow(workflow_id)
                    return True
            return False
        except Exception as e:
            logger.error(f"Error resuming workflow: {str(e)}")
            return False
    
    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [workflow.to_dict() for workflow in self.workflows.values()]
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow"""
        if workflow_id in self.workflows:
            return self.workflows[workflow_id].to_dict()
        return None
    
    async def get_status(self) -> Dict[str, Any]:
        """Get overall automation system status"""
        total_workflows = len(self.workflows)
        running_workflows = sum(1 for w in self.workflows.values() 
                              if w.status == WorkflowStatus.RUNNING)
        completed_workflows = sum(1 for w in self.workflows.values() 
                                if w.status == WorkflowStatus.COMPLETED)
        failed_workflows = sum(1 for w in self.workflows.values() 
                             if w.status == WorkflowStatus.FAILED)
        
        return {
            "total_workflows": total_workflows,
            "running": running_workflows,
            "completed": completed_workflows,
            "failed": failed_workflows,
            "scheduled": len(self.running_workflows),
            "system_status": "healthy"
        }
