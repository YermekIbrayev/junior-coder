"""
T117: Tools endpoint - Exposes available tool definitions.

Provides endpoints for discovering and invoking tools (indexer, todo).
"""

from typing import Any, Dict, List

from fastapi import APIRouter

from src.agents.indexer import INDEXER_TOOLS, dispatch_tool
from src.agents.todo import TODO_TOOLS, dispatch_todo_tool


router = APIRouter(prefix="/v1/tools", tags=["tools"])


@router.get("")
async def list_tools() -> Dict[str, Any]:
    """
    List all available tools from all categories.

    Returns:
        Dict with categorized tool definitions
    """
    all_tools = list(INDEXER_TOOLS) + list(TODO_TOOLS)
    return {
        "tools": all_tools,
        "count": len(all_tools),
        "categories": {
            "indexer": len(INDEXER_TOOLS),
            "todo": len(TODO_TOOLS),
        },
    }


@router.get("/indexer")
async def list_indexer_tools() -> Dict[str, Any]:
    """
    List indexer-specific tools.

    Returns:
        Dict with indexer tool definitions
    """
    return {
        "tools": INDEXER_TOOLS,
        "count": len(INDEXER_TOOLS),
    }


@router.get("/todo")
async def list_todo_tools() -> Dict[str, Any]:
    """
    List todo-specific tools for task management.

    Returns:
        Dict with todo tool definitions
    """
    return {
        "tools": TODO_TOOLS,
        "count": len(TODO_TOOLS),
    }


@router.post("/indexer/invoke")
async def invoke_indexer_tool(
    tool_name: str,
    arguments: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Invoke an indexer tool directly.

    Args:
        tool_name: Name of the tool to invoke
        arguments: Tool arguments

    Returns:
        Tool result
    """
    result = await dispatch_tool(tool_name, arguments)
    return result


@router.post("/todo/invoke")
async def invoke_todo_tool(
    tool_name: str,
    arguments: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Invoke a todo tool directly.

    Args:
        tool_name: Name of the tool to invoke (add_task, list_tasks, etc.)
        arguments: Tool arguments

    Returns:
        Tool result with success status
    """
    # dispatch_todo_tool is sync (fast in-memory operations)
    result = dispatch_todo_tool(tool_name, arguments)
    return result


__all__ = ["router"]
