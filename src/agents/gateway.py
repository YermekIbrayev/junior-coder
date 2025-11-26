"""
Agent Gateway - OpenAI-compatible API for AI Development Agents.

This is a facade module that re-exports from the refactored gateway package.
All functionality has been moved to src/agents/gateway/ for better organization.

Usage:
    # All these imports continue to work:
    from src.agents.gateway import app, run
    from src.agents.gateway import ChatRequest, ChatResponse, Message
    from src.agents.gateway import AGENTS, GB10_URL, QDRANT_URL

Run:
    python -m src.agents.gateway
"""

# Re-export everything from the gateway package for backward compatibility
from src.agents.gateway import (
    # FastAPI app and runner
    app,
    run,
    lifespan,
    http_client,

    # Pydantic models
    Message,
    ChatRequest,
    ChatResponse,

    # Agent registry
    AGENTS,

    # Helper functions
    create_error_response,
    generate_stream_response,
    get_memory_client,
    store_conversation_memory,

    # Configuration
    GB10_URL,
    QDRANT_URL,
    AGENT_PORT,
)

__all__ = [
    "app", "run", "lifespan", "http_client",
    "Message", "ChatRequest", "ChatResponse",
    "AGENTS",
    "create_error_response", "generate_stream_response",
    "get_memory_client", "store_conversation_memory",
    "GB10_URL", "QDRANT_URL", "AGENT_PORT",
]

if __name__ == "__main__":
    run()
