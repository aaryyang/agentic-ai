"""
Base Tool Interface for AI Agent Tools
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger(__name__)


class ToolResult(BaseModel):
    """Result from tool execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseTool(ABC):
    """
    Base class for all AI Agent tools
    
    This provides a common interface for tools that can be used by different agents
    in the multi-agent system.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = structlog.get_logger(f"{__name__}.{self.__class__.__name__}")
        
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ToolResult: Result of tool execution
        """
        pass
    
    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        Get the schema for tool parameters
        
        Returns:
            Dict describing the expected parameters
        """
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate parameters against schema
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            schema = self.get_parameters_schema()
            required_fields = schema.get("required", [])
            
            # Check required fields
            for field in required_fields:
                if field not in parameters:
                    self.logger.error(f"Missing required parameter: {field}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Parameter validation error: {str(e)}")
            return False
    
    async def safe_execute(self, **kwargs) -> ToolResult:
        """
        Safely execute tool with error handling
        
        Args:
            **kwargs: Tool parameters
            
        Returns:
            ToolResult: Execution result with error handling
        """
        try:
            # Validate parameters
            if not self.validate_parameters(kwargs):
                return ToolResult(
                    success=False,
                    error="Invalid parameters provided",
                    metadata={"tool": self.name}
                )
            
            # Execute tool
            result = await self.execute(**kwargs)
            
            self.logger.info(f"Tool {self.name} executed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Tool {self.name} execution failed: {str(e)}")
            return ToolResult(
                success=False,
                error=f"Tool execution failed: {str(e)}",
                metadata={"tool": self.name, "exception": str(e)}
            )
    
    def get_tool_info(self) -> Dict[str, Any]:
        """
        Get tool information for agent registration
        
        Returns:
            Dict with tool metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.get_parameters_schema(),
            "class": self.__class__.__name__
        }


class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.logger = structlog.get_logger(__name__)
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.tools.keys())
    
    def get_tools_info(self) -> List[Dict[str, Any]]:
        """Get information about all registered tools"""
        return [tool.get_tool_info() for tool in self.tools.values()]


# Global tool registry instance
tool_registry = ToolRegistry()
