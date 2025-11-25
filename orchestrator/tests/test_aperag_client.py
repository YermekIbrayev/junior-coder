"""
TDD RED Phase: Tests for ApeRAGClient

Tests for project knowledge GraphRAG with Qdrant backend
These tests will FAIL until we implement services/aperag_client.py (GREEN phase)
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestApeRAGClientInitialization:
    """Test ApeRAGClient initialization and configuration"""

    @patch('services.aperag_client.QdrantClient')
    @patch('services.aperag_client.httpx.AsyncClient')
    def test_init_creates_clients(self, mock_http_client, mock_qdrant_client, test_config):
        """Test that ApeRAGClient initializes Qdrant and HTTP clients"""
        from services.aperag_client import ApeRAGClient

        client = ApeRAGClient(
            qdrant_url=test_config["QDRANT_URL"],
            embedding_url=test_config["BGE_M3_URL"],
            collection_name=test_config["QDRANT_COLLECTION_KNOWLEDGE"]
        )

        # Verify QdrantClient was initialized
        mock_qdrant_client.assert_called_once_with(url=test_config["QDRANT_URL"])

        # Verify AsyncClient was initialized
        mock_http_client.assert_called_once()

        # Verify attributes
        assert client.embedding_url == test_config["BGE_M3_URL"]
        assert client.collection_name == test_config["QDRANT_COLLECTION_KNOWLEDGE"]


class TestApeRAGClientIndexDocument:
    """Test indexing documents"""

    @pytest.mark.asyncio
    @patch('services.aperag_client.QdrantClient')
    @patch('services.aperag_client.httpx.AsyncClient')
    async def test_index_document_success(self, mock_http_client_class, mock_qdrant_client_class):
        """Test successfully indexing a document"""
        from services.aperag_client import ApeRAGClient

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

        client = ApeRAGClient(
            qdrant_url="http://test:6333",
            embedding_url="http://test:8001",
            collection_name="test_knowledge"
        )

        result = await client.index_document(
            content="def test_function(): pass",
            metadata={
                "doc_type": "code",
                "file_path": "src/test.py",
                "project_id": "test_project"
            }
        )

        # Verify embedding was called
        mock_http.post.assert_called_once()

        # Verify upsert was called
        mock_qdrant.upsert.assert_called_once()

        # Verify result format
        assert "id" in result
        assert result["id"].startswith("doc_")
        assert result["status"] == "indexed"

    @pytest.mark.asyncio
    @patch('services.aperag_client.QdrantClient')
    @patch('services.aperag_client.httpx.AsyncClient')
    async def test_index_document_with_metadata(self, mock_http_client_class, mock_qdrant_client_class):
        """Test that document metadata is properly stored"""
        from services.aperag_client import ApeRAGClient

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

        client = ApeRAGClient("http://test:6333", "http://test:8001", "test_knowledge")

        await client.index_document(
            content="Test content",
            metadata={
                "doc_type": "documentation",
                "file_path": "docs/README.md",
                "language": "markdown"
            }
        )

        # Verify metadata in upsert call
        call_args = mock_qdrant.upsert.call_args
        points = call_args.kwargs["points"]
        assert len(points) == 1
        assert points[0].payload["doc_type"] == "documentation"
        assert points[0].payload["file_path"] == "docs/README.md"
        assert points[0].payload["language"] == "markdown"


class TestApeRAGClientQueryKnowledge:
    """Test querying project knowledge"""

    @pytest.mark.asyncio
    @patch('services.aperag_client.QdrantClient')
    @patch('services.aperag_client.httpx.AsyncClient')
    async def test_query_knowledge_success(self, mock_http_client_class, mock_qdrant_client_class):
        """Test successfully querying knowledge"""
        from services.aperag_client import ApeRAGClient

        # Setup mocks
        mock_qdrant = MagicMock()
        mock_hit1 = MagicMock()
        mock_hit1.payload = {
            "content": "Code example for testing",
            "doc_type": "code",
            "file_path": "src/test.py"
        }
        mock_hit1.score = 0.92

        mock_qdrant.search = MagicMock(return_value=[mock_hit1])
        mock_qdrant_client_class.return_value = mock_qdrant

        mock_http = AsyncMock()
        mock_response = MagicMock()
        mock_response.json = MagicMock(return_value={
            "data": [{"embedding": [0.1] * 1024}]
        })
        mock_http.post = AsyncMock(return_value=mock_response)
        mock_http_client_class.return_value = mock_http

        client = ApeRAGClient("http://test:6333", "http://test:8001", "test_knowledge")

        results = await client.query_knowledge(
            query="how to write tests",
            filters={"doc_type": "code"},
            top_k=5
        )

        # Verify search was called
        mock_qdrant.search.assert_called_once()

        # Verify results
        assert len(results) == 1
        assert results[0]["doc_type"] == "code"
        assert results[0]["score"] == 0.92

    @pytest.mark.asyncio
    @patch('services.aperag_client.QdrantClient')
    @patch('services.aperag_client.httpx.AsyncClient')
    async def test_query_knowledge_with_filters(self, mock_http_client_class, mock_qdrant_client_class):
        """Test querying with metadata filters"""
        from services.aperag_client import ApeRAGClient

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

        client = ApeRAGClient("http://test:6333", "http://test:8001", "test_knowledge")

        await client.query_knowledge(
            query="test",
            filters={"doc_type": "documentation", "project_id": "proj_123"},
            top_k=10
        )

        # Verify search was called
        mock_qdrant.search.assert_called_once()

        # Verify filter was applied
        call_kwargs = mock_qdrant.search.call_args.kwargs
        query_filter = call_kwargs.get("query_filter")
        assert query_filter is not None
