"""
Configuration settings for the orchestrator
Loads from environment variables with sensible defaults
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""

    # Service URLs
    GPT_OSS_URL: str = "http://localhost:8000"
    BGE_M3_URL: str = "http://localhost:8001"
    QWEN_ROUTER_URL: str = "http://localhost:8002"
    QDRANT_URL: str = "http://localhost:6333"

    # Qdrant settings
    QDRANT_COLLECTION: str = "documents"
    QDRANT_TOP_K: int = 5
    QDRANT_COLLECTION_MEMORIES: str = "agent_memories"
    QDRANT_COLLECTION_KNOWLEDGE: str = "project_knowledge"
    QDRANT_COLLECTION_SHARED: str = "shared_context"

    # Timeouts (seconds)
    ROUTER_TIMEOUT: int = 10
    EMBEDDING_TIMEOUT: int = 30
    LLM_TIMEOUT: int = 120

    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_BACKOFF: float = 2.0

    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = "/opt/vision_model/.env"
        case_sensitive = True

# Global settings instance
settings = Settings()
