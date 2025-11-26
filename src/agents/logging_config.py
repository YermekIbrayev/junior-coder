"""
Centralized logging configuration for Agent Gateway.

Provides structured JSON logging with request context tracking.

Usage:
    from src.agents.logging_config import get_logger, set_request_context

    logger = get_logger("gateway")
    set_request_context(request_id="abc123", user_id="user-1")
    logger.info("request_received", extra={"method": "POST", "path": "/v1/chat/completions"})
"""

import logging
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional
from contextvars import ContextVar

# =============================================================================
# Request Context (thread-safe via contextvars)
# =============================================================================

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


# =============================================================================
# JSON Formatter
# =============================================================================

class JSONFormatter(logging.Formatter):
    """
    Format log records as JSON for structured logging.

    Output format:
    {
        "timestamp": "2024-01-01T00:00:00.000Z",
        "level": "INFO",
        "component": "gateway",
        "event": "request_received",
        "request_id": "abc123",
        "user_id": "user-1",
        "data": {...}
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        # Base log entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "component": record.name.replace("src.agents.", ""),
            "event": record.getMessage(),
        }

        # Add request context
        ctx = get_request_context()
        if ctx:
            log_entry.update(ctx)

        # Add extra data from log call
        if hasattr(record, "__dict__"):
            extra_keys = set(record.__dict__.keys()) - {
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "exc_info", "exc_text", "thread", "threadName",
                "taskName", "message"
            }
            extra_data = {k: record.__dict__[k] for k in extra_keys}
            if extra_data:
                log_entry["data"] = extra_data

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


class HumanReadableFormatter(logging.Formatter):
    """
    Human-readable format for development/debugging.

    Output format:
    [2024-01-01 00:00:00] INFO [gateway] [req:abc123] request_received | method=POST path=/v1/chat
    """

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m"
    }

    def format(self, record: logging.LogRecord) -> str:
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Color based on level
        color = self.COLORS.get(record.levelname, "")
        reset = self.COLORS["RESET"]

        # Component name (shortened)
        component = record.name.replace("src.agents.", "")

        # Request context
        ctx = get_request_context()
        req_id = ctx.get("request_id", "-")[:8] if ctx.get("request_id") else "-"

        # Base message
        msg = f"[{timestamp}] {color}{record.levelname:7}{reset} [{component}] [req:{req_id}] {record.getMessage()}"

        # Add extra data
        if hasattr(record, "__dict__"):
            extra_keys = set(record.__dict__.keys()) - {
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "exc_info", "exc_text", "thread", "threadName",
                "taskName", "message"
            }
            extra_data = {k: record.__dict__[k] for k in extra_keys}
            if extra_data:
                # Format extra data as key=value pairs
                pairs = [f"{k}={_truncate(v)}" for k, v in extra_data.items()]
                msg += f" | {' '.join(pairs)}"

        # Add exception if present
        if record.exc_info:
            msg += f"\n{self.formatException(record.exc_info)}"

        return msg


def _truncate(value: Any, max_len: int = 100) -> str:
    """Truncate long values for display."""
    s = str(value)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


# =============================================================================
# Logger Setup
# =============================================================================

def setup_logging(
    level: Optional[str] = None,
    json_format: bool = False,
    log_file: Optional[str] = None
) -> None:
    """
    Configure logging for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR). Defaults to LOG_LEVEL env var or INFO.
        json_format: Use JSON format (True) or human-readable (False). Defaults to LOG_FORMAT env var.
        log_file: Optional file path to write logs. Defaults to LOG_FILE env var.
    """
    # Get settings from environment or params
    level = level or os.getenv("LOG_LEVEL", "INFO")
    json_format = json_format or os.getenv("LOG_FORMAT", "").lower() == "json"
    log_file = log_file or os.getenv("LOG_FILE")

    # Create formatter
    formatter = JSONFormatter() if json_format else HumanReadableFormatter()

    # Configure root logger for src.agents
    root_logger = logging.getLogger("src.agents")
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())  # Always JSON for file
        root_logger.addHandler(file_handler)

    # Prevent propagation to root logger
    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific component.

    Args:
        name: Component name (e.g., "gateway", "orchestrator", "memory")

    Returns:
        Configured logger instance
    """
    # Ensure logging is set up
    if not logging.getLogger("src.agents").handlers:
        setup_logging()

    return logging.getLogger(f"src.agents.{name}")


# =============================================================================
# Logging Event Constants
# =============================================================================

class LogEvent:
    """Standard event names for consistent logging."""

    # Request lifecycle
    REQUEST_RECEIVED = "request_received"
    REQUEST_COMPLETED = "request_completed"
    REQUEST_FAILED = "request_failed"

    # Intent classification
    INTENT_CLASSIFYING = "intent_classifying"
    INTENT_CLASSIFIED = "intent_classified"
    INTENT_UNCLEAR = "intent_unclear"

    # Chain execution
    CHAIN_STARTING = "chain_starting"
    CHAIN_COMPLETED = "chain_completed"
    CHAIN_FAILED = "chain_failed"

    # Agent execution
    AGENT_STARTING = "agent_starting"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"

    # LLM calls
    LLM_CALLING = "llm_calling"
    LLM_RESPONSE = "llm_response"
    LLM_ERROR = "llm_error"

    # Memory operations
    MEMORY_RETRIEVING = "memory_retrieving"
    MEMORY_RETRIEVED = "memory_retrieved"
    MEMORY_STORING = "memory_storing"
    MEMORY_STORED = "memory_stored"
    MEMORY_ERROR = "memory_error"

    # Streaming
    STREAM_STARTING = "stream_starting"
    STREAM_CHUNK = "stream_chunk"
    STREAM_COMPLETED = "stream_completed"


# =============================================================================
# Convenience Functions
# =============================================================================

def log_with_duration(logger: logging.Logger, event: str, start_time: float, **kwargs) -> None:
    """Log an event with duration calculated from start_time."""
    import time
    duration_ms = (time.time() - start_time) * 1000
    logger.info(event, extra={"duration_ms": round(duration_ms, 2), **kwargs})
