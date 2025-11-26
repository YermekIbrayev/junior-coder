"""
Pytest fixtures for agent tests.

Provides mock fixtures for:
- httpx client (LLM calls)
- qdrant client (vector memory)
- Common test data
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass


# ============================================================================
# HTTP Client Fixtures (for LLM calls to GB10)
# ============================================================================

@pytest.fixture
def mock_httpx_client():
    """Mock httpx.AsyncClient for LLM service calls."""
    client = AsyncMock()

    # Default successful response - using MagicMock for synchronous methods
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-oss-120b",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": "Test response"},
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15
        }
    }
    mock_response.raise_for_status = MagicMock()

    client.post.return_value = mock_response
    return client


@pytest.fixture
def mock_httpx_error():
    """Mock httpx.AsyncClient that raises connection error."""
    client = AsyncMock()
    client.post.side_effect = Exception("Connection refused")
    return client


# ============================================================================
# Qdrant Client Fixtures (for vector memory)
# ============================================================================

@pytest.fixture
def mock_qdrant_client():
    """Mock QdrantClient for memory operations."""
    client = MagicMock()

    # Mock search results
    @dataclass
    class MockScoredPoint:
        id: str
        score: float
        payload: dict

    client.search.return_value = [
        MockScoredPoint(
            id="mem-1",
            score=0.92,
            payload={"content": "Previous conversation 1", "user_id": "test-user"}
        ),
        MockScoredPoint(
            id="mem-2",
            score=0.85,
            payload={"content": "Previous conversation 2", "user_id": "test-user"}
        ),
        MockScoredPoint(
            id="mem-3",
            score=0.78,
            payload={"content": "Previous conversation 3", "user_id": "test-user"}
        )
    ]

    # Mock upsert
    client.upsert.return_value = None

    # Mock collection info
    client.get_collection.return_value = MagicMock(
        vectors_count=100,
        points_count=100
    )

    return client


@pytest.fixture
def mock_qdrant_empty():
    """Mock QdrantClient with no search results."""
    client = MagicMock()
    client.search.return_value = []
    return client


# ============================================================================
# Embedding Fixtures
# ============================================================================

@pytest.fixture
def mock_embedding_response():
    """Mock embedding response (1024-dim BGE-M3 format)."""
    return {
        "object": "list",
        "data": [{
            "object": "embedding",
            "index": 0,
            "embedding": [0.1] * 1024  # 1024-dim vector
        }],
        "model": "bge-m3",
        "usage": {"prompt_tokens": 10, "total_tokens": 10}
    }


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_messages():
    """Sample chat messages for testing."""
    return [
        {"role": "user", "content": "Write a spec for user authentication"}
    ]


@pytest.fixture
def sample_chat_request():
    """Sample OpenAI-compatible chat request."""
    return {
        "model": "orchestrator",
        "messages": [{"role": "user", "content": "Write tests for login function"}],
        "temperature": 0.7,
        "max_tokens": 4096,
        "user": "test-user"
    }


@pytest.fixture
def sample_agent_output():
    """Sample agent output for chain testing."""
    return {
        "agent_id": "spec-analyst",
        "content": "Analysis of user requirements...",
        "metadata": {"tokens_used": 150}
    }


# ============================================================================
# Async Test Helpers
# ============================================================================

@pytest.fixture
def event_loop_policy():
    """Use default event loop policy for async tests."""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()
