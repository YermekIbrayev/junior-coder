"""
Logging Module - Centralized logging configuration for Agent Gateway.

This package provides modular logging infrastructure:
- context.py: Request context tracking
- formatters.py: JSON and human-readable formatters
- setup.py: Logger configuration
- events.py: Standard event constants

Usage:
    from src.agents.logging import get_logger, set_request_context, LogEvent

    logger = get_logger("gateway")
    set_request_context(request_id="abc123", user_id="user-1")
    logger.info(LogEvent.REQUEST_RECEIVED, extra={"method": "POST"})
"""

from src.agents.logging.context import (
    set_request_context,
    get_request_context,
    clear_request_context,
)
from src.agents.logging.formatters import (
    JSONFormatter,
    HumanReadableFormatter,
)
from src.agents.logging.setup import (
    setup_logging,
    get_logger,
)
from src.agents.logging.events import (
    LogEvent,
    log_with_duration,
)

__all__ = [
    # Context
    "set_request_context",
    "get_request_context",
    "clear_request_context",
    # Formatters
    "JSONFormatter",
    "HumanReadableFormatter",
    # Setup
    "setup_logging",
    "get_logger",
    # Events
    "LogEvent",
    "log_with_duration",
]
