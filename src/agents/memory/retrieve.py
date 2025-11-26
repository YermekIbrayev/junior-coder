"""
Memory Retrieve - Retrieve memories from vector database.

Single Responsibility: Search and retrieve relevant memories.
"""

import time

from qdrant_client.models import Filter, FieldCondition, MatchValue

from src.agents.logging_config import get_logger, LogEvent
from src.agents.memory.config import DEFAULT_MEMORY_LIMIT
from src.agents.memory.embeddings import generate_embedding

logger = get_logger("memory.storage")


async def retrieve_memories(
    query: str,
    user_id: str,
    qdrant_client,
    collection_name: str,
    http_client,
    embedding_url: str,
    limit: int = DEFAULT_MEMORY_LIMIT
) -> list[str]:
    """
    Retrieve relevant memories for a query.

    Performs semantic search filtered by user_id to ensure
    memory isolation between users.

    Args:
        query: The search query
        user_id: User identifier for filtering (required for isolation)
        qdrant_client: Qdrant client instance
        collection_name: Name of the Qdrant collection
        http_client: HTTP client for embedding service
        embedding_url: URL of the embedding service
        limit: Maximum number of results (default: 3)

    Returns:
        List of memory content strings, ordered by relevance.
        Returns empty list on errors for graceful degradation.

    Raises:
        RuntimeError: If embedding generation fails after retries
    """
    if not query:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": "empty_query", "operation": "retrieve"}
        )
        return []

    if not user_id:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": "missing_user_id", "operation": "retrieve"}
        )
        return []

    start_time = time.time()
    logger.info(
        LogEvent.MEMORY_RETRIEVING,
        extra={
            "user_id": user_id,
            "query_preview": query[:100] + "..." if len(query) > 100 else query,
            "limit": limit,
            "collection": collection_name
        }
    )

    try:
        embedding = await generate_embedding(query, http_client, embedding_url)
    except RuntimeError as e:
        logger.error(
            LogEvent.MEMORY_ERROR,
            extra={
                "user_id": user_id,
                "error": str(e),
                "error_type": "embedding_failed",
                "operation": "retrieve"
            }
        )
        raise

    query_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id)
            )
        ]
    )

    try:
        results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=embedding,
            query_filter=query_filter,
            limit=limit
        )

        memories = [result.payload["content"] for result in results]
        duration_ms = (time.time() - start_time) * 1000
        scores = [round(result.score, 4) for result in results] if results else []

        logger.info(
            LogEvent.MEMORY_RETRIEVED,
            extra={
                "user_id": user_id,
                "memory_count": len(memories),
                "limit": limit,
                "scores": scores,
                "total_chars": sum(len(m) for m in memories),
                "duration_ms": round(duration_ms, 2)
            }
        )
        return memories

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            LogEvent.MEMORY_ERROR,
            extra={
                "user_id": user_id,
                "collection": collection_name,
                "error": str(e),
                "error_type": type(e).__name__,
                "operation": "retrieve",
                "duration_ms": round(duration_ms, 2)
            }
        )
        return []


__all__ = ["retrieve_memories"]
