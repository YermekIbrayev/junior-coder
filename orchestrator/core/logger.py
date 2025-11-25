"""
Logging configuration for orchestrator
Provides structured logging with DEBUG level for troubleshooting
"""
import logging
import sys

def setup_logging(level=logging.DEBUG):
    """
    Configure logging for the orchestrator

    Args:
        level: Logging level (default: DEBUG for troubleshooting)
    """
    # Create formatter with detailed information
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Create console handler (outputs to stdout, which is redirected to log file)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Configure third-party loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)  # Reduce noise from HTTP client

    # Force flush for real-time logging
    sys.stdout.flush()
    sys.stderr.flush()

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module

    Args:
        name: Module name (use __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
