"""
Memory Configuration - Constants for memory operations.

Single Responsibility: Centralize memory service configuration.
"""

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

__all__ = [
    "DEFAULT_COLLECTION_NAME",
    "DEFAULT_EMBEDDING_URL",
    "DEFAULT_MEMORY_LIMIT",
    "EMBEDDING_TIMEOUT",
    "MAX_RETRIES",
    "RETRY_DELAY_SECONDS",
]
