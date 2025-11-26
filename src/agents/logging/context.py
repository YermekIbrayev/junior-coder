"""
Logging Context - Thread-safe request context tracking.

Single Responsibility: Manage request context for log enrichment.
"""

from contextvars import ContextVar
from typing import Optional

# Thread-safe request context using contextvars
_request_context: ContextVar[dict] = ContextVar("request_context", default={})


def set_request_context(
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs
) -> None:
    """Set request context for all subsequent log messages."""
    ctx = {
        "request_id": request_id,
        "user_id": user_id,
        "model": model,
        **kwargs
    }
    # Remove None values
    ctx = {k: v for k, v in ctx.items() if v is not None}
    _request_context.set(ctx)


def get_request_context() -> dict:
    """Get current request context."""
    return _request_context.get()


def clear_request_context() -> None:
    """Clear request context after request completes."""
    _request_context.set({})


__all__ = ["set_request_context", "get_request_context", "clear_request_context"]
