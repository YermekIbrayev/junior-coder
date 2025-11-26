"""
Memory Store - Store memories to vector database.

Single Responsibility: Store memories with embeddings.
"""

import time
import uuid
from typing import Optional

from qdrant_client.models import PointStruct

from src.agents.logging_config import get_logger, LogEvent
from src.agents.memory.embeddings import generate_embedding

logger = get_logger("memory.storage")


async def store_memory(
    content: str,
    user_id: str,
    qdrant_client,
    collection_name: str,
    http_client,
    embedding_url: str,
    metadata: Optional[dict] = None
) -> str:
    """
    Store a memory in the vector database.

    Args:
        content: The conversation content to store
        user_id: User identifier for memory isolation
        qdrant_client: Qdrant client instance
        collection_name: Name of the Qdrant collection
        http_client: HTTP client for embedding service
        embedding_url: URL of the embedding service
        metadata: Optional additional metadata

    Returns:
        The ID of the stored memory point

    Raises:
        RuntimeError: If embedding generation fails after retries
        Exception: If Qdrant upsert fails
    """
    if not content:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": "empty_content", "operation": "store"}
        )
        return ""

    if not user_id:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": "missing_user_id", "operation": "store", "fallback": "anonymous"}
        )
        user_id = "anonymous"

    start_time = time.time()
    logger.info(
        LogEvent.MEMORY_STORING,
        extra={
            "user_id": user_id,
            "content_length": len(content),
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "has_metadata": metadata is not None
        }
    )

    try:
        embedding = await generate_embedding(content, http_client, embedding_url)
    except RuntimeError as e:
        logger.error(
            LogEvent.MEMORY_ERROR,
            extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": "embedding_failed",
                "operation": "store"
            }
        )
        raise

    point_id = str(uuid.uuid4())
    payload = {
        "content": content,
        "user_id": user_id,
        "timestamp": time.time()
    }

    if metadata:
        payload.update(metadata)

    point = PointStruct(
        id=point_id,
        vector=embedding,
        payload=payload
    )

    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            LogEvent.MEMORY_STORED,
            extra={
                "user_id": user_id,
                "point_id": point_id,
                "collection": collection_name,
                "duration_ms": round(duration_ms, 2)
            }
        )
        return point_id

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            LogEvent.MEMORY_ERROR,
            extra={
                "user_id": user_id,
                "collection": collection_name,
                "error": str(e),
                "error_type": type(e).__name__,
                "operation": "store",
                "duration_ms": round(duration_ms, 2)
            }
        )
        raise


__all__ = ["store_memory"]
