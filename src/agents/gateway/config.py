"""
Gateway Configuration - Environment-based settings.

Single Responsibility: Configuration constants only.
"""

import os

# External service URLs
GB10_URL = os.getenv("GB10_URL", "http://192.168.51.22:8080")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# Server settings
AGENT_PORT = int(os.getenv("AGENT_PORT", "9090"))

# HTTP client settings
HTTP_TIMEOUT = 120.0

# Indexer settings (T118)
INDEXER_MAX_FILE_SIZE = int(os.getenv("INDEXER_MAX_FILE_SIZE", str(1024 * 1024)))  # 1MB
INDEXER_MAX_RETRIES = int(os.getenv("INDEXER_MAX_RETRIES", "3"))
INDEXER_RETRY_DELAY = float(os.getenv("INDEXER_RETRY_DELAY", "0.5"))

__all__ = [
    "GB10_URL",
    "QDRANT_URL",
    "AGENT_PORT",
    "HTTP_TIMEOUT",
    # Indexer config
    "INDEXER_MAX_FILE_SIZE",
    "INDEXER_MAX_RETRIES",
    "INDEXER_RETRY_DELAY",
]
