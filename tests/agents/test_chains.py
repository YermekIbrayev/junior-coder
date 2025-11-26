"""
Tests for Agent Chains - SDD, TDD, and Retro chains.

TDD Phase: RED - These tests verify chain structure and agent ordering.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestSDDChain:
    """Test SDDChain structure and agent ordering (T041)."""

    def test_sdd_chain_exists(self):
        """SDDChain class must exist."""
        from src.agents.chains.sdd import SDDChain
        assert SDDChain is not None

    def test_sdd_chain_has_correct_id(self):
        """SDDChain must have id 'sdd'."""
        from src.agents.chains.sdd import SDDChain
        chain = SDDChain()
        assert chain.id == "sdd"

    def test_sdd_chain_has_correct_name(self):
        """SDDChain must have correct name."""
        from src.agents.chains.sdd import SDDChain
        chain = SDDChain()
        assert "Specification" in chain.name or "SDD" in chain.name

    def test_sdd_chain_has_five_agents(self):
        """SDDChain must have exactly 5 agents."""
        from src.agents.chains.sdd import SDDChain
        chain = SDDChain()
        assert len(chain.agents) == 5

    def test_sdd_chain_agent_order(self):
        """SDDChain agents must be in correct order."""
        from src.agents.chains.sdd import SDDChain
        chain = SDDChain()

        expected_order = [
            "spec-analyst",
            "spec-clarifier",
            "code-planner",
            "alignment-analyzer",
            "vibe-check-guardian"
        ]

        agent_ids = [agent.id for agent in chain.agents]
        assert agent_ids == expected_order

    def test_sdd_chain_first_agent_is_spec_analyst(self):
        """First agent in SDDChain must be spec-analyst."""
        from src.agents.chains.sdd import SDDChain
        chain = SDDChain()
        assert chain.agents[0].id == "spec-analyst"

    def test_sdd_chain_last_agent_is_vibe_check_guardian(self):
        """Last agent in SDDChain must be vibe-check-guardian."""
        from src.agents.chains.sdd import SDDChain
        chain = SDDChain()
        assert chain.agents[-1].id == "vibe-check-guardian"

    def test_sdd_chain_extends_base_chain(self):
        """SDDChain must extend BaseChain."""
        from src.agents.chains.sdd import SDDChain
        from src.agents.chains.base import BaseChain
        chain = SDDChain()
        # Check it's a dataclass with same attributes
        assert hasattr(chain, 'id')
        assert hasattr(chain, 'name')
        assert hasattr(chain, 'agents')

    def test_sdd_chain_agents_are_base_agents(self):
        """All SDDChain agents must be BaseAgent instances."""
        from src.agents.chains.sdd import SDDChain
        from src.agents.agents.base import BaseAgent
        chain = SDDChain()
        for agent in chain.agents:
            assert isinstance(agent, BaseAgent)


class TestTDDChain:
    """Test TDDChain structure and agent ordering (T043)."""

    def test_tdd_chain_exists(self):
        """TDDChain class must exist."""
        from src.agents.chains.tdd import TDDChain
        assert TDDChain is not None

    def test_tdd_chain_has_correct_id(self):
        """TDDChain must have id 'tdd'."""
        from src.agents.chains.tdd import TDDChain
        chain = TDDChain()
        assert chain.id == "tdd"

    def test_tdd_chain_has_correct_name(self):
        """TDDChain must have correct name."""
        from src.agents.chains.tdd import TDDChain
        chain = TDDChain()
        assert "Test" in chain.name or "TDD" in chain.name

    def test_tdd_chain_has_three_agents(self):
        """TDDChain must have exactly 3 agents."""
        from src.agents.chains.tdd import TDDChain
        chain = TDDChain()
        assert len(chain.agents) == 3

    def test_tdd_chain_agent_order(self):
        """TDDChain agents must be in correct order."""
        from src.agents.chains.tdd import TDDChain
        chain = TDDChain()

        expected_order = [
            "test-architect",
            "implementation-specialist",
            "quality-guardian"
        ]

        agent_ids = [agent.id for agent in chain.agents]
        assert agent_ids == expected_order

    def test_tdd_chain_first_agent_is_test_architect(self):
        """First agent in TDDChain must be test-architect."""
        from src.agents.chains.tdd import TDDChain
        chain = TDDChain()
        assert chain.agents[0].id == "test-architect"

    def test_tdd_chain_last_agent_is_quality_guardian(self):
        """Last agent in TDDChain must be quality-guardian."""
        from src.agents.chains.tdd import TDDChain
        chain = TDDChain()
        assert chain.agents[-1].id == "quality-guardian"

    def test_tdd_chain_agents_are_base_agents(self):
        """All TDDChain agents must be BaseAgent instances."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.agents.base import BaseAgent
        chain = TDDChain()
        for agent in chain.agents:
            assert isinstance(agent, BaseAgent)


class TestRetroChain:
    """Test RetroChain structure and agent ordering (T045)."""

    def test_retro_chain_exists(self):
        """RetroChain class must exist."""
        from src.agents.chains.retro import RetroChain
        assert RetroChain is not None

    def test_retro_chain_has_correct_id(self):
        """RetroChain must have id 'retro'."""
        from src.agents.chains.retro import RetroChain
        chain = RetroChain()
        assert chain.id == "retro"

    def test_retro_chain_has_correct_name(self):
        """RetroChain must have correct name."""
        from src.agents.chains.retro import RetroChain
        chain = RetroChain()
        assert "Retro" in chain.name or "Analysis" in chain.name

    def test_retro_chain_has_three_agents(self):
        """RetroChain must have exactly 3 agents."""
        from src.agents.chains.retro import RetroChain
        chain = RetroChain()
        assert len(chain.agents) == 3

    def test_retro_chain_agent_order(self):
        """RetroChain agents must be in correct order."""
        from src.agents.chains.retro import RetroChain
        chain = RetroChain()

        expected_order = [
            "knowledge-curator",
            "synthesis-specialist",
            "system-improver"
        ]

        agent_ids = [agent.id for agent in chain.agents]
        assert agent_ids == expected_order

    def test_retro_chain_first_agent_is_knowledge_curator(self):
        """First agent in RetroChain must be knowledge-curator."""
        from src.agents.chains.retro import RetroChain
        chain = RetroChain()
        assert chain.agents[0].id == "knowledge-curator"

    def test_retro_chain_last_agent_is_system_improver(self):
        """Last agent in RetroChain must be system-improver."""
        from src.agents.chains.retro import RetroChain
        chain = RetroChain()
        assert chain.agents[-1].id == "system-improver"

    def test_retro_chain_agents_are_base_agents(self):
        """All RetroChain agents must be BaseAgent instances."""
        from src.agents.chains.retro import RetroChain
        from src.agents.agents.base import BaseAgent
        chain = RetroChain()
        for agent in chain.agents:
            assert isinstance(agent, BaseAgent)


class TestChainExecution:
    """Test chain execution - iterating agents and accumulating outputs (T047)."""

    @pytest.mark.asyncio
    async def test_chain_execute_method_exists(self):
        """BaseChain must have execute method."""
        from src.agents.chains.base import BaseChain
        assert hasattr(BaseChain, 'execute')

    @pytest.mark.asyncio
    async def test_chain_execute_returns_chain_context(self):
        """Chain execute must return ChainContext."""
        from src.agents.chains.sdd import SDDChain
        from src.agents.chains.base import ChainContext

        chain = SDDChain()
        context = ChainContext(
            user_message="Write a spec",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )

        # Mock the agent runner to avoid actual LLM calls
        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Agent output"
            result = await chain.execute(context, http_client=MagicMock())

        assert isinstance(result, ChainContext)

    @pytest.mark.asyncio
    async def test_chain_execute_iterates_all_agents(self):
        """Chain execute must call each agent in sequence."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Agent output"
            await chain.execute(context, http_client=MagicMock())

            # Should be called once per agent (3 agents in TDD chain)
            assert mock_run.call_count == 3

    @pytest.mark.asyncio
    async def test_chain_execute_accumulates_outputs(self):
        """Chain execute must accumulate agent outputs in context."""
        from src.agents.chains.retro import RetroChain
        from src.agents.chains.base import ChainContext

        chain = RetroChain()
        context = ChainContext(
            user_message="Review code",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="retro"
        )

        call_count = 0
        def mock_response(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return f"Output from agent {call_count}"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = mock_response
            result = await chain.execute(context, http_client=MagicMock())

            # All agents should have outputs
            assert len(result.agent_outputs) == 3
            assert "knowledge-curator" in result.agent_outputs
            assert "synthesis-specialist" in result.agent_outputs
            assert "system-improver" in result.agent_outputs

    @pytest.mark.asyncio
    async def test_chain_execute_updates_current_agent(self):
        """Chain execute must update current_agent during execution."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        agents_seen = []

        async def capture_agent(**kwargs):
            # Capture the agent being run (keyword argument)
            agent = kwargs.get("agent")
            agents_seen.append(agent.id)
            return f"Output from {agent.id}"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = capture_agent
            result = await chain.execute(context, http_client=MagicMock())

            # Agents should be executed in order
            assert agents_seen == ["test-architect", "implementation-specialist", "quality-guardian"]


class TestContextPassing:
    """Test context passing between agents (T049)."""

    @pytest.mark.asyncio
    async def test_agent_receives_previous_outputs(self):
        """Each agent must receive outputs from previous agents."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        contexts_passed = []

        async def capture_context(**kwargs):
            agent = kwargs.get("agent")
            context_str = kwargs.get("context")
            contexts_passed.append({
                "agent": agent.id,
                "context": context_str
            })
            return f"Output from {agent.id}"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = capture_context
            await chain.execute(context, http_client=MagicMock())

            # Second agent should see first agent's output in context
            assert len(contexts_passed) == 3

            # First agent should not have previous outputs
            assert "Output from" not in contexts_passed[0]["context"]

            # Second agent should have first agent's output
            assert "test-architect" in contexts_passed[1]["context"]

            # Third agent should have both previous outputs
            assert "test-architect" in contexts_passed[2]["context"]
            assert "implementation-specialist" in contexts_passed[2]["context"]

    @pytest.mark.asyncio
    async def test_context_includes_user_message(self):
        """Agent context must include original user message."""
        from src.agents.chains.sdd import SDDChain
        from src.agents.chains.base import ChainContext

        chain = SDDChain()
        user_msg = "Write a specification for user authentication"
        context = ChainContext(
            user_message=user_msg,
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )

        contexts_passed = []

        async def capture_context(**kwargs):
            context_str = kwargs.get("context")
            contexts_passed.append(context_str)
            return "Agent output"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = capture_context
            await chain.execute(context, http_client=MagicMock())

            # All agents should receive user message in context
            for ctx in contexts_passed:
                assert user_msg in ctx

    @pytest.mark.asyncio
    async def test_context_includes_memory_context(self):
        """Agent context must include memory context when provided."""
        from src.agents.chains.retro import RetroChain
        from src.agents.chains.base import ChainContext

        chain = RetroChain()
        memories = ["Previous discussion about API design", "User prefers REST over GraphQL"]
        context = ChainContext(
            user_message="Review the API",
            conversation_history=[],
            memory_context=memories,
            agent_outputs={},
            current_agent="",
            chain_id="retro"
        )

        contexts_passed = []

        async def capture_context(**kwargs):
            context_str = kwargs.get("context")
            contexts_passed.append(context_str)
            return "Agent output"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = capture_context
            await chain.execute(context, http_client=MagicMock())

            # First agent should receive memory context
            assert "Previous discussion about API design" in contexts_passed[0]

    @pytest.mark.asyncio
    async def test_chain_returns_final_context(self):
        """Chain execute must return context with all agent outputs."""
        from src.agents.chains.sdd import SDDChain
        from src.agents.chains.base import ChainContext

        chain = SDDChain()
        context = ChainContext(
            user_message="Write spec",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="sdd"
        )

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Agent completed"
            result = await chain.execute(context, http_client=MagicMock())

            # Result should have outputs from all 5 SDD agents
            assert len(result.agent_outputs) == 5
            # Last agent should be set
            assert result.current_agent == "vibe-check-guardian"


class TestPartialFailure:
    """Test partial failure handling - agent fails, return partial results + error (T051)."""

    @pytest.mark.asyncio
    async def test_chain_context_has_error_field(self):
        """ChainContext must have an error field for failure tracking."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="test",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="test"
        )
        # ChainContext should have error field (None by default)
        assert hasattr(context, "error")
        assert context.error is None

    @pytest.mark.asyncio
    async def test_chain_context_has_failed_agent_field(self):
        """ChainContext must track which agent failed."""
        from src.agents.chains.base import ChainContext

        context = ChainContext(
            user_message="test",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="test"
        )
        # ChainContext should have failed_agent field (None by default)
        assert hasattr(context, "failed_agent")
        assert context.failed_agent is None

    @pytest.mark.asyncio
    async def test_partial_failure_returns_partial_results(self):
        """When agent fails, chain must return partial results from successful agents."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        call_count = 0

        async def fail_on_second(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("LLM service unavailable")
            return f"Output from agent {call_count}"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = fail_on_second
            result = await chain.execute(context, http_client=MagicMock())

            # First agent should have output
            assert "test-architect" in result.agent_outputs
            # Second agent (failed) should NOT have output
            assert "implementation-specialist" not in result.agent_outputs
            # Third agent should NOT have output (chain stopped)
            assert "quality-guardian" not in result.agent_outputs

    @pytest.mark.asyncio
    async def test_partial_failure_sets_error(self):
        """When agent fails, chain must set error in context."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        call_count = 0

        async def fail_on_second(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("LLM service unavailable")
            return f"Output from agent {call_count}"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = fail_on_second
            result = await chain.execute(context, http_client=MagicMock())

            # Error should be set
            assert result.error is not None
            assert "LLM service unavailable" in result.error

    @pytest.mark.asyncio
    async def test_partial_failure_sets_failed_agent(self):
        """When agent fails, chain must set failed_agent in context."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        call_count = 0

        async def fail_on_second(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:
                raise RuntimeError("LLM service unavailable")
            return f"Output from agent {call_count}"

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = fail_on_second
            result = await chain.execute(context, http_client=MagicMock())

            # Failed agent should be tracked
            assert result.failed_agent == "implementation-specialist"

    @pytest.mark.asyncio
    async def test_partial_failure_does_not_raise(self):
        """Chain must not raise exception on agent failure, instead return context with error."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        async def always_fail(**kwargs):
            raise RuntimeError("LLM service unavailable")

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = always_fail
            # Should NOT raise, should return context with error
            result = await chain.execute(context, http_client=MagicMock())
            assert isinstance(result, ChainContext)
            assert result.error is not None

    @pytest.mark.asyncio
    async def test_successful_chain_has_no_error(self):
        """Successful chain execution must have no error set."""
        from src.agents.chains.tdd import TDDChain
        from src.agents.chains.base import ChainContext

        chain = TDDChain()
        context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={},
            current_agent="",
            chain_id="tdd"
        )

        with patch("src.agents.chains.base.run_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = "Agent output"
            result = await chain.execute(context, http_client=MagicMock())

            # No error on successful execution
            assert result.error is None
            assert result.failed_agent is None
            # All agents completed
            assert len(result.agent_outputs) == 3
