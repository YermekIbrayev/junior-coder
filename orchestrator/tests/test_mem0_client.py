"""
TDD Tests for Mem0Client

Tests for agent long-term memory management with Qdrant backend
Updated to work with direct Qdrant integration (no mem0 library dependency)
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestMem0ClientInitialization:
    """Test Mem0Client initialization and configuration"""

    @patch('services.mem0_client.QdrantClient')
    @patch('services.mem0_client.httpx.AsyncClient')
    def test_init_creates_clients(self, mock_http_client, mock_qdrant_client, test_config):
        """Test that Mem0Client initializes Qdrant and HTTP clients"""
        from services.mem0_client import Mem0Client

        client = Mem0Client(
            qdrant_url=test_config["QDRANT_URL"],
            embedding_url=test_config["BGE_M3_URL"],
            collection_name=test_config["QDRANT_COLLECTION_MEMORIES"]
        )

        # Verify QdrantClient was initialized
        mock_qdrant_client.assert_called_once_with(url=test_config["QDRANT_URL"])

        # Verify AsyncClient was initialized
        mock_http_client.assert_called_once()

        # Verify attributes set correctly
        assert client.embedding_url == test_config["BGE_M3_URL"]
        assert client.collection_name == test_config["QDRANT_COLLECTION_MEMORIES"]


class TestMem0ClientAddMemory:
    """Test adding memories to Qdrant"""

    @pytest.mark.asyncio
    @patch('services.mem0_client.QdrantClient')
    @patch('services.mem0_client.httpx.AsyncClient')
    async def test_add_memory_success(self, mock_http_client_class, mock_qdrant_client_class):
        """Test successfully adding a memory"""
        from services.mem0_client import Mem0Client

        # Setup mocks
        mock_qdrant = MagicMock()
        mock_qdrant.upsert = MagicMock(return_value=None)
        mock_qdrant_client_class.return_value = mock_qdrant

        mock_http = AsyncMock()
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value={
            "data": [{"embedding": [0.1] * 1024}]
        })
        mock_http.post = AsyncMock(return_value=mock_response)
        mock_http_client_class.return_value = mock_http

        # Create client
        client = Mem0Client(
            qdrant_url="http://test:6333",
            embedding_url="http://test:8001",
            collection_name="test_memories"
        )

        # Add memory
        result = await client.add_memory(
            user_id="user_test",
            agent_id="agent_implementer",
            messages=[{"role": "user", "content": "Test message"}],
            metadata={"task": "testing"}
        )

        # Verify embedding was called
        mock_http.post.assert_called_once()

        # Verify upsert was called
        mock_qdrant.upsert.assert_called_once()

        # Verify result format
        assert "id" in result
        assert result["id"].startswith("mem_")
        assert result["status"] == "success"

    @pytest.mark.asyncio
    @patch('services.mem0_client.QdrantClient')
    @patch('services.mem0_client.httpx.AsyncClient')
    async def test_add_memory_includes_agent_id(self, mock_http_client_class, mock_qdrant_client_class):
        """Test that agent_id is properly stored in payload"""
        from services.mem0_client import Mem0Client

        # Setup mocks
        mock_qdrant = MagicMock()
        mock_qdrant.upsert = MagicMock(return_value=None)
        mock_qdrant_client_class.return_value = mock_qdrant

        mock_http = AsyncMock()
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value={
            "data": [{"embedding": [0.1] * 1024}]
        })
        mock_http.post = AsyncMock(return_value=mock_response)
        mock_http_client_class.return_value = mock_http

        client = Mem0Client("http://test:6333", "http://test:8001", "test_memories")

        await client.add_memory(
            user_id="user_test",
            agent_id="agent_planner",
            messages=[{"role": "user", "content": "Test"}],
            metadata={}
        )

        # Verify agent_id in upsert call
        call_args = mock_qdrant.upsert.call_args
        points = call_args.kwargs["points"]
        assert len(points) == 1
        assert points[0].payload["agent_id"] == "agent_planner"
        assert points[0].payload["user_id"] == "user_test"


class TestMem0ClientSearchMemories:
    """Test searching memories in Qdrant"""

    @pytest.mark.asyncio
    @patch('services.mem0_client.QdrantClient')
    @patch('services.mem0_client.httpx.AsyncClient')
    async def test_search_memories_success(self, mock_http_client_class, mock_qdrant_client_class):
        """Test successfully searching memories"""
        from services.mem0_client import Mem0Client

        # Setup mocks
        mock_qdrant = MagicMock()
        mock_hit1 = MagicMock()
        mock_hit1.payload = {
            "content": "Test memory 1",
            "user_id": "user_test",
            "agent_id": "agent_implementer",
            "timestamp": 1704997200.0
        }
        mock_hit1.score = 0.95

        mock_hit2 = MagicMock()
        mock_hit2.payload = {
            "content": "Test memory 2",
            "user_id": "user_test",
            "agent_id": "agent_implementer",
            "timestamp": 1704997300.0
        }
        mock_hit2.score = 0.85

        mock_qdrant.search = MagicMock(return_value=[mock_hit1, mock_hit2])
        mock_qdrant_client_class.return_value = mock_qdrant

        mock_http = AsyncMock()
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value={
            "data": [{"embedding": [0.1] * 1024}]
        })
        mock_http.post = AsyncMock(return_value=mock_response)
        mock_http_client_class.return_value = mock_http

        client = Mem0Client("http://test:6333", "http://test:8001", "test_memories")

        results = await client.search_memories(
            query="test query",
            user_id="user_test",
            agent_id="agent_implementer",
            limit=5
        )

        # Verify search was called
        mock_qdrant.search.assert_called_once()

        # Verify results
        assert len(results) == 2
        assert results[0]["agent_id"] == "agent_implementer"
        assert results[0]["content"] == "Test memory 1"
        assert results[0]["score"] == 0.95

    @pytest.mark.asyncio
    @patch('services.mem0_client.QdrantClient')
    @patch('services.mem0_client.httpx.AsyncClient')
    async def test_search_memories_cross_agent(self, mock_http_client_class, mock_qdrant_client_class):
        """Test searching memories across all agents (no agent_id filter)"""
        from services.mem0_client import Mem0Client

        # Setup mocks
        mock_qdrant = MagicMock()
        mock_qdrant.search = MagicMock(return_value=[])
        mock_qdrant_client_class.return_value = mock_qdrant

        mock_http = AsyncMock()
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value={
            "data": [{"embedding": [0.1] * 1024}]
        })
        mock_http.post = AsyncMock(return_value=mock_response)
        mock_http_client_class.return_value = mock_http

        client = Mem0Client("http://test:6333", "http://test:8001", "test_memories")

        await client.search_memories(
            query="test query",
            user_id="user_test",
            agent_id=None,  # Search across all agents
            limit=10
        )

        # Verify search was called
        mock_qdrant.search.assert_called_once()

        # Verify filter only has user_id (not agent_id)
        call_kwargs = mock_qdrant.search.call_args.kwargs
        query_filter = call_kwargs.get("query_filter")
        if query_filter:
            # Filter should only contain user_id condition
            filter_conditions = query_filter.must
            assert len(filter_conditions) == 1  # Only user_id, no agent_id
