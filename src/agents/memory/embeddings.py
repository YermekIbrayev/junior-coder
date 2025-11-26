"""
Memory Embeddings - Vector embedding generation for semantic search.

Single Responsibility: Generate embeddings using BGE-M3 service.
"""

import asyncio
import time

from src.agents.logging_config import get_logger
from src.agents.memory.config import (
    EMBEDDING_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
)

logger = get_logger("memory.embeddings")


async def generate_embedding(
    text: str,
    http_client,
    embedding_url: str
) -> list[float]:
    """
    Generate embedding vector for text using BGE-M3.

    Includes retry logic for transient failures.

    Args:
        text: Text to embed
        http_client: Async HTTP client for service calls
        embedding_url: URL of the embedding service

    Returns:
        1024-dimensional embedding vector

    Raises:
        RuntimeError: If http_client is not configured or embedding fails
                      after all retries
    """
    if http_client is None:
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
                    "url": embedding_url
                }
            )

            response = await http_client.post(
                embedding_url,
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


__all__ = ["generate_embedding"]
