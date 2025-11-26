"""
Tests for ChainContext dataclass.

TDD Phase: RED - These tests validate ChainContext has all required fields.
"""

import pytest
from typing import Dict, List


class TestChainContextFields:
    """Test ChainContext has all required fields per data model."""

    def test_chain_context_has_user_message_field(self):
        """ChainContext must have a 'user_message' string field."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="Write a spec for authentication",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )
        assert context.user_message == "Write a spec for authentication"
        assert isinstance(context.user_message, str)

    def test_chain_context_has_conversation_history_field(self):
        """ChainContext must have a 'conversation_history' list field."""
        from src.agents.chains.base import ChainContext

        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        context = ChainContext(
            user_message="Follow up",
            conversation_history=history,
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )
        assert context.conversation_history == history
        assert isinstance(context.conversation_history, list)
        assert len(context.conversation_history) == 2

    def test_chain_context_has_memory_context_field(self):
        """ChainContext must have a 'memory_context' list of strings field."""
        from src.agents.chains.base import ChainContext

        memories = [
            "User previously discussed authentication patterns",
            "User prefers JWT over sessions"
        ]
        context = ChainContext(
            user_message="Continue auth work",
            conversation_history=[],
            memory_context=memories,
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )
        assert context.memory_context == memories
        assert isinstance(context.memory_context, list)
        assert len(context.memory_context) == 2

    def test_chain_context_has_agent_outputs_field(self):
        """ChainContext must have an 'agent_outputs' dict field."""
        from src.agents.chains.base import ChainContext

        outputs = {
            "spec-analyst": "Analysis of requirements...",
            "spec-clarifier": "Clarified requirements..."
        }
        context = ChainContext(
            user_message="Write spec",
            conversation_history=[],
            memory_context=[],
            agent_outputs=outputs,
            current_agent="code-planner",
            chain_id="sdd"
        )
        assert context.agent_outputs == outputs
        assert isinstance(context.agent_outputs, dict)
        assert context.agent_outputs["spec-analyst"] == "Analysis of requirements..."

    def test_chain_context_has_current_agent_field(self):
        """ChainContext must have a 'current_agent' string field."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="Write spec",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="spec-analyst",
            chain_id="sdd"
        )
        assert context.current_agent == "spec-analyst"
        assert isinstance(context.current_agent, str)

    def test_chain_context_has_chain_id_field(self):
        """ChainContext must have a 'chain_id' string field."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="Write spec",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )
        assert context.chain_id == "sdd"
        assert isinstance(context.chain_id, str)


class TestChainContextUsage:
    """Test ChainContext usage patterns in chain execution."""

    def test_chain_context_empty_initialization(self):
        """ChainContext can be initialized with empty collections."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="Hello",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="test"
        )
        assert context.user_message == "Hello"
        assert context.conversation_history == []
        assert context.memory_context == []
        assert context.agent_outputs == {}

    def test_chain_context_agent_outputs_mutable(self):
        """ChainContext agent_outputs dict should be mutable for accumulation."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="Test",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="agent-1",
            chain_id="test"
        )

        # Simulate chain execution adding outputs
        context.agent_outputs["agent-1"] = "Output from agent 1"
        context.agent_outputs["agent-2"] = "Output from agent 2"

        assert len(context.agent_outputs) == 2
        assert "agent-1" in context.agent_outputs
        assert "agent-2" in context.agent_outputs

    def test_chain_context_current_agent_updatable(self):
        """ChainContext current_agent should be updatable during chain execution."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="Test",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="agent-1",
            chain_id="test"
        )

        # Update current agent as chain progresses
        assert context.current_agent == "agent-1"
        # Note: dataclasses are mutable by default
        context.current_agent = "agent-2"
        assert context.current_agent == "agent-2"

    def test_chain_context_with_full_conversation_history(self):
        """ChainContext handles multi-turn conversation history."""
        from src.agents.chains.base import ChainContext

        history = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is TDD?"},
            {"role": "assistant", "content": "TDD stands for Test-Driven Development..."},
            {"role": "user", "content": "Show me an example"}
        ]
        context = ChainContext(
            user_message="Show me an example",
            conversation_history=history,
            memory_context=["User learning about TDD"],
            agent_outputs={},
            current_agent="test-architect",
            chain_id="tdd"
        )

        assert len(context.conversation_history) == 4
        assert context.conversation_history[0]["role"] == "system"
        assert context.conversation_history[-1]["content"] == "Show me an example"
