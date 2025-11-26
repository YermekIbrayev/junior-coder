"""
Tests for AgentRunner class.

TDD Phase: RED - These tests should FAIL until AgentRunner is implemented.

TDD Tests for Phase 6.3:
- T064: Memory retrieval in AgentRunner (retrieve before LLM call)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestAgentRunnerCallLLM:
    """Test AgentRunner.call_llm() method for GB10 LLM calls."""

    @pytest.mark.asyncio
    async def test_call_llm_exists(self):
        """AgentRunner must have a call_llm async method."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner()
        assert hasattr(runner, "call_llm")

    @pytest.mark.asyncio
    async def test_call_llm_sends_post_request(self, mock_httpx_client):
        """call_llm must send POST request to LLM endpoint."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner(http_client=mock_httpx_client)
        messages = [{"role": "user", "content": "Hello"}]

        await runner.call_llm(messages)

        mock_httpx_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_llm_uses_correct_endpoint(self, mock_httpx_client):
        """call_llm must use /v1/chat/completions endpoint."""
        from src.agents.agents.runner import AgentRunner, LLM_BASE_URL

        runner = AgentRunner(http_client=mock_httpx_client)
        messages = [{"role": "user", "content": "Hello"}]

        await runner.call_llm(messages)

        call_args = mock_httpx_client.post.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url")
        assert "/v1/chat/completions" in url

    @pytest.mark.asyncio
    async def test_call_llm_sends_openai_format(self, mock_httpx_client):
        """call_llm must send messages in OpenAI chat format."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner(http_client=mock_httpx_client)
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"}
        ]

        await runner.call_llm(messages)

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        assert "messages" in json_data
        assert json_data["messages"] == messages

    @pytest.mark.asyncio
    async def test_call_llm_returns_response_content(self, mock_httpx_client):
        """call_llm must return the assistant's message content."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner(http_client=mock_httpx_client)
        messages = [{"role": "user", "content": "Hello"}]

        result = await runner.call_llm(messages)

        assert result == "Test response"

    @pytest.mark.asyncio
    async def test_call_llm_with_temperature(self, mock_httpx_client):
        """call_llm must accept optional temperature parameter."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner(http_client=mock_httpx_client)
        messages = [{"role": "user", "content": "Hello"}]

        await runner.call_llm(messages, temperature=0.5)

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        assert json_data.get("temperature") == 0.5

    @pytest.mark.asyncio
    async def test_call_llm_with_max_tokens(self, mock_httpx_client):
        """call_llm must accept optional max_tokens parameter."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner(http_client=mock_httpx_client)
        messages = [{"role": "user", "content": "Hello"}]

        await runner.call_llm(messages, max_tokens=2048)

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        assert json_data.get("max_tokens") == 2048

    @pytest.mark.asyncio
    async def test_call_llm_raises_on_error(self, mock_httpx_error):
        """call_llm must raise exception on connection error."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner(http_client=mock_httpx_error)
        messages = [{"role": "user", "content": "Hello"}]

        with pytest.raises(Exception):
            await runner.call_llm(messages)


class TestAgentRunnerRunAgent:
    """Test AgentRunner.run_agent() method for full agent execution."""

    @pytest.mark.asyncio
    async def test_run_agent_exists(self):
        """AgentRunner must have a run_agent async method."""
        from src.agents.agents.runner import AgentRunner

        runner = AgentRunner()
        assert hasattr(runner, "run_agent")

    @pytest.mark.asyncio
    async def test_run_agent_loads_prompt(self, mock_httpx_client):
        """run_agent must load the agent's prompt from prompt_path."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        await runner.run_agent(agent, "Test user message")

        # Verify prompt was loaded and included in LLM call
        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        messages = json_data.get("messages", [])

        # Should have system message with prompt content
        system_messages = [m for m in messages if m.get("role") == "system"]
        assert len(system_messages) > 0

    @pytest.mark.asyncio
    async def test_run_agent_includes_user_message(self, mock_httpx_client):
        """run_agent must include the user's message."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        await runner.run_agent(agent, "Write a spec for authentication")

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        messages = json_data.get("messages", [])

        # Should have user message
        user_messages = [m for m in messages if m.get("role") == "user"]
        assert len(user_messages) > 0
        assert "Write a spec for authentication" in user_messages[-1]["content"]

    @pytest.mark.asyncio
    async def test_run_agent_returns_response(self, mock_httpx_client):
        """run_agent must return the LLM response."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        result = await runner.run_agent(agent, "Test message")

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_run_agent_with_context(self, mock_httpx_client):
        """run_agent must accept optional context parameter."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        context = "Previous agent said: Analysis complete."
        await runner.run_agent(agent, "Continue work", context=context)

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        messages = json_data.get("messages", [])

        # Context should be included somehow in the messages
        all_content = " ".join(m.get("content", "") for m in messages)
        assert "Previous agent said" in all_content or context in all_content

    @pytest.mark.asyncio
    async def test_run_agent_with_conversation_history(self, mock_httpx_client):
        """run_agent must accept optional conversation_history parameter."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        history = [
            {"role": "user", "content": "What is TDD?"},
            {"role": "assistant", "content": "Test-Driven Development..."}
        ]
        await runner.run_agent(agent, "Show me an example", conversation_history=history)

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        messages = json_data.get("messages", [])

        # History should be included in messages
        assert len(messages) >= 3  # system + history + current user


class TestAgentRunnerConstants:
    """Test AgentRunner constants and configuration."""

    def test_llm_base_url_constant_exists(self):
        """LLM_BASE_URL constant must be defined."""
        from src.agents.agents.runner import LLM_BASE_URL

        assert LLM_BASE_URL is not None
        assert "192.168.51.22" in LLM_BASE_URL or "localhost" in LLM_BASE_URL

    def test_default_temperature_constant(self):
        """DEFAULT_TEMPERATURE constant should be defined."""
        from src.agents.agents.runner import DEFAULT_TEMPERATURE

        assert isinstance(DEFAULT_TEMPERATURE, float)
        assert 0.0 <= DEFAULT_TEMPERATURE <= 2.0

    def test_default_max_tokens_constant(self):
        """DEFAULT_MAX_TOKENS constant should be defined."""
        from src.agents.agents.runner import DEFAULT_MAX_TOKENS

        assert isinstance(DEFAULT_MAX_TOKENS, int)
        assert DEFAULT_MAX_TOKENS > 0


# ============================================================================
# T064: Memory Retrieval Tests (RED)
# ============================================================================

class TestMemoryRetrieval:
    """Test memory retrieval in AgentRunner - T064."""

    @pytest.mark.asyncio
    async def test_run_agent_accepts_memory_client(self, mock_httpx_client):
        """run_agent must accept an optional memory_client parameter."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        # Should accept memory_client parameter without error
        result = await runner.run_agent(
            agent=agent,
            user_message="Test message",
            memory_client=None
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_run_agent_retrieves_memories_before_llm(
        self, mock_httpx_client, mock_qdrant_client, mock_embedding_response
    ):
        """run_agent must retrieve memories before calling LLM."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent
        from src.agents.memory.client import MemoryClient

        # Setup mock memory client
        mock_memory_response = MagicMock()
        mock_memory_response.json.return_value = mock_embedding_response
        mock_memory_response.raise_for_status = MagicMock()

        memory_http_client = AsyncMock()
        memory_http_client.post.return_value = mock_memory_response

        memory_client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=memory_http_client
        )

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        await runner.run_agent(
            agent=agent,
            user_message="What did we discuss earlier?",
            user_id="user-123",
            memory_client=memory_client
        )

        # Verify memory retrieval was called
        memory_http_client.post.assert_called()

    @pytest.mark.asyncio
    async def test_run_agent_includes_memories_in_context(
        self, mock_httpx_client, mock_qdrant_client, mock_embedding_response
    ):
        """run_agent must include retrieved memories in context."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent
        from src.agents.memory.client import MemoryClient

        # Setup mock memory client
        mock_memory_response = MagicMock()
        mock_memory_response.json.return_value = mock_embedding_response
        mock_memory_response.raise_for_status = MagicMock()

        memory_http_client = AsyncMock()
        memory_http_client.post.return_value = mock_memory_response

        memory_client = MemoryClient(
            qdrant_client=mock_qdrant_client,
            http_client=memory_http_client
        )

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        await runner.run_agent(
            agent=agent,
            user_message="Follow up question",
            user_id="user-123",
            memory_client=memory_client
        )

        # Check that LLM was called with context containing memories
        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        messages = json_data.get("messages", [])

        # Find system message and check for memory content
        all_content = " ".join(m.get("content", "") for m in messages)
        # Should contain something from the mock memories
        assert "Previous conversation" in all_content or "Relevant Memories" in all_content

    @pytest.mark.asyncio
    async def test_run_agent_accepts_user_id(self, mock_httpx_client):
        """run_agent must accept a user_id parameter for memory isolation."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        # Should accept user_id parameter without error
        result = await runner.run_agent(
            agent=agent,
            user_message="Test message",
            user_id="user-123"
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_run_agent_works_without_memory_client(self, mock_httpx_client):
        """run_agent must work correctly without memory_client (backward compatible)."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        # Should work without memory_client
        result = await runner.run_agent(
            agent=agent,
            user_message="Test message"
        )

        assert result == "Test response"

    @pytest.mark.asyncio
    async def test_run_agent_handles_empty_memories(
        self, mock_httpx_client, mock_qdrant_empty, mock_embedding_response
    ):
        """run_agent must handle empty memory results gracefully."""
        from src.agents.agents.runner import AgentRunner
        from src.agents.agents.base import BaseAgent
        from src.agents.memory.client import MemoryClient

        # Setup mock memory client with empty results
        mock_memory_response = MagicMock()
        mock_memory_response.json.return_value = mock_embedding_response
        mock_memory_response.raise_for_status = MagicMock()

        memory_http_client = AsyncMock()
        memory_http_client.post.return_value = mock_memory_response

        memory_client = MemoryClient(
            qdrant_client=mock_qdrant_empty,
            http_client=memory_http_client
        )

        runner = AgentRunner(http_client=mock_httpx_client)
        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        # Should work even with no memories
        result = await runner.run_agent(
            agent=agent,
            user_message="Test message",
            user_id="user-123",
            memory_client=memory_client
        )

        assert result == "Test response"

    @pytest.mark.asyncio
    async def test_module_run_agent_accepts_memory_client(
        self, mock_httpx_client
    ):
        """Module-level run_agent must accept memory_client parameter."""
        from src.agents.agents.runner import run_agent
        from src.agents.agents.base import BaseAgent

        agent = BaseAgent(
            id="spec-analyst",
            name="Spec Analyst",
            prompt_path="spec-analyst"
        )

        # Should accept memory_client parameter
        result = await run_agent(
            agent=agent,
            context="",
            user_message="Test message",
            http_client=mock_httpx_client,
            memory_client=None,
            user_id="user-123"
        )

        assert result is not None
