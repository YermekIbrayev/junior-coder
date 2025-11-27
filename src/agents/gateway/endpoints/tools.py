"""
T117: Tools endpoint - Exposes available tool definitions.

Provides endpoints for discovering and invoking indexer tools.
"""

from typing import Any, Dict, List

from fastapi import APIRouter

from src.agents.indexer import INDEXER_TOOLS, dispatch_tool


router = APIRouter(prefix="/v1/tools", tags=["tools"])


@router.get("")
async def list_tools() -> Dict[str, Any]:
    """
    List all available tools.

    Returns:
        Dict with list of tool definitions
    """
    return {
        "tools": INDEXER_TOOLS,
        "count": len(INDEXER_TOOLS),
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


__all__ = ["router"]
