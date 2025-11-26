"""
Tests for Orchestrator module - IntentClassification.

TDD Phase: RED - These tests should FAIL until IntentClassification is implemented.
"""

import pytest
from enum import Enum


class TestIntentEnum:
    """Test Intent enum has required values."""

    def test_intent_enum_exists(self):
        """Intent enum must exist."""
        from src.agents.orchestrator import Intent

        assert Intent is not None

    def test_intent_has_sdd_value(self):
        """Intent enum must have SDD value."""
        from src.agents.orchestrator import Intent

        assert hasattr(Intent, "SDD")
        assert Intent.SDD.value == "sdd"

    def test_intent_has_tdd_value(self):
        """Intent enum must have TDD value."""
        from src.agents.orchestrator import Intent

        assert hasattr(Intent, "TDD")
        assert Intent.TDD.value == "tdd"

    def test_intent_has_retro_value(self):
        """Intent enum must have RETRO value."""
        from src.agents.orchestrator import Intent

        assert hasattr(Intent, "RETRO")
        assert Intent.RETRO.value == "retro"

    def test_intent_has_unclear_value(self):
        """Intent enum must have UNCLEAR value."""
        from src.agents.orchestrator import Intent

        assert hasattr(Intent, "UNCLEAR")
        assert Intent.UNCLEAR.value == "unclear"

    def test_intent_is_enum(self):
        """Intent must be an Enum type."""
        from src.agents.orchestrator import Intent

        assert issubclass(Intent, Enum)


class TestIntentClassificationFields:
    """Test IntentClassification has required fields."""

    def test_intent_classification_has_intent_field(self):
        """IntentClassification must have an 'intent' field of Intent type."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.SDD,
            confidence=0.95,
            reasoning="User wants to write a specification"
        )
        assert classification.intent == Intent.SDD
        assert isinstance(classification.intent, Intent)

    def test_intent_classification_has_confidence_field(self):
        """IntentClassification must have a 'confidence' float field."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.TDD,
            confidence=0.87,
            reasoning="User wants to write tests"
        )
        assert classification.confidence == 0.87
        assert isinstance(classification.confidence, float)

    def test_intent_classification_has_reasoning_field(self):
        """IntentClassification must have a 'reasoning' string field."""
        from src.agents.orchestrator import IntentClassification, Intent

        reasoning_text = "User mentioned 'write tests' and 'TDD approach'"
        classification = IntentClassification(
            intent=Intent.TDD,
            confidence=0.92,
            reasoning=reasoning_text
        )
        assert classification.reasoning == reasoning_text
        assert isinstance(classification.reasoning, str)


class TestIntentClassificationValues:
    """Test IntentClassification value constraints."""

    def test_confidence_accepts_zero(self):
        """Confidence should accept 0.0 value."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.UNCLEAR,
            confidence=0.0,
            reasoning="Cannot determine intent"
        )
        assert classification.confidence == 0.0

    def test_confidence_accepts_one(self):
        """Confidence should accept 1.0 value."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.SDD,
            confidence=1.0,
            reasoning="Absolutely certain this is SDD"
        )
        assert classification.confidence == 1.0

    def test_confidence_accepts_mid_range(self):
        """Confidence should accept mid-range values."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.RETRO,
            confidence=0.65,
            reasoning="Likely a retrospective request"
        )
        assert classification.confidence == 0.65

    def test_empty_reasoning_allowed(self):
        """Empty reasoning string should be allowed."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.SDD,
            confidence=0.9,
            reasoning=""
        )
        assert classification.reasoning == ""


class TestIntentClassificationUsage:
    """Test IntentClassification usage patterns."""

    def test_classification_for_spec_request(self):
        """Classification for specification request should use SDD."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.SDD,
            confidence=0.95,
            reasoning="User asked to 'write a spec' - clear SDD indicator"
        )
        assert classification.intent == Intent.SDD
        assert classification.confidence > 0.9

    def test_classification_for_test_request(self):
        """Classification for test request should use TDD."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.TDD,
            confidence=0.88,
            reasoning="User asked to 'write tests' - TDD workflow"
        )
        assert classification.intent == Intent.TDD

    def test_classification_for_retro_request(self):
        """Classification for retrospective request should use RETRO."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.RETRO,
            confidence=0.82,
            reasoning="User asking for review and improvements"
        )
        assert classification.intent == Intent.RETRO

    def test_classification_for_unclear_request(self):
        """Classification for ambiguous request should use UNCLEAR."""
        from src.agents.orchestrator import IntentClassification, Intent

        classification = IntentClassification(
            intent=Intent.UNCLEAR,
            confidence=0.3,
            reasoning="Request is ambiguous, needs clarification"
        )
        assert classification.intent == Intent.UNCLEAR
        assert classification.confidence < 0.5


class TestClassifyIntent:
    """Test classify_intent function for LLM-based intent classification."""

    @pytest.mark.asyncio
    async def test_classify_intent_exists(self):
        """classify_intent function must exist."""
        from src.agents.orchestrator import classify_intent

        assert callable(classify_intent)

    @pytest.mark.asyncio
    async def test_classify_intent_returns_intent_classification(self, mock_httpx_client):
        """classify_intent must return an IntentClassification object."""
        from src.agents.orchestrator import classify_intent, IntentClassification
        from unittest.mock import patch, MagicMock

        # Mock LLM response with JSON classification
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "User wants to write a spec"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Write a spec for user auth", mock_httpx_client)

        assert isinstance(result, IntentClassification)

    @pytest.mark.asyncio
    async def test_classify_intent_returns_sdd_for_spec_request(self, mock_httpx_client):
        """classify_intent should return SDD for specification requests."""
        from src.agents.orchestrator import classify_intent, Intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "User wants to write a specification"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Write a spec for user authentication", mock_httpx_client)

        assert result.intent == Intent.SDD

    @pytest.mark.asyncio
    async def test_classify_intent_returns_tdd_for_test_request(self, mock_httpx_client):
        """classify_intent should return TDD for test writing requests."""
        from src.agents.orchestrator import classify_intent, Intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.92, "reasoning": "User wants to write tests"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Write tests for the login function", mock_httpx_client)

        assert result.intent == Intent.TDD

    @pytest.mark.asyncio
    async def test_classify_intent_returns_retro_for_review_request(self, mock_httpx_client):
        """classify_intent should return RETRO for retrospective requests."""
        from src.agents.orchestrator import classify_intent, Intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "retro", "confidence": 0.88, "reasoning": "User wants retrospective analysis"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Review and improve the codebase", mock_httpx_client)

        assert result.intent == Intent.RETRO

    @pytest.mark.asyncio
    async def test_classify_intent_returns_unclear_for_ambiguous_request(self, mock_httpx_client):
        """classify_intent should return UNCLEAR for ambiguous requests."""
        from src.agents.orchestrator import classify_intent, Intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "unclear", "confidence": 0.35, "reasoning": "Request is ambiguous"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Help me", mock_httpx_client)

        assert result.intent == Intent.UNCLEAR

    @pytest.mark.asyncio
    async def test_classify_intent_includes_confidence(self, mock_httpx_client):
        """classify_intent must include confidence score."""
        from src.agents.orchestrator import classify_intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.87, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Create a specification", mock_httpx_client)

        assert result.confidence == 0.87
        assert 0.0 <= result.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_classify_intent_includes_reasoning(self, mock_httpx_client):
        """classify_intent must include reasoning explanation."""
        from src.agents.orchestrator import classify_intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.9, "reasoning": "User explicitly mentioned test-driven development"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Use TDD approach for this feature", mock_httpx_client)

        assert "test" in result.reasoning.lower() or len(result.reasoning) > 0

    @pytest.mark.asyncio
    async def test_classify_intent_calls_llm(self, mock_httpx_client):
        """classify_intent must call the LLM service."""
        from src.agents.orchestrator import classify_intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.9, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        await classify_intent("Write a spec", mock_httpx_client)

        mock_httpx_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_classify_intent_handles_invalid_json(self, mock_httpx_client):
        """classify_intent should handle invalid JSON from LLM gracefully."""
        from src.agents.orchestrator import classify_intent, Intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "This is not valid JSON"
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await classify_intent("Some request", mock_httpx_client)

        # Should default to UNCLEAR on parse error
        assert result.intent == Intent.UNCLEAR


class TestRunOrchestrator:
    """Test run_orchestrator function for intent classification and chain dispatch."""

    @pytest.mark.asyncio
    async def test_run_orchestrator_exists(self):
        """run_orchestrator function must exist."""
        from src.agents.orchestrator import run_orchestrator

        assert callable(run_orchestrator)

    @pytest.mark.asyncio
    async def test_run_orchestrator_returns_orchestrator_result(self, mock_httpx_client):
        """run_orchestrator must return an OrchestratorResult object."""
        from src.agents.orchestrator import run_orchestrator, OrchestratorResult
        from unittest.mock import MagicMock, patch

        # Mock classification response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Write a spec for authentication",
            conversation=[{"role": "user", "content": "Write a spec for authentication"}],
            http_client=mock_httpx_client
        )

        assert isinstance(result, OrchestratorResult)

    @pytest.mark.asyncio
    async def test_run_orchestrator_classifies_intent(self, mock_httpx_client):
        """run_orchestrator must classify user intent."""
        from src.agents.orchestrator import run_orchestrator, Intent
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Write a spec for user auth",
            conversation=[{"role": "user", "content": "Write a spec for user auth"}],
            http_client=mock_httpx_client
        )

        assert result.classification.intent == Intent.SDD

    @pytest.mark.asyncio
    async def test_run_orchestrator_returns_chain_id_for_sdd(self, mock_httpx_client):
        """run_orchestrator must return 'sdd' chain_id for SDD intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Write a specification",
            conversation=[{"role": "user", "content": "Write a specification"}],
            http_client=mock_httpx_client
        )

        assert result.chain_id == "sdd"

    @pytest.mark.asyncio
    async def test_run_orchestrator_returns_chain_id_for_tdd(self, mock_httpx_client):
        """run_orchestrator must return 'tdd' chain_id for TDD intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.92, "reasoning": "Test request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Write tests for login",
            conversation=[{"role": "user", "content": "Write tests for login"}],
            http_client=mock_httpx_client
        )

        assert result.chain_id == "tdd"

    @pytest.mark.asyncio
    async def test_run_orchestrator_returns_chain_id_for_retro(self, mock_httpx_client):
        """run_orchestrator must return 'retro' chain_id for RETRO intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "retro", "confidence": 0.88, "reasoning": "Review request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Review the codebase",
            conversation=[{"role": "user", "content": "Review the codebase"}],
            http_client=mock_httpx_client
        )

        assert result.chain_id == "retro"

    @pytest.mark.asyncio
    async def test_run_orchestrator_includes_response_text(self, mock_httpx_client):
        """run_orchestrator must include response text."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Write a spec",
            conversation=[{"role": "user", "content": "Write a spec"}],
            http_client=mock_httpx_client
        )

        assert result.response is not None
        assert isinstance(result.response, str)


class TestUnclearHandling:
    """Test UNCLEAR intent handling with clarifying questions."""

    @pytest.mark.asyncio
    async def test_unclear_returns_clarifying_question(self, mock_httpx_client):
        """UNCLEAR intent should return a clarifying question."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "unclear", "confidence": 0.3, "reasoning": "Ambiguous request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Help me",
            conversation=[{"role": "user", "content": "Help me"}],
            http_client=mock_httpx_client
        )

        assert result.chain_id is None
        assert result.needs_clarification is True

    @pytest.mark.asyncio
    async def test_unclear_includes_clarifying_message(self, mock_httpx_client):
        """UNCLEAR intent should include a clarifying message in response."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "unclear", "confidence": 0.25, "reasoning": "Too vague"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Do something",
            conversation=[{"role": "user", "content": "Do something"}],
            http_client=mock_httpx_client
        )

        assert result.response is not None
        # Response should ask for clarification
        assert len(result.response) > 0

    @pytest.mark.asyncio
    async def test_low_confidence_triggers_clarification(self, mock_httpx_client):
        """Low confidence (below threshold) should trigger clarification."""
        from src.agents.orchestrator import run_orchestrator, CONFIDENCE_THRESHOLD
        from unittest.mock import MagicMock

        # Even with a valid intent, low confidence should trigger clarification
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.4, "reasoning": "Maybe spec?"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Something about features",
            conversation=[{"role": "user", "content": "Something about features"}],
            http_client=mock_httpx_client
        )

        # Low confidence should trigger clarification regardless of intent
        assert result.needs_clarification is True

    @pytest.mark.asyncio
    async def test_high_confidence_no_clarification(self, mock_httpx_client):
        """High confidence should not trigger clarification."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.95, "reasoning": "Clear test request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        result = await run_orchestrator(
            user_message="Write unit tests for the login function",
            conversation=[{"role": "user", "content": "Write unit tests for the login function"}],
            http_client=mock_httpx_client
        )

        assert result.needs_clarification is False
        assert result.chain_id == "tdd"


class TestChainDispatch:
    """Test orchestrator chain dispatch - executing the appropriate chain (T053)."""

    @pytest.mark.asyncio
    async def test_orchestrator_result_has_chain_output_field(self):
        """OrchestratorResult must have chain_output field for chain execution results."""
        from src.agents.orchestrator import OrchestratorResult, IntentClassification, Intent

        result = OrchestratorResult(
            classification=IntentClassification(
                intent=Intent.SDD,
                confidence=0.95,
                reasoning="Spec request"
            ),
            chain_id="sdd",
            response="Routing to SDD"
        )
        # Should have chain_output field (None by default when no chain executed)
        assert hasattr(result, "chain_output")

    @pytest.mark.asyncio
    async def test_run_orchestrator_with_execute_chain_dispatches_sdd(self, mock_httpx_client):
        """run_orchestrator with execute_chain=True should execute SDDChain for SDD intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock, patch, AsyncMock

        # Mock classification response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Mock chain execution - patch in the chains module where it's defined
        with patch("src.agents.chains.sdd.SDDChain") as mock_chain_class:
            mock_chain = MagicMock()
            mock_chain.execute = AsyncMock(return_value=MagicMock(
                agent_outputs={"spec-analyst": "Output"},
                error=None
            ))
            mock_chain_class.return_value = mock_chain

            result = await run_orchestrator(
                user_message="Write a spec for authentication",
                conversation=[{"role": "user", "content": "Write a spec for authentication"}],
                http_client=mock_httpx_client,
                execute_chain=True
            )

            # Chain should have been executed
            mock_chain.execute.assert_called_once()
            assert result.chain_output is not None

    @pytest.mark.asyncio
    async def test_run_orchestrator_with_execute_chain_dispatches_tdd(self, mock_httpx_client):
        """run_orchestrator with execute_chain=True should execute TDDChain for TDD intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock, patch, AsyncMock

        # Mock classification response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.92, "reasoning": "Test request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Mock chain execution - patch in the chains module where it's defined
        with patch("src.agents.chains.tdd.TDDChain") as mock_chain_class:
            mock_chain = MagicMock()
            mock_chain.execute = AsyncMock(return_value=MagicMock(
                agent_outputs={"test-architect": "Output"},
                error=None
            ))
            mock_chain_class.return_value = mock_chain

            result = await run_orchestrator(
                user_message="Write tests for login",
                conversation=[{"role": "user", "content": "Write tests for login"}],
                http_client=mock_httpx_client,
                execute_chain=True
            )

            # Chain should have been executed
            mock_chain.execute.assert_called_once()
            assert result.chain_id == "tdd"

    @pytest.mark.asyncio
    async def test_run_orchestrator_with_execute_chain_dispatches_retro(self, mock_httpx_client):
        """run_orchestrator with execute_chain=True should execute RetroChain for RETRO intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock, patch, AsyncMock

        # Mock classification response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "retro", "confidence": 0.88, "reasoning": "Review request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Mock chain execution - patch in the chains module where it's defined
        with patch("src.agents.chains.retro.RetroChain") as mock_chain_class:
            mock_chain = MagicMock()
            mock_chain.execute = AsyncMock(return_value=MagicMock(
                agent_outputs={"knowledge-curator": "Output"},
                error=None
            ))
            mock_chain_class.return_value = mock_chain

            result = await run_orchestrator(
                user_message="Review the codebase",
                conversation=[{"role": "user", "content": "Review the codebase"}],
                http_client=mock_httpx_client,
                execute_chain=True
            )

            # Chain should have been executed
            mock_chain.execute.assert_called_once()
            assert result.chain_id == "retro"

    @pytest.mark.asyncio
    async def test_run_orchestrator_without_execute_chain_does_not_run_chain(self, mock_httpx_client):
        """run_orchestrator without execute_chain should not execute any chain."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock, patch, AsyncMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "sdd", "confidence": 0.95, "reasoning": "Spec request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Mock chain to verify it's NOT called - patch in chains module
        with patch("src.agents.chains.sdd.SDDChain") as mock_chain_class:
            mock_chain = MagicMock()
            mock_chain.execute = AsyncMock()
            mock_chain_class.return_value = mock_chain

            result = await run_orchestrator(
                user_message="Write a spec",
                conversation=[{"role": "user", "content": "Write a spec"}],
                http_client=mock_httpx_client,
                execute_chain=False  # Default
            )

            # Chain should NOT have been executed
            mock_chain.execute.assert_not_called()
            assert result.chain_output is None

    @pytest.mark.asyncio
    async def test_run_orchestrator_unclear_intent_does_not_execute_chain(self, mock_httpx_client):
        """run_orchestrator should not execute chain for UNCLEAR intent."""
        from src.agents.orchestrator import run_orchestrator
        from unittest.mock import MagicMock, patch, AsyncMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "unclear", "confidence": 0.3, "reasoning": "Ambiguous"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Patch in chains modules
        with patch("src.agents.chains.sdd.SDDChain") as mock_sdd:
            with patch("src.agents.chains.tdd.TDDChain") as mock_tdd:
                with patch("src.agents.chains.retro.RetroChain") as mock_retro:
                    mock_sdd.return_value.execute = AsyncMock()
                    mock_tdd.return_value.execute = AsyncMock()
                    mock_retro.return_value.execute = AsyncMock()

                    result = await run_orchestrator(
                        user_message="Help me",
                        conversation=[{"role": "user", "content": "Help me"}],
                        http_client=mock_httpx_client,
                        execute_chain=True
                    )

                    # No chain should have been executed
                    mock_sdd.return_value.execute.assert_not_called()
                    mock_tdd.return_value.execute.assert_not_called()
                    mock_retro.return_value.execute.assert_not_called()
                    assert result.needs_clarification is True

    @pytest.mark.asyncio
    async def test_chain_output_contains_agent_outputs(self, mock_httpx_client):
        """chain_output should contain agent_outputs from chain execution."""
        from src.agents.orchestrator import run_orchestrator
        from src.agents.chains.base import ChainContext
        from unittest.mock import MagicMock, patch, AsyncMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.95, "reasoning": "Test request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Create mock chain context with agent outputs
        mock_chain_context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={
                "test-architect": "Test plan output",
                "implementation-specialist": "Implementation output",
                "quality-guardian": "Quality review output"
            },
            current_agent="quality-guardian",
            chain_id="tdd"
        )

        # Patch in chains module
        with patch("src.agents.chains.tdd.TDDChain") as mock_chain_class:
            mock_chain = MagicMock()
            mock_chain.execute = AsyncMock(return_value=mock_chain_context)
            mock_chain_class.return_value = mock_chain

            result = await run_orchestrator(
                user_message="Write tests for login",
                conversation=[{"role": "user", "content": "Write tests for login"}],
                http_client=mock_httpx_client,
                execute_chain=True
            )

            # chain_output should contain the agent outputs
            assert result.chain_output is not None
            assert "test-architect" in result.chain_output.agent_outputs
            assert "implementation-specialist" in result.chain_output.agent_outputs
            assert "quality-guardian" in result.chain_output.agent_outputs

    @pytest.mark.asyncio
    async def test_chain_execution_handles_partial_failure(self, mock_httpx_client):
        """Chain execution should handle partial failure gracefully."""
        from src.agents.orchestrator import run_orchestrator
        from src.agents.chains.base import ChainContext
        from unittest.mock import MagicMock, patch, AsyncMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"intent": "tdd", "confidence": 0.95, "reasoning": "Test request"}'
                }
            }]
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx_client.post.return_value = mock_response

        # Create mock chain context with partial failure
        mock_chain_context = ChainContext(
            user_message="Write tests",
            conversation_history=[],
            memory_context=[],
            agent_outputs={
                "test-architect": "Test plan output"
            },
            current_agent="implementation-specialist",
            chain_id="tdd",
            error="LLM service unavailable",
            failed_agent="implementation-specialist"
        )

        # Patch in chains module
        with patch("src.agents.chains.tdd.TDDChain") as mock_chain_class:
            mock_chain = MagicMock()
            mock_chain.execute = AsyncMock(return_value=mock_chain_context)
            mock_chain_class.return_value = mock_chain

            result = await run_orchestrator(
                user_message="Write tests for login",
                conversation=[{"role": "user", "content": "Write tests for login"}],
                http_client=mock_httpx_client,
                execute_chain=True
            )

            # Should return partial results with error
            assert result.chain_output is not None
            assert result.chain_output.error is not None
            assert "test-architect" in result.chain_output.agent_outputs
