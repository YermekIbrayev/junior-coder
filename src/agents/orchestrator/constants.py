"""
Orchestrator Constants - Configuration values and prompts.

Single Responsibility: Centralize configuration for intent classification.
"""

# Confidence threshold for intent classification (0.0-1.0)
# Below this threshold, the orchestrator will ask for clarification
CONFIDENCE_THRESHOLD = 0.5

# LLM temperature for classification (low for consistency)
CLASSIFICATION_TEMPERATURE = 0.1

# Max tokens for classification response
CLASSIFICATION_MAX_TOKENS = 256

# Model for classification (qwen is fast and sufficient for intent detection)
CLASSIFICATION_MODEL = "qwen"

# Clarifying question for unclear intents
CLARIFYING_QUESTION = """I'd like to help, but I'm not sure what you're looking for. Could you please clarify?

Are you trying to:
- **Write a specification** (design documents, requirements, feature planning)
- **Write tests** (unit tests, integration tests, TDD approach)
- **Review and improve code** (code review, refactoring, retrospective analysis)

Please provide more details about what you'd like to accomplish."""

# Intent to human-readable name mapping
INTENT_DISPLAY_NAMES = {
    "SDD": "Specification-Driven Development",
    "TDD": "Test-Driven Development",
    "RETRO": "Retrospective Analysis",
    "UNCLEAR": "Unclear Intent"
}

# Classification prompt for intent detection
CLASSIFICATION_PROMPT = """You are an intent classifier for a software development assistant.

Analyze the user's message and classify their intent into one of these categories:
- "sdd" (Specification-Driven Development): User wants to write specifications, design documents, requirements, or plan features
- "tdd" (Test-Driven Development): User wants to write tests, test code, or follow TDD practices
- "retro" (Retrospective): User wants to review, analyze, improve existing code, or do retrospective analysis
- "unclear": The request is ambiguous or doesn't clearly fit any category

Respond with ONLY a JSON object in this exact format:
{"intent": "<sdd|tdd|retro|unclear>", "confidence": <0.0-1.0>, "reasoning": "<brief explanation>"}

Examples:
- "Write a spec for user authentication" -> {"intent": "sdd", "confidence": 0.95, "reasoning": "User explicitly wants to write a specification"}
- "Add tests for the login function" -> {"intent": "tdd", "confidence": 0.92, "reasoning": "User wants to write tests"}
- "Review and refactor the API code" -> {"intent": "retro", "confidence": 0.88, "reasoning": "User wants to review and improve existing code"}
- "Help me" -> {"intent": "unclear", "confidence": 0.3, "reasoning": "Request is too vague to determine intent"}
"""

__all__ = [
    "CONFIDENCE_THRESHOLD",
    "CLASSIFICATION_TEMPERATURE",
    "CLASSIFICATION_MAX_TOKENS",
    "CLASSIFICATION_MODEL",
    "CLARIFYING_QUESTION",
    "INTENT_DISPLAY_NAMES",
    "CLASSIFICATION_PROMPT",
]
