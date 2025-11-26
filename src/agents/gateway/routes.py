"""
Gateway Routes - HTTP endpoint router.

This is a facade module that combines endpoint routers.
All endpoint logic has been moved to gateway/endpoints/ for better organization.

Single Responsibility: Combine and expose endpoint routers.
"""

from fastapi import APIRouter

from src.agents.gateway.endpoints.health import router as health_router
from src.agents.gateway.endpoints.chat import (
    router as chat_router,
    set_http_client,
)

# Combined router
router = APIRouter()
router.include_router(health_router)
router.include_router(chat_router)

__all__ = ["router", "set_http_client"]
