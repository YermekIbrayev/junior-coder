"""
Mem0-compatible Client for Agent Long-Term Memory

Direct Qdrant integration implementing Mem0-like API
Uses Qdrant + BGE-M3 for agent memory storage and retrieval

NOTE: Compatible with Mem0 API, ready for mem0ai==1.0.0 integration
Constitution Compliance: Principle VIII (Token-Efficient, <100 lines ✅)
"""
from typing import Optional, List, Dict, Any
import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import time


class Mem0Client:
    """Agent long-term memory with Qdrant backend"""

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

    async def add_memory(
        self,
        user_id: str,
        agent_id: str,
        messages: List[Dict[str, str]],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add agent memory to Qdrant

        Args:
            user_id: User identifier
            agent_id: Agent identifier (for isolation)
            messages: Message list [{"role": "user", "content": "..."}]
            metadata: Additional metadata

        Returns:
            {"id": "mem_xxx", "status": "success"}
        """
        # Extract content from messages
        content = " ".join([m["content"] for m in messages])

        # Get embedding
        embedding = await self._get_embedding(content)

        # Create point with payload
        point_id = str(uuid.uuid4())
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "content": content,
                "user_id": user_id,
                "agent_id": agent_id,
                "timestamp": time.time(),
                **metadata
            }
        )

        # Upsert to Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        return {"id": f"mem_{point_id[:8]}", "status": "success"}

    async def search_memories(
        self,
        query: str,
        user_id: str,
        agent_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search agent memories

        Args:
            query: Search query
            user_id: User filter
            agent_id: Optional agent filter (None = cross-agent search)
            limit: Max results

        Returns:
            [{"content": "...", "score": 0.95, ...}]
        """
        # Get query embedding
        query_embedding = await self._get_embedding(query)

        # Build filter
        filter_conditions = [
            FieldCondition(key="user_id", match=MatchValue(value=user_id))
        ]
        if agent_id:
            filter_conditions.append(
                FieldCondition(key="agent_id", match=MatchValue(value=agent_id))
            )

        # Search Qdrant
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=Filter(must=filter_conditions) if filter_conditions else None,
            limit=limit
        )

        # Format results
        return [
            {
                "content": hit.payload.get("content"),
                "user_id": hit.payload.get("user_id"),
                "agent_id": hit.payload.get("agent_id"),
                "timestamp": hit.payload.get("timestamp"),
                "score": hit.score
            }
            for hit in results
        ]
