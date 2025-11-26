"""
MemoryClient - Qdrant-based conversation memory with semantic search.

Stores and retrieves conversation memories using vector embeddings for
semantic similarity search, with user isolation.

Features:
- Semantic search using BGE-M3 embeddings (1024 dimensions)
- User isolation via user_id filtering
- Retry logic for transient failures
- Graceful degradation on service unavailability
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from src.agents.logging_config import get_logger, LogEvent

# Module logger with structured logging
logger = get_logger("memory.client")

# Default collection name for agent memories
DEFAULT_COLLECTION_NAME = "agent_memories"

# Default embedding service URL (BGE-M3 on GB10)
DEFAULT_EMBEDDING_URL = "http://192.168.51.22:8080/v1/embeddings"

# Default number of memories to retrieve
DEFAULT_MEMORY_LIMIT = 3

# Embedding timeout in seconds
EMBEDDING_TIMEOUT = 30.0

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5


@dataclass
class MemoryClient:
    """
    Client for storing and retrieving conversation memories.

    Uses Qdrant for vector storage and BGE-M3 for embeddings.
    Supports user isolation via user_id filtering.

    Attributes:
        qdrant_client: Qdrant client instance for vector operations
        collection_name: Name of the Qdrant collection
        http_client: HTTP client for embedding service calls
        embedding_url: URL of the embedding service
    """

    qdrant_client: object
    collection_name: str = field(default=DEFAULT_COLLECTION_NAME)
    http_client: Optional[object] = field(default=None)
    embedding_url: str = field(default=DEFAULT_EMBEDDING_URL)

    async def _generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding vector for text using BGE-M3.

        Includes retry logic for transient failures.

        Args:
            text: Text to embed

        Returns:
            1024-dimensional embedding vector

        Raises:
            RuntimeError: If http_client is not configured or embedding fails
                          after all retries
        """
        if self.http_client is None:
            raise RuntimeError("http_client required for embedding generation")

        payload = {
            "input": text,
            "model": "bge-m3"
        }

        last_error = None
        start_time = time.time()

        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(
                    "embedding_generating",
                    extra={
                        "attempt": attempt + 1,
                        "max_retries": MAX_RETRIES,
                        "text_preview": text[:50] + "...",
                        "url": self.embedding_url
                    }
                )

                response = await self.http_client.post(
                    self.embedding_url,
                    json=payload,
                    timeout=EMBEDDING_TIMEOUT
                )
                response.raise_for_status()

                data = response.json()
                embedding = data["data"][0]["embedding"]
                duration_ms = (time.time() - start_time) * 1000

                logger.debug(
                    "embedding_generated",
                    extra={
                        "dimensions": len(embedding),
                        "duration_ms": round(duration_ms, 2),
                        "attempts_used": attempt + 1
                    }
                )
                return embedding

            except Exception as e:
                last_error = e
                logger.warning(
                    "embedding_failed",
                    extra={
                        "attempt": attempt + 1,
                        "max_retries": MAX_RETRIES,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "will_retry": attempt < MAX_RETRIES - 1
                    }
                )
                if attempt < MAX_RETRIES - 1:
                    import asyncio
                    await asyncio.sleep(RETRY_DELAY_SECONDS * (attempt + 1))

        # All retries exhausted
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            "embedding_exhausted",
            extra={
                "max_retries": MAX_RETRIES,
                "duration_ms": round(duration_ms, 2),
                "final_error": str(last_error)
            }
        )
        raise RuntimeError(
            f"Embedding generation failed after {MAX_RETRIES} attempts: {last_error}"
        )

    async def store_memory(
        self,
        content: str,
        user_id: str,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Store a memory in the vector database.

        Generates an embedding for the content and stores it with metadata
        including user_id for isolation.

        Args:
            content: The conversation content to store
            user_id: User identifier for memory isolation
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
            # Generate embedding
            embedding = await self._generate_embedding(content)
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

        # Generate unique ID
        point_id = str(uuid.uuid4())

        # Build payload
        payload = {
            "content": content,
            "user_id": user_id,
            "timestamp": time.time()
        }

        # Merge optional metadata
        if metadata:
            payload.update(metadata)

        # Create point
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload=payload
        )

        try:
            # Upsert to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            duration_ms = (time.time() - start_time) * 1000
            logger.info(
                LogEvent.MEMORY_STORED,
                extra={
                    "user_id": user_id,
                    "point_id": point_id,
                    "collection": self.collection_name,
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
                    "collection": self.collection_name,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "operation": "store",
                    "duration_ms": round(duration_ms, 2)
                }
            )
            raise

    async def retrieve_memories(
        self,
        query: str,
        user_id: str,
        limit: int = DEFAULT_MEMORY_LIMIT
    ) -> list[str]:
        """
        Retrieve relevant memories for a query.

        Performs semantic search filtered by user_id to ensure
        memory isolation between users.

        Args:
            query: The search query
            user_id: User identifier for filtering (required for isolation)
            limit: Maximum number of results (default: 3)

        Returns:
            List of memory content strings, ordered by relevance.
            Returns empty list on errors to allow graceful degradation.

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
                "collection": self.collection_name
            }
        )

        try:
            # Generate embedding for query
            embedding = await self._generate_embedding(query)
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

        # Build user_id filter for isolation
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )

        try:
            # Search Qdrant
            results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                query_filter=query_filter,
                limit=limit
            )

            # Extract content from results
            memories = [result.payload["content"] for result in results]
            duration_ms = (time.time() - start_time) * 1000

            # Extract scores for debugging
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
                    "collection": self.collection_name,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "operation": "retrieve",
                    "duration_ms": round(duration_ms, 2)
                }
            )
            # Return empty list for graceful degradation
            return []
