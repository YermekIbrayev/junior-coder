"""
Orchestrator - Intent classification and chain dispatch.

This package provides modular orchestration:
- models.py: Data structures (Intent, IntentClassification, OrchestratorResult)
- constants.py: Configuration values and prompts
- classifier.py: LLM-based intent classification
- runner.py: Main orchestration and chain execution

Usage:
    from src.agents.orchestrator import run_orchestrator, OrchestratorResult
    result = await run_orchestrator(user_message, conversation, execute_chain=True)
"""

from src.agents.orchestrator.models import (
    Intent,
    IntentClassification,
    OrchestratorResult,
)
from src.agents.orchestrator.constants import (
    CONFIDENCE_THRESHOLD,
    CLASSIFICATION_TEMPERATURE,
    CLASSIFICATION_MAX_TOKENS,
    CLASSIFICATION_MODEL,
    CLARIFYING_QUESTION,
    INTENT_DISPLAY_NAMES,
    CLASSIFICATION_PROMPT,
)
from src.agents.orchestrator.classifier import classify_intent
from src.agents.orchestrator.runner import run_orchestrator

__all__ = [
    # Models
    "Intent",
    "IntentClassification",
    "OrchestratorResult",
    # Constants
    "CONFIDENCE_THRESHOLD",
    "CLASSIFICATION_TEMPERATURE",
    "CLASSIFICATION_MAX_TOKENS",
    "CLASSIFICATION_MODEL",
    "CLARIFYING_QUESTION",
    "INTENT_DISPLAY_NAMES",
    "CLASSIFICATION_PROMPT",
    # Functions
    "classify_intent",
    "run_orchestrator",
]
