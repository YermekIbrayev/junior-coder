"""
Pytest configuration and fixtures for orchestrator tests

Provides mocks for Qdrant, HTTP clients, Mem0, and ApeRAG
Following TDD principles with comprehensive test fixtures
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_qdrant_client():
    """
    Mock Qdrant client for vector DB operations

    Provides mocked search and upsert methods to avoid real DB calls
    """
    client = MagicMock()

    # Mock search results (agent memories)
    client.search = AsyncMock(return_value=[
        MagicMock(
            payload={"content": "Test memory 1", "agent_id": "agent_test"},
            score=0.95
        ),
        MagicMock(
            payload={"content": "Test memory 2", "agent_id": "agent_test"},
            score=0.85
        )
    ])

    # Mock upsert (indexing)
    client.upsert = AsyncMock(return_value=MagicMock(status="completed"))

    return client


@pytest.fixture
def mock_http_client():
    """
    Mock httpx.AsyncClient for API calls to BGE-M3, GPT-OSS, etc.

    Returns mock responses for embedding and LLM calls
    """
    client = AsyncMock()

    # Mock embedding response
    client.post = AsyncMock(return_value=MagicMock(
        json=AsyncMock(return_value={
            "data": [{"embedding": [0.1] * 1024}]  # 1024-dim embedding
        }),
        status_code=200
    ))

    return client


@pytest.fixture
def mock_mem0():
    """
    Mock Mem0 AsyncMemory instance for agent long-term memory

    Provides mocked add and search methods
    """
    mem0 = AsyncMock()

    # Mock add memory
    mem0.add = AsyncMock(return_value={
        "id": "mem_123abc",
        "status": "success"
    })

    # Mock search memories
    mem0.search = AsyncMock(return_value=[
        {
            "content": "Previous conversation about testing",
            "user_id": "user_test",
            "agent_id": "agent_implementer",
            "timestamp": "2025-01-11T10:00:00Z",
            "score": 0.95
        },
        {
            "content": "Task state: implementing Mem0 integration",
            "user_id": "user_test",
            "agent_id": "agent_implementer",
            "timestamp": "2025-01-11T10:05:00Z",
            "score": 0.88
        }
    ])

    return mem0


@pytest.fixture
def mock_aperag():
    """
    Mock ApeRAG instance for project knowledge GraphRAG

    Provides mocked index_document, query, and query_graph methods
    """
    aperag = AsyncMock()

    # Mock document indexing
    aperag.index_document = AsyncMock(return_value={
        "id": "doc_456def",
        "entities_extracted": 5,
        "relationships_extracted": 3,
        "status": "indexed"
    })

    # Mock knowledge query
    aperag.query = AsyncMock(return_value=[
        {
            "content": "Code example: async def test_function()...",
            "doc_type": "code",
            "file_path": "src/services/mem0_client.py",
            "score": 0.92
        },
        {
            "content": "Documentation: Mem0 is a hybrid database...",
            "doc_type": "documentation",
            "file_path": "docs/architecture.md",
            "score": 0.87
        }
    ])

    # Mock graph traversal
    aperag.query_graph = AsyncMock(return_value=[
        {"entity": "Mem0Client", "relationship": "uses", "target": "AsyncMemory"},
        {"entity": "Mem0Client", "relationship": "connects_to", "target": "Qdrant"}
    ])

    return aperag


@pytest.fixture
def test_config():
    """
    Test configuration settings

    Provides URLs and collection names for testing
    """
    return {
        "QDRANT_URL": "http://test-qdrant:6333",
        "BGE_M3_URL": "http://test-bge:8001",
        "GPT_OSS_URL": "http://test-gpt:8000",
        "QWEN_ROUTER_URL": "http://test-qwen:8002",
        "QDRANT_COLLECTION_MEMORIES": "test_agent_memories",
        "QDRANT_COLLECTION_KNOWLEDGE": "test_project_knowledge",
        "QDRANT_COLLECTION_SHARED": "test_shared_context"
    }


@pytest.fixture
async def async_test_client():
    """
    Async test client for FastAPI integration tests

    Provides httpx.AsyncClient configured for testing
    """
    from httpx import AsyncClient
    from main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
