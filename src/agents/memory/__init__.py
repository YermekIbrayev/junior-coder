"""
Memory Module - Qdrant-based conversation memory with semantic search.

This package provides modular memory operations:
- config.py: Configuration constants
- embeddings.py: Vector embedding generation
- storage.py: Store/retrieve operations
- client.py: MemoryClient class

Usage:
    from src.agents.memory import MemoryClient
    client = MemoryClient(qdrant_client=qdrant, http_client=http)
    await client.store_memory(content, user_id)
    memories = await client.retrieve_memories(query, user_id)
"""

from src.agents.memory.client import MemoryClient
from src.agents.memory.config import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_EMBEDDING_URL,
    DEFAULT_MEMORY_LIMIT,
)

__all__ = [
    "MemoryClient",
    "DEFAULT_COLLECTION_NAME",
    "DEFAULT_EMBEDDING_URL",
    "DEFAULT_MEMORY_LIMIT",
]
