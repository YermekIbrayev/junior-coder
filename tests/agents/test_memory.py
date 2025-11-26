"""
Tests for MemoryClient - Qdrant-based conversation memory.

TDD Tests for Phase 6.1:
- T056: MemoryClient init (qdrant_client, collection name)
- T058: store_memory (embed content, store with user_id metadata)
- T060: retrieve_memories (semantic search, filter by user_id, return top 3)

TDD Tests for Phase 6.2:
- T062: Embedding generation (mock BGE-M3 call, return 1024-dim vector)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass


# ============================================================================
# T056: MemoryClient Init Tests (RED)
# ============================================================================

class TestMemoryClientInit:
    """Test MemoryClient initialization - T056."""

    def test_memory_client_class_exists(self):
        """MemoryClient class must exist."""
        from src.agents.memory.client import MemoryClient
        assert MemoryClient is not None

    def test_memory_client_accepts_qdrant_client(self, mock_qdrant_client):
        """MemoryClient must accept a qdrant_client parameter."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        assert client.qdrant_client is mock_qdrant_client

    def test_memory_client_accepts_collection_name(self, mock_qdrant_client):
        """MemoryClient must accept a collection_name parameter."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            collection_name="test_collection"
        )
        assert client.collection_name == "test_collection"

    def test_memory_client_default_collection_name(self, mock_qdrant_client):
        """MemoryClient must have a default collection name."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        assert client.collection_name == "agent_memories"

    def test_memory_client_accepts_http_client(self, mock_qdrant_client, mock_httpx_client):
        """MemoryClient must accept an http_client for embedding calls."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )
        assert client.http_client is mock_httpx_client

    def test_memory_client_has_embedding_url(self, mock_qdrant_client):
        """MemoryClient must have an embedding service URL."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        assert hasattr(client, 'embedding_url')
        assert client.embedding_url is not None


# ============================================================================
# T058: store_memory Tests (RED)
# ============================================================================

class TestStoreMemory:
    """Test store_memory method - T058."""

    @pytest.mark.asyncio
    async def test_store_memory_method_exists(self, mock_qdrant_client):
        """MemoryClient must have a store_memory method."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        assert hasattr(client, 'store_memory')
        assert callable(client.store_memory)

    @pytest.mark.asyncio
    async def test_store_memory_accepts_content_and_user_id(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """store_memory must accept content and user_id parameters."""
        from src.agents.memory.client import MemoryClient

        # Mock embedding response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        # Should not raise
        await client.store_memory(
            content="User asked about authentication",
            user_id="user-123"
        )

    @pytest.mark.asyncio
    async def test_store_memory_generates_embedding(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """store_memory must generate embedding for content."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.store_memory(
            content="User asked about authentication",
            user_id="user-123"
        )

        # Verify embedding service was called
        mock_httpx_client.post.assert_called()
        call_args = mock_httpx_client.post.call_args
        assert "embeddings" in call_args[0][0]  # URL contains embeddings

    @pytest.mark.asyncio
    async def test_store_memory_upserts_to_qdrant(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """store_memory must upsert point to Qdrant with user_id metadata."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.store_memory(
            content="User asked about authentication",
            user_id="user-123"
        )

        # Verify Qdrant upsert was called
        mock_qdrant_client.upsert.assert_called_once()
        call_kwargs = mock_qdrant_client.upsert.call_args[1]

        # Check collection name
        assert call_kwargs['collection_name'] == "agent_memories"

        # Check points have correct structure
        points = call_kwargs['points']
        assert len(points) == 1
        point = points[0]

        # Verify payload contains user_id and content
        assert point.payload['user_id'] == "user-123"
        assert point.payload['content'] == "User asked about authentication"

    @pytest.mark.asyncio
    async def test_store_memory_includes_timestamp(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """store_memory must include timestamp in metadata."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.store_memory(
            content="Test content",
            user_id="user-123"
        )

        call_kwargs = mock_qdrant_client.upsert.call_args[1]
        point = call_kwargs['points'][0]

        assert 'timestamp' in point.payload
        assert isinstance(point.payload['timestamp'], float)

    @pytest.mark.asyncio
    async def test_store_memory_accepts_optional_metadata(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """store_memory must accept optional metadata dict."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.store_memory(
            content="Test content",
            user_id="user-123",
            metadata={"chain_id": "sdd", "agent_id": "spec-analyst"}
        )

        call_kwargs = mock_qdrant_client.upsert.call_args[1]
        point = call_kwargs['points'][0]

        assert point.payload['chain_id'] == "sdd"
        assert point.payload['agent_id'] == "spec-analyst"


# ============================================================================
# T060: retrieve_memories Tests (RED)
# ============================================================================

class TestRetrieveMemories:
    """Test retrieve_memories method - T060."""

    @pytest.mark.asyncio
    async def test_retrieve_memories_method_exists(self, mock_qdrant_client):
        """MemoryClient must have a retrieve_memories method."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        assert hasattr(client, 'retrieve_memories')
        assert callable(client.retrieve_memories)

    @pytest.mark.asyncio
    async def test_retrieve_memories_accepts_query_and_user_id(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must accept query and user_id parameters."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        # Should not raise
        results = await client.retrieve_memories(
            query="What did we discuss about auth?",
            user_id="user-123"
        )

        assert results is not None

    @pytest.mark.asyncio
    async def test_retrieve_memories_generates_embedding_for_query(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must generate embedding for the query."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123"
        )

        # Verify embedding was generated
        mock_httpx_client.post.assert_called()

    @pytest.mark.asyncio
    async def test_retrieve_memories_searches_qdrant(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must search Qdrant with embedding."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123"
        )

        # Verify Qdrant search was called
        mock_qdrant_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_retrieve_memories_filters_by_user_id(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must filter by user_id."""
        from src.agents.memory.client import MemoryClient
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123"
        )

        # Verify filter was passed
        call_kwargs = mock_qdrant_client.search.call_args[1]
        assert 'query_filter' in call_kwargs

        # The filter should contain user_id condition
        query_filter = call_kwargs['query_filter']
        assert query_filter is not None

    @pytest.mark.asyncio
    async def test_retrieve_memories_returns_top_3_by_default(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must return top 3 results by default."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123"
        )

        # Verify limit=3 was passed
        call_kwargs = mock_qdrant_client.search.call_args[1]
        assert call_kwargs.get('limit', 3) == 3

    @pytest.mark.asyncio
    async def test_retrieve_memories_returns_content_strings(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must return list of content strings."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        results = await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123"
        )

        # Should return list of strings
        assert isinstance(results, list)
        assert len(results) == 3  # From mock_qdrant_client fixture
        assert all(isinstance(r, str) for r in results)

    @pytest.mark.asyncio
    async def test_retrieve_memories_returns_empty_list_when_no_results(
        self, mock_qdrant_empty, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must return empty list when no results."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_empty,
            http_client=mock_httpx_client
        )

        results = await client.retrieve_memories(
            query="Something we never discussed",
            user_id="user-123"
        )

        assert results == []

    @pytest.mark.asyncio
    async def test_retrieve_memories_accepts_custom_limit(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must accept a custom limit parameter."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123",
            limit=5
        )

        call_kwargs = mock_qdrant_client.search.call_args[1]
        assert call_kwargs['limit'] == 5


# ============================================================================
# T062: Embedding Generation Tests (RED)
# ============================================================================

class TestEmbeddingGeneration:
    """Test embedding generation - T062."""

    @pytest.mark.asyncio
    async def test_generate_embedding_method_exists(self, mock_qdrant_client):
        """MemoryClient must have a _generate_embedding method."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        assert hasattr(client, '_generate_embedding')
        assert callable(client._generate_embedding)

    @pytest.mark.asyncio
    async def test_generate_embedding_requires_http_client(self, mock_qdrant_client):
        """_generate_embedding must raise if http_client is not configured."""
        from src.agents.memory.client import MemoryClient

        client = MemoryClient(qdrant_client=mock_qdrant_client)
        # No http_client set

        with pytest.raises(RuntimeError, match="http_client required"):
            await client._generate_embedding("test text")

    @pytest.mark.asyncio
    async def test_generate_embedding_calls_bge_m3_endpoint(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """_generate_embedding must call BGE-M3 embedding endpoint."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client._generate_embedding("test text")

        # Verify the embedding endpoint was called
        mock_httpx_client.post.assert_called_once()
        call_args = mock_httpx_client.post.call_args
        assert "embeddings" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_generate_embedding_sends_correct_payload(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """_generate_embedding must send correct payload format."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client._generate_embedding("test text for embedding")

        # Verify payload format
        call_kwargs = mock_httpx_client.post.call_args[1]
        payload = call_kwargs['json']

        assert payload['input'] == "test text for embedding"
        assert payload['model'] == "bge-m3"

    @pytest.mark.asyncio
    async def test_generate_embedding_returns_1024_dim_vector(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """_generate_embedding must return 1024-dimensional vector."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        embedding = await client._generate_embedding("test text")

        # Verify it's a 1024-dim vector
        assert isinstance(embedding, list)
        assert len(embedding) == 1024
        assert all(isinstance(x, (int, float)) for x in embedding)

    @pytest.mark.asyncio
    async def test_generate_embedding_extracts_from_response(
        self, mock_qdrant_client, mock_httpx_client
    ):
        """_generate_embedding must extract embedding from OpenAI-format response."""
        from src.agents.memory.client import MemoryClient

        # Custom embedding response with specific values
        custom_embedding = [0.5] * 1024
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "object": "list",
            "data": [{
                "object": "embedding",
                "index": 0,
                "embedding": custom_embedding
            }],
            "model": "bge-m3",
            "usage": {"prompt_tokens": 5, "total_tokens": 5}
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        embedding = await client._generate_embedding("test text")

        # Verify the exact embedding was extracted
        assert embedding == custom_embedding

    @pytest.mark.asyncio
    async def test_generate_embedding_uses_timeout(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """_generate_embedding must use configured timeout."""
        from src.agents.memory.client import MemoryClient, EMBEDDING_TIMEOUT

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client._generate_embedding("test text")

        # Verify timeout was passed
        call_kwargs = mock_httpx_client.post.call_args[1]
        assert call_kwargs['timeout'] == EMBEDDING_TIMEOUT

    @pytest.mark.asyncio
    async def test_generate_embedding_raises_on_http_error(
        self, mock_qdrant_client, mock_httpx_client
    ):
        """_generate_embedding must propagate HTTP errors."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 500 Error")
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        with pytest.raises(Exception, match="HTTP 500"):
            await client._generate_embedding("test text")

    @pytest.mark.asyncio
    async def test_generate_embedding_uses_custom_url(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """_generate_embedding must use custom embedding_url if provided."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        custom_url = "http://custom-embedding:9000/v1/embeddings"
        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client,
            embedding_url=custom_url
        )

        await client._generate_embedding("test text")

        # Verify custom URL was used
        call_args = mock_httpx_client.post.call_args[0]
        assert call_args[0] == custom_url

    @pytest.mark.asyncio
    async def test_embedding_constant_exists(self):
        """EMBEDDING_TIMEOUT constant must exist."""
        from src.agents.memory.client import EMBEDDING_TIMEOUT

        assert EMBEDDING_TIMEOUT is not None
        assert isinstance(EMBEDDING_TIMEOUT, (int, float))
        assert EMBEDDING_TIMEOUT > 0

    @pytest.mark.asyncio
    async def test_default_embedding_url_constant_exists(self):
        """DEFAULT_EMBEDDING_URL constant must exist."""
        from src.agents.memory.client import DEFAULT_EMBEDDING_URL

        assert DEFAULT_EMBEDDING_URL is not None
        assert isinstance(DEFAULT_EMBEDDING_URL, str)
        assert "embeddings" in DEFAULT_EMBEDDING_URL


# ============================================================================
# T068: User Isolation Tests (RED)
# ============================================================================

class TestUserIsolation:
    """Test user_id isolation in MemoryClient - T068."""

    @pytest.mark.asyncio
    async def test_retrieve_memories_only_returns_own_user_memories(
        self, mock_httpx_client, mock_embedding_response
    ):
        """retrieve_memories must only return memories for the specified user_id."""
        from src.agents.memory.client import MemoryClient
        from dataclasses import dataclass

        @dataclass
        class MockScoredPoint:
            id: str
            score: float
            payload: dict

        # Create mock qdrant that stores all memories but returns filtered ones
        mock_qdrant = MagicMock()

        # When user-123 searches, only return user-123's memories (filtered by qdrant)
        mock_qdrant.search.return_value = [
            MockScoredPoint(
                id="mem-1",
                score=0.95,
                payload={"content": "User 123 conversation", "user_id": "user-123"}
            )
        ]

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant,
            http_client=mock_httpx_client
        )

        results = await client.retrieve_memories(
            query="What did we discuss?",
            user_id="user-123"
        )

        # Verify filter was applied correctly
        call_kwargs = mock_qdrant.search.call_args[1]
        query_filter = call_kwargs['query_filter']

        # The filter must contain user_id condition
        assert query_filter is not None
        assert len(query_filter.must) > 0
        # First condition should filter by user_id
        user_filter = query_filter.must[0]
        assert user_filter.key == "user_id"
        assert user_filter.match.value == "user-123"

    @pytest.mark.asyncio
    async def test_different_users_get_different_memories(
        self, mock_httpx_client, mock_embedding_response
    ):
        """Different users must get their own isolated memories."""
        from src.agents.memory.client import MemoryClient
        from dataclasses import dataclass

        @dataclass
        class MockScoredPoint:
            id: str
            score: float
            payload: dict

        mock_qdrant = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Setup to return different results based on filter
        def search_side_effect(**kwargs):
            query_filter = kwargs.get('query_filter')
            if query_filter and query_filter.must:
                user_id = query_filter.must[0].match.value
                if user_id == "user-alice":
                    return [
                        MockScoredPoint(
                            id="alice-1",
                            score=0.9,
                            payload={"content": "Alice's secret project", "user_id": "user-alice"}
                        )
                    ]
                elif user_id == "user-bob":
                    return [
                        MockScoredPoint(
                            id="bob-1",
                            score=0.85,
                            payload={"content": "Bob's todo list", "user_id": "user-bob"}
                        )
                    ]
            return []

        mock_qdrant.search.side_effect = search_side_effect

        client = MemoryClient(
            qdrant_client=mock_qdrant,
            http_client=mock_httpx_client
        )

        # Alice's query
        alice_results = await client.retrieve_memories(
            query="What was my project?",
            user_id="user-alice"
        )

        # Bob's query
        bob_results = await client.retrieve_memories(
            query="What was my project?",
            user_id="user-bob"
        )

        # Verify isolation
        assert alice_results == ["Alice's secret project"]
        assert bob_results == ["Bob's todo list"]
        assert alice_results != bob_results

    @pytest.mark.asyncio
    async def test_store_memory_includes_user_id_in_payload(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """store_memory must include user_id in the point payload."""
        from src.agents.memory.client import MemoryClient

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.store_memory(
            content="Test conversation",
            user_id="user-specific-123"
        )

        # Verify upsert was called with correct user_id
        call_kwargs = mock_qdrant_client.upsert.call_args[1]
        point = call_kwargs['points'][0]
        assert point.payload['user_id'] == "user-specific-123"

    @pytest.mark.asyncio
    async def test_user_cannot_access_other_users_memories(
        self, mock_httpx_client, mock_embedding_response
    ):
        """A user must not be able to access another user's memories."""
        from src.agents.memory.client import MemoryClient
        from dataclasses import dataclass

        @dataclass
        class MockScoredPoint:
            id: str
            score: float
            payload: dict

        mock_qdrant = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Qdrant filters properly - attacker gets empty results
        def search_side_effect(**kwargs):
            query_filter = kwargs.get('query_filter')
            if query_filter and query_filter.must:
                user_id = query_filter.must[0].match.value
                # Only victim's data exists, attacker gets nothing
                if user_id == "attacker":
                    return []  # No results for attacker
                elif user_id == "victim":
                    return [
                        MockScoredPoint(
                            id="victim-1",
                            score=0.99,
                            payload={"content": "Victim's sensitive data", "user_id": "victim"}
                        )
                    ]
            return []

        mock_qdrant.search.side_effect = search_side_effect

        client = MemoryClient(
            qdrant_client=mock_qdrant,
            http_client=mock_httpx_client
        )

        # Attacker tries to access victim's data
        attacker_results = await client.retrieve_memories(
            query="Show me victim's data",
            user_id="attacker"
        )

        # Victim accesses their own data
        victim_results = await client.retrieve_memories(
            query="Show me my data",
            user_id="victim"
        )

        # Attacker should get nothing
        assert attacker_results == []
        # Victim should get their data
        assert victim_results == ["Victim's sensitive data"]

    @pytest.mark.asyncio
    async def test_retrieve_memories_filter_structure_is_correct(
        self, mock_qdrant_client, mock_httpx_client, mock_embedding_response
    ):
        """The user_id filter must have the correct Qdrant filter structure."""
        from src.agents.memory.client import MemoryClient
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        mock_response = MagicMock()
        mock_response.json.return_value = mock_embedding_response
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=mock_httpx_client
        )

        await client.retrieve_memories(
            query="test query",
            user_id="test-user-456"
        )

        # Verify filter structure
        call_kwargs = mock_qdrant_client.search.call_args[1]
        query_filter = call_kwargs['query_filter']

        # Must be a Filter object
        assert isinstance(query_filter, Filter)
        # Must have 'must' conditions
        assert hasattr(query_filter, 'must')
        assert len(query_filter.must) >= 1
        # First condition must filter user_id
        condition = query_filter.must[0]
        assert isinstance(condition, FieldCondition)
        assert condition.key == "user_id"
        assert isinstance(condition.match, MatchValue)
        assert condition.match.value == "test-user-456"
