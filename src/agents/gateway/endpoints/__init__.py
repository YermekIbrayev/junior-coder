"""
Gateway Endpoints - HTTP endpoint handlers.

This package contains modular endpoint handlers:
- health.py: Health check and models list
- chat.py: Main chat completions endpoint
"""

from src.agents.gateway.endpoints.health import router as health_router
from src.agents.gateway.endpoints.chat import router as chat_router

__all__ = ["health_router", "chat_router"]
