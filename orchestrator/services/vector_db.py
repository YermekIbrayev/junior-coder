"""
Qdrant vector database client
Handles indexing and similarity search
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Optional
from uuid import uuid4
from core.config import settings

# Global Qdrant client
qdrant_client: Optional[QdrantClient] = None

def get_qdrant_client() -> QdrantClient:
    """Get or create Qdrant client"""
    global qdrant_client
    if not qdrant_client:
        qdrant_client = QdrantClient(url=settings.QDRANT_URL)
    return qdrant_client

async def ensure_collection():
    """Create collection if it doesn't exist"""
    client = get_qdrant_client()

    # Check if collection exists
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if settings.QDRANT_COLLECTION not in collection_names:
        # Create collection for BGE-M3 (1024 dimensions)
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )

async def index_documents(texts: List[str], embeddings: List[List[float]]) -> int:
    """
    Index documents into Qdrant

    Args:
        texts: Document texts
        embeddings: Corresponding embeddings

    Returns:
        Number of documents indexed
    """
    client = get_qdrant_client()
    await ensure_collection()

    # Create points
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={"text": text}
        )
        for text, embedding in zip(texts, embeddings)
    ]

    # Upload points
    client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)

    return len(points)

async def search_similar(query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    """
    Search for similar documents

    Args:
        query_embedding: Query vector
        top_k: Number of results

    Returns:
        List of dicts with 'text' and 'score'
    """
    client = get_qdrant_client()
    await ensure_collection()

    results = client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=top_k
    )

    return [
        {"text": hit.payload["text"], "score": hit.score}
        for hit in results
    ]
