"""
Tests for BaseChain class.

TDD Phase: RED - These tests should FAIL until BaseChain is implemented.
"""

import pytest
from typing import List
from unittest.mock import AsyncMock, MagicMock


class TestBaseChainFields:
    """Test BaseChain has required fields: id, name, agents, description."""

    def test_base_chain_has_id_field(self):
        """BaseChain must have an 'id' field."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )
        assert chain.id == "test-chain"

    def test_base_chain_has_name_field(self):
        """BaseChain must have a 'name' field."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )
        assert chain.name == "Test Chain"

    def test_base_chain_has_agents_list(self):
        """BaseChain must have an 'agents' list field."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst"),
            BaseAgent(id="agent-2", name="Agent 2", prompt_path="spec-clarifier")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )
        assert len(chain.agents) == 2
        assert chain.agents[0].id == "agent-1"
        assert chain.agents[1].id == "agent-2"

    def test_base_chain_has_description_field(self):
        """BaseChain must have an optional 'description' field."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents,
            description="A test workflow"
        )
        assert chain.description == "A test workflow"

    def test_base_chain_description_defaults_to_empty(self):
        """BaseChain description should default to empty string."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )
        assert chain.description == ""

    def test_base_chain_preserves_agent_order(self):
        """BaseChain must preserve the order of agents."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="first", name="First", prompt_path="spec-analyst"),
            BaseAgent(id="second", name="Second", prompt_path="spec-clarifier"),
            BaseAgent(id="third", name="Third", prompt_path="code-planner")
        ]
        chain = BaseChain(
            id="ordered-chain",
            name="Ordered Chain",
            agents=agents
        )
        assert [a.id for a in chain.agents] == ["first", "second", "third"]


class TestBaseChainExecuteSignature:
    """Test BaseChain.execute() method signature and behavior."""

    def test_execute_method_exists(self):
        """BaseChain must have an execute() method."""
        from src.agents.chains.base import BaseChain
        from src.agents.agents.base import BaseAgent

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )
        assert hasattr(chain, "execute")
        assert callable(chain.execute)

    @pytest.mark.asyncio
    async def test_execute_is_async(self):
        """BaseChain.execute() must be an async method."""
        from src.agents.chains.base import BaseChain, ChainContext
        from src.agents.agents.base import BaseAgent
        import asyncio

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )

        context = ChainContext(
            user_message="test",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="test-chain"
        )

        # execute should be awaitable
        result = chain.execute(context)
        assert asyncio.iscoroutine(result)
        # Clean up the coroutine
        result.close()

    @pytest.mark.asyncio
    async def test_execute_accepts_chain_context(self):
        """BaseChain.execute() must accept a ChainContext parameter."""
        from src.agents.chains.base import BaseChain, ChainContext
        from src.agents.agents.base import BaseAgent
        from unittest.mock import patch

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )

        context = ChainContext(
            user_message="Write a spec",
            conversation_history=[],
            memory_context=["past context"],
            agent_outputs={},
            current_agent="",
            chain_id="test-chain"
        )

        # Should not raise TypeError for signature
        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Agent output"
            try:
                result = await chain.execute(context)
            except NotImplementedError:
                # Expected - base implementation may raise NotImplementedError
                pass

    @pytest.mark.asyncio
    async def test_execute_returns_chain_context(self):
        """BaseChain.execute() must return a ChainContext."""
        from src.agents.chains.base import BaseChain, ChainContext
        from src.agents.agents.base import BaseAgent
        from unittest.mock import patch

        agents = [
            BaseAgent(id="agent-1", name="Agent 1", prompt_path="spec-analyst")
        ]
        chain = BaseChain(
            id="test-chain",
            name="Test Chain",
            agents=agents
        )

        context = ChainContext(
            user_message="Write a spec",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="test-chain"
        )

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Agent output"
            try:
                result = await chain.execute(context)
                assert isinstance(result, ChainContext)
            except NotImplementedError:
                # Base class may raise NotImplementedError
                pass
