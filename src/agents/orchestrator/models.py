"""
Orchestrator Models - Data structures for intent classification.

Single Responsibility: Define types for orchestrator workflow.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.agents.chains.base import ChainContext


class Intent(Enum):
    """
    Classification of user intent for workflow routing.

    Values:
        SDD: Specification-Driven Development workflow
        TDD: Test-Driven Development workflow
        RETRO: Retrospective analysis workflow
        UNCLEAR: Ambiguous request requiring clarification
    """

    SDD = "sdd"
    TDD = "tdd"
    RETRO = "retro"
    UNCLEAR = "unclear"


@dataclass
class IntentClassification:
    """
    Result of analyzing a user request for intent classification.

    Attributes:
        intent: The classified intent (SDD, TDD, RETRO, or UNCLEAR)
        confidence: Confidence score from 0.0 to 1.0
        reasoning: Explanation of why this classification was chosen
    """

    intent: Intent
    confidence: float
    reasoning: str


@dataclass
class OrchestratorResult:
    """
    Result from the orchestrator's intent classification and routing.

    Attributes:
        classification: The intent classification result
        chain_id: The chain to execute (sdd, tdd, retro) or None if unclear
        response: Response text (routing message or clarifying question)
        needs_clarification: Whether the user needs to clarify their intent
        chain_output: Output from chain execution (None if chain not executed)
    """

    classification: IntentClassification
    chain_id: str | None
    response: str
    needs_clarification: bool = False
    chain_output: "ChainContext | None" = None


__all__ = ["Intent", "IntentClassification", "OrchestratorResult"]
