"""
Logging Formatters - JSON and human-readable log formatters.

Single Responsibility: Format log records for output.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any

from src.agents.logging.context import get_request_context

# Keys to exclude from extra data extraction
_EXCLUDED_RECORD_KEYS = {
    "name", "msg", "args", "created", "filename", "funcName",
    "levelname", "levelno", "lineno", "module", "msecs",
    "pathname", "process", "processName", "relativeCreated",
    "stack_info", "exc_info", "exc_text", "thread", "threadName",
    "taskName", "message"
}


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
            extra_keys = set(record.__dict__.keys()) - _EXCLUDED_RECORD_KEYS
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
            extra_keys = set(record.__dict__.keys()) - _EXCLUDED_RECORD_KEYS
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


__all__ = ["JSONFormatter", "HumanReadableFormatter"]
