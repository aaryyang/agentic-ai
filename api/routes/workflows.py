"""
Workflow automation API routes
"""

from fastapi import APIRouter, HTTPException
from ..schemas.requests import WorkflowRequest
from ..schemas.responses import WorkflowResponse
from typing import Dict, Any, List
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.post("/create", response_model=WorkflowResponse)
async def create_workflow(request: WorkflowRequest):
    """Create new automation workflow"""
    try:
        from workflows.automation import WorkflowAutomation
        
        workflow_automation = WorkflowAutomation()
        
        workflow = await workflow_automation.create_workflow(
            name=request.workflow_name,
            steps=request.steps,
            trigger_type=request.trigger_type,
            parameters=request.parameters
        )
        
        return WorkflowResponse(
            workflow_id=workflow["id"],
            status="created",
            result=workflow
        )
        
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{workflow_id}/execute", response_model=WorkflowResponse)
async def execute_workflow(workflow_id: str, data: Dict[str, Any] = None):
    """Execute existing workflow"""
    try:
        from workflows.automation import WorkflowAutomation
        
        workflow_automation = WorkflowAutomation()
        
        result = await workflow_automation.execute_workflow(workflow_id, data)
        
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="completed",
            result=result
        )
        
    except Exception as e:
        logger.error(f"Error executing workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
async def list_workflows():
    """List all workflows"""
    try:
        from workflows.automation import WorkflowAutomation
        
        workflow_automation = WorkflowAutomation()
        workflows = await workflow_automation.list_workflows()
        return workflows
        
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
