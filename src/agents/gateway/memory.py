"""
Memory Helpers - Conversation memory client management.

Single Responsibility: Memory client lifecycle and storage operations.
"""

from src.agents.logging_config import get_logger, LogEvent
from src.agents.gateway.config import QDRANT_URL

logger = get_logger("gateway.memory")

# Global memory client (initialized lazily)
_memory_client = None
_http_client = None


def set_http_client(client):
    """Set the HTTP client for memory operations."""
    global _http_client
    _http_client = client


async def get_memory_client():
    """Get or create the memory client."""
    global _memory_client

    # Sync from gateway module if memory_client was explicitly set (test compatibility)
    # PEP 562: __setattr__ not supported at module level, so tests set directly in __dict__
    import src.agents.gateway as gateway
    if "memory_client" in gateway.__dict__:
        _memory_client = gateway.__dict__["memory_client"]
        # Clear from gateway dict so __getattr__ works normally after
        del gateway.__dict__["memory_client"]

    if _memory_client is None:
        try:
            from qdrant_client import QdrantClient
            from src.agents.memory.client import MemoryClient

            qdrant = QdrantClient(url=QDRANT_URL)
            _memory_client = MemoryClient(
                qdrant_client=qdrant,
                http_client=_http_client
            )
            logger.info(f"Memory client initialized with Qdrant at {QDRANT_URL}")
        except Exception as e:
            logger.warning(f"Failed to initialize memory client: {e}")
            return None
    return _memory_client


def _reset_memory_client():
    """Reset the memory client (for testing)."""
    global _memory_client
    _memory_client = None


async def store_conversation_memory(
    content: str,
    user_id: str,
    metadata: dict | None = None
) -> None:
    """
    Store a conversation exchange in memory.

    Args:
        content: Combined user message and assistant response
        user_id: User identifier for memory isolation
        metadata: Optional metadata (chain_id, model, etc.)
    """
    # Import dynamically to allow test mocking at src.agents.gateway level
    import src.agents.gateway as gateway
    client = await gateway.get_memory_client()

    if client is None:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": "client_not_available", "operation": "store", "user_id": user_id}
        )
        return

    try:
        await client.store_memory(
            content=content,
            user_id=user_id,
            metadata=metadata
        )
        logger.debug(
            LogEvent.MEMORY_STORED,
            extra={"user_id": user_id, "content_length": len(content)}
        )
    except Exception as e:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": str(e), "error_type": type(e).__name__, "operation": "store"}
        )


__all__ = ["get_memory_client", "store_conversation_memory", "set_http_client", "_memory_client", "_reset_memory_client"]
