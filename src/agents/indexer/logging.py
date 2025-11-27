"""
T116: Structured logging for the Project Architecture Indexer.

Provides consistent logging with metrics across all indexer modules.
"""

import logging
import time
from contextlib import contextmanager
from typing import Any, Dict, Optional


# Create indexer-specific logger
logger = logging.getLogger("indexer")


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the indexer module.

    Args:
        level: Logging level (default INFO)
    """
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    logger.addHandler(handler)
    logger.setLevel(level)


def log_operation(
    operation: str,
    status: str = "info",
    **kwargs: Any,
) -> None:
    """
    Log a structured operation message.

    Args:
        operation: Operation name
        status: Log level (info, warning, error, debug)
        **kwargs: Additional context to log
    """
    extra_info = " ".join(f"{k}={v}" for k, v in kwargs.items())
    message = f"[{operation}] {extra_info}" if extra_info else f"[{operation}]"

    log_method = getattr(logger, status, logger.info)
    log_method(message)


@contextmanager
def log_timing(operation: str, **kwargs: Any):
    """
    Context manager to log operation timing.

    Args:
        operation: Operation name
        **kwargs: Additional context

    Yields:
        Dict to store metrics during operation
    """
    start_time = time.time()
    metrics: Dict[str, Any] = {"operation": operation}

    try:
        log_operation(operation, status="debug", state="started", **kwargs)
        yield metrics
        elapsed = time.time() - start_time
        metrics["elapsed_ms"] = round(elapsed * 1000, 2)
        log_operation(
            operation,
            status="info",
            state="completed",
            elapsed_ms=metrics["elapsed_ms"],
            **kwargs,
        )
    except Exception as e:
        elapsed = time.time() - start_time
        metrics["elapsed_ms"] = round(elapsed * 1000, 2)
        metrics["error"] = str(e)
        log_operation(
            operation,
            status="error",
            state="failed",
            elapsed_ms=metrics["elapsed_ms"],
            error=str(e),
            **kwargs,
        )
        raise
