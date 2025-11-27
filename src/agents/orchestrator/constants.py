"""
Orchestrator Constants - Configuration values and prompts.

Single Responsibility: Centralize configuration for intent classification.
Prompts are loaded from .agents/prompts/classifications/intent.yaml.
"""

from src.agents.prompts.loader import get_prompt_content

# Confidence threshold for intent classification (0.0-1.0)
# Below this threshold, the orchestrator will ask for clarification
CONFIDENCE_THRESHOLD = 0.5

# LLM temperature for classification (low for consistency)
CLASSIFICATION_TEMPERATURE = 0.1

# Max tokens for classification response
CLASSIFICATION_MAX_TOKENS = 256

# Model for classification (qwen is fast and sufficient for intent detection)
CLASSIFICATION_MODEL = "qwen"

# Intent to human-readable name mapping
INTENT_DISPLAY_NAMES = {
    "SDD": "Specification-Driven Development",
    "TDD": "Test-Driven Development",
    "RETRO": "Retrospective Analysis",
    "UNCLEAR": "Unclear Intent",
    "GENERAL": "General Question"
}

# Load prompts from YAML
CLASSIFICATION_PROMPT = get_prompt_content("classifications/intent.yaml", "classification")
CLARIFYING_QUESTION = get_prompt_content("classifications/intent.yaml", "clarifying_question")

__all__ = [
    "CONFIDENCE_THRESHOLD",
    "CLASSIFICATION_TEMPERATURE",
    "CLASSIFICATION_MAX_TOKENS",
    "CLASSIFICATION_MODEL",
    "CLARIFYING_QUESTION",
    "INTENT_DISPLAY_NAMES",
    "CLASSIFICATION_PROMPT",
]
