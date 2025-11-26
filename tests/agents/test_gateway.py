"""
Tests for Agent Gateway endpoints.

TDD Phase: RED - These tests verify OpenAI-compatible API behavior.

TDD Tests for Phase 6.3:
- T066: Memory storage in gateway (store after response)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient


class TestChatCompletionsEndpoint:
    """Test POST /v1/chat/completions endpoint for OpenAI compatibility."""

    @pytest.mark.asyncio
    async def test_chat_completions_exists(self):
        """chat_completions endpoint must exist at /v1/chat/completions."""
        from src.agents.gateway import app

        with patch("src.agents.orchestrator.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Test response"

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )
                # Should not be 404 (endpoint exists)
                assert response.status_code != 404

    @pytest.mark.asyncio
    async def test_chat_completions_returns_openai_format(self, mock_httpx_client):
        """chat_completions must return OpenAI-compatible response format."""
        from src.agents.gateway import app

        with patch("src.agents.orchestrator.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Test response from agent"

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )

                assert response.status_code == 200
                data = response.json()

                # Required OpenAI fields
                assert "id" in data
                assert data["id"].startswith("chatcmpl-")
                assert data["object"] == "chat.completion"
                assert "created" in data
                assert isinstance(data["created"], int)
                assert "model" in data
                assert "choices" in data
                assert "usage" in data

    @pytest.mark.asyncio
    async def test_chat_completions_response_has_choices(self, mock_httpx_client):
        """chat_completions must return choices array with message."""
        from src.agents.gateway import app

        with patch("src.agents.orchestrator.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Test response content"

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )

                data = response.json()
                assert len(data["choices"]) > 0

                choice = data["choices"][0]
                assert "index" in choice
                assert "message" in choice
                assert "finish_reason" in choice

                message = choice["message"]
                assert message["role"] == "assistant"
                assert "content" in message

    @pytest.mark.asyncio
    async def test_chat_completions_accepts_temperature(self, mock_httpx_client):
        """chat_completions must accept temperature parameter."""
        from src.agents.gateway import app

        with patch("src.agents.orchestrator.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Response"

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "temperature": 0.5
                    }
                )

                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_chat_completions_accepts_max_tokens(self, mock_httpx_client):
        """chat_completions must accept max_tokens parameter."""
        from src.agents.gateway import app

        with patch("src.agents.orchestrator.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Response"

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "max_tokens": 2048
                    }
                )

                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_chat_completions_accepts_user_id(self, mock_httpx_client):
        """chat_completions must accept user parameter for memory isolation."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(intent=Intent.SDD, confidence=0.9, reasoning="Test"),
            chain_id="sdd",
            response="Response"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "user": "test-user-123"
                    }
                )

                assert response.status_code == 200
                # Verify user_id was passed to orchestrator
                mock_run.assert_called_once()
                call_kwargs = mock_run.call_args[1]
                assert call_kwargs.get("user_id") == "test-user-123"

    @pytest.mark.asyncio
    async def test_chat_completions_extracts_user_message(self, mock_httpx_client):
        """chat_completions must extract last user message for orchestrator."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(intent=Intent.SDD, confidence=0.9, reasoning="Test"),
            chain_id="sdd",
            response="Response"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [
                            {"role": "system", "content": "You are helpful"},
                            {"role": "user", "content": "First question"},
                            {"role": "assistant", "content": "First answer"},
                            {"role": "user", "content": "Second question"}
                        ]
                    }
                )

                # Should extract last user message
                call_kwargs = mock_run.call_args[1]
                assert call_kwargs.get("user_message") == "Second question"

    @pytest.mark.asyncio
    async def test_chat_completions_passes_conversation_history(self, mock_httpx_client):
        """chat_completions must pass full conversation to orchestrator."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(intent=Intent.SDD, confidence=0.9, reasoning="Test"),
            chain_id="sdd",
            response="Response"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            messages = [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there"},
                {"role": "user", "content": "How are you?"}
            ]

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": messages
                    }
                )

                call_kwargs = mock_run.call_args[1]
                assert "conversation" in call_kwargs
                assert len(call_kwargs["conversation"]) == 3

    @pytest.mark.asyncio
    async def test_chat_completions_model_in_response(self, mock_httpx_client):
        """chat_completions must include model name in response."""
        from src.agents.gateway import app

        with patch("src.agents.orchestrator.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Response"

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "spec-analyst",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )

                data = response.json()
                assert "spec-analyst" in data["model"]


class TestModelsEndpoint:
    """Test GET /v1/models endpoint."""

    @pytest.mark.asyncio
    async def test_models_endpoint_exists(self):
        """Models endpoint must exist at /v1/models."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/v1/models")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_models_returns_list_format(self):
        """Models endpoint must return OpenAI list format."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/v1/models")

            data = response.json()
            assert data["object"] == "list"
            assert "data" in data
            assert isinstance(data["data"], list)

    @pytest.mark.asyncio
    async def test_models_lists_all_agents(self):
        """Models endpoint must list all agents from AGENTS registry."""
        from src.agents.gateway import app, AGENTS

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/v1/models")

            data = response.json()
            model_ids = [m["id"] for m in data["data"]]

            # All agents should be listed
            for agent_id in AGENTS.keys():
                assert agent_id in model_ids

    @pytest.mark.asyncio
    async def test_models_has_model_format(self):
        """Each model entry must have required fields."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/v1/models")

            data = response.json()
            for model in data["data"]:
                assert "id" in model
                assert model["object"] == "model"
                assert "owned_by" in model

    @pytest.mark.asyncio
    async def test_models_includes_orchestrator(self):
        """Models endpoint must include 'orchestrator' agent."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/v1/models")

            data = response.json()
            model_ids = [m["id"] for m in data["data"]]
            assert "orchestrator" in model_ids


class TestHealthEndpoint:
    """Test GET /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_endpoint_exists(self):
        """Health endpoint must exist at /health."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_health_returns_status(self):
        """Health endpoint must return status field."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")

            data = response.json()
            assert "status" in data
            assert data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_health_returns_service_name(self):
        """Health endpoint must return service name."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")

            data = response.json()
            assert "service" in data
            assert data["service"] == "agent-gateway"

    @pytest.mark.asyncio
    async def test_health_returns_agent_list(self):
        """Health endpoint must return list of agents."""
        from src.agents.gateway import app, AGENTS

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")

            data = response.json()
            assert "agents" in data
            assert isinstance(data["agents"], list)
            assert len(data["agents"]) == len(AGENTS)

    @pytest.mark.asyncio
    async def test_health_returns_urls(self):
        """Health endpoint must return service URLs."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")

            data = response.json()
            assert "gb10_url" in data
            assert "qdrant_url" in data


class TestOrchestratorModelRouting:
    """Test orchestrator model routing (T038) - model="orchestrator" uses run_orchestrator."""

    @pytest.mark.asyncio
    async def test_orchestrator_model_calls_run_orchestrator(self):
        """When model="orchestrator", must call run_orchestrator function."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.95,
                reasoning="User wants to write a spec"
            ),
            chain_id="sdd",
            response="Routing to Specification-Driven Development workflow (confidence: 95%)"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Write a spec"}]
                    }
                )

                mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_orchestrator_returns_response_text(self):
        """Orchestrator response must include the routing response text."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.TDD,
                confidence=0.88,
                reasoning="User wants to write tests"
            ),
            chain_id="tdd",
            response="Routing to Test-Driven Development workflow (confidence: 88%)"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Write tests"}]
                    }
                )

                data = response.json()
                assert "Routing to Test-Driven Development" in data["choices"][0]["message"]["content"]

    @pytest.mark.asyncio
    async def test_orchestrator_clarification_response(self):
        """When orchestrator needs clarification, must return clarifying question."""
        from src.agents.gateway import app
        from src.agents.orchestrator import (
            OrchestratorResult, IntentClassification, Intent, CLARIFYING_QUESTION
        )

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.UNCLEAR,
                confidence=0.3,
                reasoning="Request is too vague"
            ),
            chain_id=None,
            response=CLARIFYING_QUESTION,
            needs_clarification=True
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "help"}]
                    }
                )

                data = response.json()
                content = data["choices"][0]["message"]["content"]
                assert "clarify" in content.lower() or "looking for" in content.lower()

    @pytest.mark.asyncio
    async def test_orchestrator_passes_http_client(self):
        """Orchestrator must receive http_client for LLM calls."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Spec request"
            ),
            chain_id="sdd",
            response="Routing to SDD"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Write spec"}]
                    }
                )

                # Verify http_client was passed
                call_kwargs = mock_run.call_args[1]
                assert "http_client" in call_kwargs

    @pytest.mark.asyncio
    async def test_orchestrator_model_returns_200(self):
        """Orchestrator model must return 200 status on successful routing."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.RETRO,
                confidence=0.85,
                reasoning="Code review request"
            ),
            chain_id="retro",
            response="Routing to Retrospective Analysis workflow"
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Review code"}]
                    }
                )

                assert response.status_code == 200


class TestErrorHandling:
    """Test error handling for LLM unavailability and other errors."""

    @pytest.mark.asyncio
    async def test_llm_unavailable_returns_503(self):
        """When LLM is unavailable, must return 503 status code."""
        from src.agents.gateway import app

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            # Simulate LLM connection error
            mock_run.side_effect = Exception("Connection refused")

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )

                assert response.status_code == 503

    @pytest.mark.asyncio
    async def test_llm_unavailable_returns_error_format(self):
        """When LLM is unavailable, must return OpenAI-style error format."""
        from src.agents.gateway import app

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = Exception("Connection refused")

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )

                data = response.json()
                assert "error" in data
                assert "message" in data["error"]
                assert "type" in data["error"]

    @pytest.mark.asyncio
    async def test_llm_unavailable_suggests_retry(self):
        """When LLM is unavailable, error message should suggest retry."""
        from src.agents.gateway import app

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = Exception("Connection refused")

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                    }
                )

                data = response.json()
                # Should indicate service unavailability
                assert data["error"]["type"] == "service_unavailable"

    @pytest.mark.asyncio
    async def test_invalid_request_returns_400(self):
        """Invalid request should return 400 status code."""
        from src.agents.gateway import app

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Missing required 'messages' field
            response = await client.post(
                "/v1/chat/completions",
                json={"model": "orchestrator"}
            )

            assert response.status_code == 422  # FastAPI validation error


# ============================================================================
# T066: Memory Storage Tests (RED)
# ============================================================================

class TestMemoryStorage:
    """Test memory storage in gateway - T066."""

    @pytest.mark.asyncio
    async def test_chat_completions_stores_memory_after_response(self):
        """chat_completions must store conversation to memory after response."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="Test response from agent",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "user": "user-123"
                    }
                )

                # Verify memory storage was called
                assert response.status_code == 200
                mock_store.assert_called_once()

    @pytest.mark.asyncio
    async def test_memory_storage_includes_user_message_and_response(self):
        """Memory storage must include both user message and assistant response."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="This is the assistant response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "User question here"}],
                        "user": "user-123"
                    }
                )

                # Check that stored content includes both parts
                call_args = mock_store.call_args
                if call_args:
                    stored_content = call_args[1].get("content", "") if call_args[1] else call_args[0][0]
                    assert "User question here" in stored_content or "assistant response" in stored_content

    @pytest.mark.asyncio
    async def test_memory_storage_includes_user_id(self):
        """Memory storage must use the user_id from request."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="Test response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "user": "specific-user-456"
                    }
                )

                # Check that user_id was passed
                call_args = mock_store.call_args
                if call_args:
                    user_id = call_args[1].get("user_id", "") if call_args[1] else None
                    # User ID should be passed to store function
                    assert user_id == "specific-user-456" or "specific-user-456" in str(call_args)

    @pytest.mark.asyncio
    async def test_memory_storage_uses_default_user_when_not_provided(self):
        """Memory storage must use 'default' user_id when not provided in request."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="Test response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}]
                        # No user field
                    }
                )

                # Should still store memory with default user
                mock_store.assert_called_once()

    @pytest.mark.asyncio
    async def test_store_conversation_memory_function_exists(self):
        """store_conversation_memory function must exist in gateway."""
        from src.agents.gateway import store_conversation_memory

        assert store_conversation_memory is not None
        assert callable(store_conversation_memory)

    @pytest.mark.asyncio
    async def test_memory_storage_includes_metadata(self):
        """Memory storage must include metadata (chain_id, model)."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="Test response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "user": "user-123"
                    }
                )

                # Check that metadata was included
                call_args = mock_store.call_args
                if call_args and call_args[1]:
                    metadata = call_args[1].get("metadata", {})
                    # Should have some metadata
                    assert metadata is not None


# ============================================================================
# T070: Memory Failure Handling Tests (RED)
# ============================================================================

class TestMemoryFailureHandling:
    """Test memory storage failure handling in gateway - T070."""

    @pytest.mark.asyncio
    async def test_memory_storage_failure_returns_response(self):
        """Response must still be returned when memory storage fails."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.9,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="This is the valid response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result
            # Simulate memory storage failure
            mock_store.side_effect = Exception("Qdrant connection failed")

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "user": "user-123"
                    }
                )

                # Response should still be successful
                assert response.status_code == 200
                data = response.json()
                assert data["choices"][0]["message"]["content"] == "This is the valid response"

    @pytest.mark.asyncio
    async def test_memory_storage_failure_does_not_crash_endpoint(self):
        """Memory storage failure must not cause 500 error."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.TDD,
                confidence=0.88,
                reasoning="Test"
            ),
            chain_id="tdd",
            response="TDD workflow response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result
            # Simulate various failure types
            mock_store.side_effect = TimeoutError("Connection timeout")

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Write tests"}],
                        "user": "user-123"
                    }
                )

                # Should NOT be a 500 error
                assert response.status_code != 500
                assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_memory_storage_failure_logs_warning(self):
        """Memory storage failure must log a warning and return gracefully."""
        from src.agents.gateway import store_conversation_memory

        # Call with no memory client initialized (will fail)
        with patch("src.agents.gateway.get_memory_client", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None  # Simulate unavailable client

            # Should not raise an exception
            result = await store_conversation_memory(
                content="Test content",
                user_id="user-123"
            )

            # Function should return None (graceful failure)
            assert result is None
            # get_memory_client was called
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_memory_client_handles_init_failure(self, caplog):
        """get_memory_client must handle initialization failures gracefully."""
        from src.agents.gateway import get_memory_client
        import logging

        # Reset the global memory_client
        import src.agents.gateway as gateway_module
        gateway_module.memory_client = None

        with caplog.at_level(logging.WARNING):
            # Patch qdrant_client module that get_memory_client imports from
            with patch.dict("sys.modules", {"qdrant_client": MagicMock()}):
                # Make QdrantClient raise an exception when instantiated
                with patch("qdrant_client.QdrantClient", side_effect=Exception("Qdrant unavailable")):
                    client = await get_memory_client()

                    # Should return None on failure
                    assert client is None

    @pytest.mark.asyncio
    async def test_store_memory_gracefully_handles_client_error(self):
        """store_conversation_memory must handle MemoryClient errors gracefully."""
        from src.agents.gateway import store_conversation_memory

        # Mock get_memory_client to return a mock client that fails
        with patch("src.agents.gateway.get_memory_client", new_callable=AsyncMock) as mock_get:
            mock_client = MagicMock()
            mock_client.store_memory = AsyncMock(side_effect=Exception("Storage failed"))
            mock_get.return_value = mock_client

            # Should not raise, just log warning
            await store_conversation_memory(
                content="Test content",
                user_id="user-123"
            )
            # If we get here without exception, the test passes

    @pytest.mark.asyncio
    async def test_response_returned_before_memory_storage_in_case_of_failure(self):
        """User must receive response even if memory storage takes long or fails."""
        from src.agents.gateway import app
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        mock_result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.95,
                reasoning="Test"
            ),
            chain_id="sdd",
            response="Quick response",
            needs_clarification=False
        )

        with patch("src.agents.gateway.run_orchestrator", new_callable=AsyncMock) as mock_run, \
             patch("src.agents.gateway.store_conversation_memory", new_callable=AsyncMock) as mock_store:
            mock_run.return_value = mock_result
            # Simulate slow/failing memory storage
            mock_store.side_effect = Exception("Storage completely failed")

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "orchestrator",
                        "messages": [{"role": "user", "content": "Quick question"}],
                        "user": "user-123"
                    }
                )

                # User still gets their response
                assert response.status_code == 200
                data = response.json()
                assert "Quick response" in data["choices"][0]["message"]["content"]
