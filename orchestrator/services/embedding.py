"""
Embedding generation service using BGE-M3
Generates 1024-dimensional vectors for semantic search
"""
import httpx
from typing import List
from core.config import settings
from services import llm_client

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings using BGE-M3

    Args:
        texts: List of strings to embed

    Returns:
        List of 1024-dimensional embedding vectors

    Raises:
        httpx.HTTPError: If request fails
    """
    if not llm_client.http_client:
        raise RuntimeError("HTTP client not initialized")

    # BGE-M3 OpenAI-compatible embeddings endpoint
    response = await llm_client.http_client.post(
        f"{settings.BGE_M3_URL}/v1/embeddings",
        json={"input": texts, "model": "bge-m3"},
        timeout=settings.EMBEDDING_TIMEOUT
    )
    response.raise_for_status()

    data = response.json()

    # Extract embeddings from response
    embeddings = [item["embedding"] for item in data["data"]]

    return embeddings
