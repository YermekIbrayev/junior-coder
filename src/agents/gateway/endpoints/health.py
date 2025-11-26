"""
Health Endpoints - Health check and models list.

Single Responsibility: Provide service status and available models.
"""

from fastapi import APIRouter

from src.agents.gateway.config import GB10_URL, QDRANT_URL
from src.agents.gateway.registry import AGENTS

router = APIRouter()


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "agent-gateway",
        "agents": list(AGENTS.keys()),
        "gb10_url": GB10_URL,
        "qdrant_url": QDRANT_URL
    }


@router.get("/v1/models")
async def list_models():
    """List available agents as 'models'."""
    return {
        "object": "list",
        "data": [
            {
                "id": agent_id,
                "object": "model",
                "owned_by": "agent-gateway",
                "description": desc
            }
            for agent_id, desc in AGENTS.items()
        ]
    }


__all__ = ["router"]
