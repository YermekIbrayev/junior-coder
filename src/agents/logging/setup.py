"""
Logging Setup - Configure logging for the application.

Single Responsibility: Initialize and configure logging infrastructure.
"""

import logging
import os
import sys
from typing import Optional

from src.agents.logging.formatters import JSONFormatter, HumanReadableFormatter


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


__all__ = ["setup_logging", "get_logger"]
