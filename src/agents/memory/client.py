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

from dataclasses import dataclass, field
from typing import Optional

from src.agents.memory.config import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_EMBEDDING_URL,
    DEFAULT_MEMORY_LIMIT,
    EMBEDDING_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
)
from src.agents.memory.embeddings import generate_embedding
from src.agents.memory.storage import (
    store_memory as _store_memory,
    retrieve_memories as _retrieve_memories,
)


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

        Backward compatibility wrapper for tests.
        """
        return await generate_embedding(text, self.http_client, self.embedding_url)

    async def store_memory(
        self,
        content: str,
        user_id: str,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Store a memory in the vector database.

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
        return await _store_memory(
            content=content,
            user_id=user_id,
            qdrant_client=self.qdrant_client,
            collection_name=self.collection_name,
            http_client=self.http_client,
            embedding_url=self.embedding_url,
            metadata=metadata
        )

    async def retrieve_memories(
        self,
        query: str,
        user_id: str,
        limit: int = DEFAULT_MEMORY_LIMIT
    ) -> list[str]:
        """
        Retrieve relevant memories for a query.

        Args:
            query: The search query
            user_id: User identifier for filtering (required for isolation)
            limit: Maximum number of results (default: 3)

        Returns:
            List of memory content strings, ordered by relevance.
        """
        return await _retrieve_memories(
            query=query,
            user_id=user_id,
            qdrant_client=self.qdrant_client,
            collection_name=self.collection_name,
            http_client=self.http_client,
            embedding_url=self.embedding_url,
            limit=limit
        )


# Re-export constants for backward compatibility
__all__ = [
    "MemoryClient",
    "EMBEDDING_TIMEOUT",
    "MAX_RETRIES",
    "RETRY_DELAY_SECONDS",
    "DEFAULT_COLLECTION_NAME",
    "DEFAULT_EMBEDDING_URL",
    "DEFAULT_MEMORY_LIMIT",
]
