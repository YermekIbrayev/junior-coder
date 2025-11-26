"""
Tests for OpenAI-compatible streaming in Agent Gateway.

TDD RED Phase: These tests define expected streaming behavior.
"""

import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def mock_orchestrator():
    """Mock the orchestrator to return a simple response."""
    with patch("src.agents.gateway.run_orchestrator") as mock:
        result = MagicMock()
        result.chain_id = "test-chain"
        result.classification = MagicMock()
        result.classification.intent.value = "tdd"
        result.classification.confidence = 0.9
        result.chain_output = None
        result.response = "Hello! How can I help you today?"
        mock.return_value = result
        yield mock


@pytest.fixture
def client(mock_orchestrator):
    """Create test client with mocked orchestrator."""
    from src.agents.gateway import app
    return TestClient(app)


# =============================================================================
# Test: Streaming Response Type
# =============================================================================

class TestStreamingResponseType:
    """Verify streaming returns correct response type."""

    def test_stream_true_returns_event_stream(self, client):
        """When stream=True, Content-Type should be text/event-stream."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    def test_stream_false_returns_json(self, client):
        """When stream=False, Content-Type should be application/json."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": False
            }
        )
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")


# =============================================================================
# Test: SSE Chunk Format
# =============================================================================

class TestSSEChunkFormat:
    """Verify SSE chunks follow OpenAI format."""

    def parse_sse_chunks(self, response_text: str) -> list:
        """Parse SSE response into list of data chunks."""
        chunks = []
        for line in response_text.split("\n"):
            if line.startswith("data: "):
                data = line[6:]  # Remove "data: " prefix
                if data != "[DONE]":
                    chunks.append(json.loads(data))
                else:
                    chunks.append("[DONE]")
        return chunks

    def test_first_chunk_has_role(self, client):
        """First chunk delta should contain role: assistant."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        chunks = self.parse_sse_chunks(response.text)

        assert len(chunks) > 0, "Should have at least one chunk"
        first_chunk = chunks[0]
        assert first_chunk["choices"][0]["delta"].get("role") == "assistant"

    def test_chunks_have_correct_structure(self, client):
        """Each chunk should have id, object, created, model, choices."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        chunks = self.parse_sse_chunks(response.text)

        for chunk in chunks:
            if chunk == "[DONE]":
                continue
            assert "id" in chunk
            assert chunk["object"] == "chat.completion.chunk"
            assert "created" in chunk
            assert "model" in chunk
            assert "choices" in chunk
            assert len(chunk["choices"]) > 0

    def test_content_chunks_have_delta_content(self, client):
        """Middle chunks should have content in delta."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        chunks = self.parse_sse_chunks(response.text)

        # Skip first (role) and last (finish) chunks, and [DONE]
        content_chunks = [c for c in chunks[1:-1] if c != "[DONE]"]

        # Should have content chunks if response has multiple words
        if content_chunks:
            for chunk in content_chunks:
                delta = chunk["choices"][0]["delta"]
                # Content chunks should have content key
                assert "content" in delta or delta == {}

    def test_final_chunk_has_finish_reason(self, client):
        """Last data chunk (before [DONE]) should have finish_reason: stop."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        chunks = self.parse_sse_chunks(response.text)

        # Find last non-[DONE] chunk
        data_chunks = [c for c in chunks if c != "[DONE]"]
        assert len(data_chunks) > 0

        final_chunk = data_chunks[-1]
        assert final_chunk["choices"][0]["finish_reason"] == "stop"

    def test_stream_ends_with_done(self, client):
        """Stream should end with data: [DONE]."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        chunks = self.parse_sse_chunks(response.text)

        assert chunks[-1] == "[DONE]", "Stream should end with [DONE]"


# =============================================================================
# Test: Content Reconstruction
# =============================================================================

class TestContentReconstruction:
    """Verify streamed content matches non-streamed response."""

    def parse_sse_chunks(self, response_text: str) -> list:
        """Parse SSE response into list of data chunks."""
        chunks = []
        for line in response_text.split("\n"):
            if line.startswith("data: "):
                data = line[6:]
                if data != "[DONE]":
                    chunks.append(json.loads(data))
        return chunks

    def test_streamed_content_matches_full_response(self, client):
        """Concatenated stream content should match non-stream response."""
        # Get non-streaming response
        non_stream_response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": False
            }
        )
        expected_content = non_stream_response.json()["choices"][0]["message"]["content"]

        # Get streaming response
        stream_response = client.post(
            "/v1/chat/completions",
            json={
                "model": "orchestrator",
                "messages": [{"role": "user", "content": "Hi"}],
                "stream": True
            }
        )
        chunks = self.parse_sse_chunks(stream_response.text)

        # Reconstruct content from chunks
        reconstructed = ""
        for chunk in chunks:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                reconstructed += delta["content"]

        assert reconstructed.strip() == expected_content.strip()
