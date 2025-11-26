"""
Agent Gateway - OpenAI-compatible API for AI Development Agents.

This package provides a modular gateway implementation:
- config.py: Environment-based configuration
- models.py: Pydantic request/response models
- registry.py: Agent registry
- responses.py: Error response helpers
- streaming.py: SSE streaming helpers
- memory.py: Memory client management
- routes.py: HTTP endpoint handlers

Usage:
    from src.agents.gateway import app, run
    run()  # Starts server on configured port
"""

from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

from src.agents.logging_config import setup_logging
from src.agents.gateway.config import AGENT_PORT, GB10_URL, QDRANT_URL, HTTP_TIMEOUT
from src.agents.gateway.models import Message, ChatRequest, ChatResponse
from src.agents.gateway.registry import AGENTS
from src.agents.gateway.responses import create_error_response
from src.agents.gateway.streaming import generate_stream_response
import src.agents.gateway.memory as _memory_module
from src.agents.gateway.memory import (
    get_memory_client, store_conversation_memory,
    set_http_client as set_memory_http_client,
    _reset_memory_client,
)
from src.agents.gateway.routes import router, set_http_client as set_routes_http_client

# Re-export orchestrator for backward compatibility (tests mock this)
from src.agents.orchestrator import run_orchestrator, OrchestratorResult


# Module-level attribute access for memory_client backward compatibility
# PEP 562: Python 3.7+ supports __getattr__ at module level (NOT __setattr__)
def __getattr__(name):
    """Handle attribute access for dynamic module attributes."""
    if name == "memory_client":
        return _memory_module._memory_client
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Initialize structured logging
setup_logging()

# Global HTTP client
http_client: httpx.AsyncClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup/shutdown."""
    global http_client
    http_client = httpx.AsyncClient(timeout=HTTP_TIMEOUT)

    # Wire up HTTP client to modules that need it
    set_routes_http_client(http_client)
    set_memory_http_client(http_client)

    yield

    await http_client.aclose()


# Create FastAPI application
app = FastAPI(
    title="Agent Gateway",
    description="OpenAI-compatible API for AI development agents",
    version="0.2.0",
    lifespan=lifespan
)

# Include routes
app.include_router(router)


def run():
    """Run the gateway server."""
    import uvicorn
    print(f"Agent Gateway starting on port {AGENT_PORT}")
    print(f"   GB10: {GB10_URL}")
    print(f"   Qdrant: {QDRANT_URL}")
    print(f"   Agents: {len(AGENTS)}")
    uvicorn.run(app, host="0.0.0.0", port=AGENT_PORT)


# Re-export for backward compatibility
__all__ = [
    # App and runner
    "app", "run", "lifespan", "http_client",
    # Models
    "Message", "ChatRequest", "ChatResponse",
    # Registry
    "AGENTS",
    # Helpers
    "create_error_response", "generate_stream_response",
    "get_memory_client", "store_conversation_memory",
    # Orchestrator (for tests)
    "run_orchestrator", "OrchestratorResult",
    # Config
    "GB10_URL", "QDRANT_URL", "AGENT_PORT",
]
