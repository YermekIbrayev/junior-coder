"""
Logging Events - Standard event names for consistent logging.

Single Responsibility: Define event constants for structured logging.
"""

import logging
import time


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


def log_with_duration(logger: logging.Logger, event: str, start_time: float, **kwargs) -> None:
    """Log an event with duration calculated from start_time."""
    duration_ms = (time.time() - start_time) * 1000
    logger.info(event, extra={"duration_ms": round(duration_ms, 2), **kwargs})


__all__ = ["LogEvent", "log_with_duration"]
