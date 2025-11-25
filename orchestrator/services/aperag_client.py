"""
ApeRAG-compatible Client for Project Knowledge GraphRAG

Direct Qdrant integration for project documentation and code indexing
Uses Qdrant + BGE-M3 for knowledge storage and retrieval

NOTE: Compatible with ApeRAG API, ready for future GraphRAG integration
Constitution Compliance: Principle VIII (Token-Efficient, <100 lines ✅)
"""
from typing import Optional, List, Dict, Any
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import time


class ApeRAGClient:
    """Project knowledge GraphRAG with Qdrant backend"""

    def __init__(self, qdrant_url: str, embedding_url: str, collection_name: str):
        """Initialize with Qdrant and embedding service URLs"""
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self.embedding_url = embedding_url
        self.collection_name = collection_name
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from BGE-M3 service"""
        response = await self.http_client.post(
            f"{self.embedding_url}/v1/embeddings",
            json={"input": text, "model": "BAAI/bge-m3"}
        )
        data = response.json()
        return data["data"][0]["embedding"]

    async def index_document(
        self,
        content: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Index document into Qdrant

        Args:
            content: Document content (code, docs, etc.)
            metadata: Document metadata (doc_type, file_path, language, etc.)

        Returns:
            {"id": "doc_xxx", "status": "indexed"}
        """
        # Get embedding
        embedding = await self._get_embedding(content)

        # Create point with payload
        point_id = str(uuid.uuid4())
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "content": content,
                "timestamp": time.time(),
                **metadata
            }
        )

        # Upsert to Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        return {"id": f"doc_{point_id[:8]}", "status": "indexed"}

    async def query_knowledge(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query project knowledge

        Args:
            query: Search query
            filters: Optional metadata filters (doc_type, project_id, etc.)
            top_k: Max results

        Returns:
            [{"content": "...", "score": 0.92, "doc_type": "...", ...}]
        """
        # Get query embedding
        query_embedding = await self._get_embedding(query)

        # Build filter from metadata
        filter_conditions = []
        if filters:
            for key, value in filters.items():
                filter_conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )

        # Search Qdrant
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=Filter(must=filter_conditions) if filter_conditions else None,
            limit=top_k
        )

        # Format results
        return [
            {
                "content": hit.payload.get("content"),
                "doc_type": hit.payload.get("doc_type"),
                "file_path": hit.payload.get("file_path"),
                "timestamp": hit.payload.get("timestamp"),
                "score": hit.score,
                **{k: v for k, v in hit.payload.items()
                   if k not in ["content", "doc_type", "file_path", "timestamp"]}
            }
            for hit in results
        ]
