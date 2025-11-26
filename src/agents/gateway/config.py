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

__all__ = ["GB10_URL", "QDRANT_URL", "AGENT_PORT", "HTTP_TIMEOUT"]
