"""
Centralized logging configuration for Agent Gateway.

This is a facade module that re-exports from the refactored logging package.
All functionality has been moved to src/agents/logging/ for better organization.

Usage:
    from src.agents.logging_config import get_logger, set_request_context, LogEvent

    logger = get_logger("gateway")
    set_request_context(request_id="abc123", user_id="user-1")
    logger.info(LogEvent.REQUEST_RECEIVED, extra={"method": "POST"})
"""

# Re-export everything from the logging package for backward compatibility
from src.agents.logging import (
    # Context
    set_request_context,
    get_request_context,
    clear_request_context,

    # Formatters
    JSONFormatter,
    HumanReadableFormatter,

    # Setup
    setup_logging,
    get_logger,

    # Events
    LogEvent,
    log_with_duration,
)

__all__ = [
    "set_request_context",
    "get_request_context",
    "clear_request_context",
    "JSONFormatter",
    "HumanReadableFormatter",
    "setup_logging",
    "get_logger",
    "LogEvent",
    "log_with_duration",
]
