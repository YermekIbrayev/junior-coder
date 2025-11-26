"""
Orchestrator - Intent classification and chain dispatch.

Analyzes user requests to determine the appropriate workflow chain.
"""

from dataclasses import dataclass
from enum import Enum
import time

from src.agents.logging_config import get_logger, LogEvent

# Module logger with structured logging
logger = get_logger("orchestrator")


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
    chain_output: "ChainContext | None" = None  # Forward reference to avoid circular import


# ============================================================================
# CONSTANTS
# ============================================================================

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
- "Write a spec for user authentication" → {"intent": "sdd", "confidence": 0.95, "reasoning": "User explicitly wants to write a specification"}
- "Add tests for the login function" → {"intent": "tdd", "confidence": 0.92, "reasoning": "User wants to write tests"}
- "Review and refactor the API code" → {"intent": "retro", "confidence": 0.88, "reasoning": "User wants to review and improve existing code"}
- "Help me" → {"intent": "unclear", "confidence": 0.3, "reasoning": "Request is too vague to determine intent"}
"""


async def classify_intent(user_message: str, http_client) -> IntentClassification:
    """
    Classify the user's intent using the LLM.

    Args:
        user_message: The user's input message to classify
        http_client: Async HTTP client for LLM calls

    Returns:
        IntentClassification with intent, confidence, and reasoning
    """
    import json
    from src.agents.agents.runner import LLM_BASE_URL, LLM_TIMEOUT

    url = f"{LLM_BASE_URL}/v1/chat/completions"

    payload = {
        "model": CLASSIFICATION_MODEL,
        "messages": [
            {"role": "system", "content": CLASSIFICATION_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": CLASSIFICATION_TEMPERATURE,
        "max_tokens": CLASSIFICATION_MAX_TOKENS
    }

    start_time = time.time()
    logger.info(
        LogEvent.INTENT_CLASSIFYING,
        extra={
            "message_preview": user_message[:100] + "..." if len(user_message) > 100 else user_message,
            "message_length": len(user_message),
            "model": CLASSIFICATION_MODEL
        }
    )

    try:
        response = await http_client.post(url, json=payload, timeout=LLM_TIMEOUT)
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Parse JSON response from LLM
        classification_data = json.loads(content)

        intent_str = classification_data.get("intent", "unclear").lower()
        confidence = float(classification_data.get("confidence", 0.5))
        reasoning = classification_data.get("reasoning", "")

        # Map string to Intent enum
        intent_map = {
            "sdd": Intent.SDD,
            "tdd": Intent.TDD,
            "retro": Intent.RETRO,
            "unclear": Intent.UNCLEAR
        }
        intent = intent_map.get(intent_str, Intent.UNCLEAR)

        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            LogEvent.INTENT_CLASSIFIED,
            extra={
                "intent": intent.value,
                "intent_name": intent.name,
                "confidence": round(confidence, 3),
                "reasoning": reasoning,
                "duration_ms": round(duration_ms, 2)
            }
        )

        return IntentClassification(
            intent=intent,
            confidence=confidence,
            reasoning=reasoning
        )

    except json.JSONDecodeError as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.warning(
            LogEvent.INTENT_UNCLEAR,
            extra={
                "error": str(e),
                "error_type": "JSONDecodeError",
                "duration_ms": round(duration_ms, 2)
            }
        )
        return IntentClassification(
            intent=Intent.UNCLEAR,
            confidence=0.0,
            reasoning="Failed to parse LLM response"
        )
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            LogEvent.INTENT_UNCLEAR,
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "duration_ms": round(duration_ms, 2)
            },
            exc_info=True
        )
        return IntentClassification(
            intent=Intent.UNCLEAR,
            confidence=0.0,
            reasoning=f"Classification error: {str(e)}"
        )


async def run_orchestrator(
    user_message: str,
    conversation: list[dict[str, str]],
    user_id: str = "default",
    requested_agent: str | None = None,
    http_client=None,
    execute_chain: bool = False
) -> OrchestratorResult:
    """
    Run the orchestrator to classify intent and route to appropriate chain.

    Classifies the user's intent and determines which workflow chain to execute.
    If the intent is unclear or confidence is low, asks a clarifying question.
    If execute_chain=True, also executes the appropriate chain.

    Args:
        user_message: The user's input message
        conversation: Full conversation history
        user_id: User ID for memory isolation
        requested_agent: Specific agent to use (bypasses orchestrator)
        http_client: Optional HTTP client for LLM calls (for testing)
        execute_chain: Whether to execute the chain after classification

    Returns:
        OrchestratorResult with classification, chain_id, response, and chain_output
    """
    import httpx

    # Use provided client or create one
    if http_client is None:
        async with httpx.AsyncClient(timeout=120.0) as client:
            return await _run_orchestrator_internal(
                user_message=user_message,
                conversation=conversation,
                user_id=user_id,
                requested_agent=requested_agent,
                http_client=client,
                execute_chain=execute_chain
            )
    else:
        return await _run_orchestrator_internal(
            user_message=user_message,
            conversation=conversation,
            user_id=user_id,
            requested_agent=requested_agent,
            http_client=http_client,
            execute_chain=execute_chain
        )


async def _run_orchestrator_internal(
    user_message: str,
    conversation: list[dict[str, str]],
    user_id: str,
    requested_agent: str | None,
    http_client,
    execute_chain: bool = False
) -> OrchestratorResult:
    """Internal implementation of run_orchestrator with injected HTTP client."""
    logger.debug(f"Orchestrator processing request for user: {user_id}")

    # Classify the user's intent
    classification = await classify_intent(user_message, http_client)

    # Check if clarification is needed
    needs_clarification = (
        classification.intent == Intent.UNCLEAR or
        classification.confidence < CONFIDENCE_THRESHOLD
    )

    if needs_clarification:
        logger.info(
            f"Clarification needed for user {user_id}: "
            f"intent={classification.intent.name}, confidence={classification.confidence:.0%}"
        )
        return OrchestratorResult(
            classification=classification,
            chain_id=None,
            response=CLARIFYING_QUESTION,
            needs_clarification=True,
            chain_output=None
        )

    # Map intent to chain ID
    chain_id = classification.intent.value  # "sdd", "tdd", or "retro"

    # Generate routing response using the display names constant
    intent_name = INTENT_DISPLAY_NAMES.get(
        classification.intent.name,
        "Unknown"
    )

    response = f"Routing to {intent_name} workflow (confidence: {classification.confidence:.0%})"

    logger.info(f"Routing user {user_id} to chain: {chain_id}")

    # Execute chain if requested
    chain_output = None
    if execute_chain:
        chain_output = await _execute_chain(
            chain_id=chain_id,
            user_message=user_message,
            conversation=conversation,
            http_client=http_client
        )

    return OrchestratorResult(
        classification=classification,
        chain_id=chain_id,
        response=response,
        needs_clarification=False,
        chain_output=chain_output
    )


async def _execute_chain(
    chain_id: str,
    user_message: str,
    conversation: list[dict[str, str]],
    http_client
) -> "ChainContext":
    """
    Execute the appropriate chain based on chain_id.

    Args:
        chain_id: The chain to execute ("sdd", "tdd", or "retro")
        user_message: The user's input message
        conversation: Full conversation history
        http_client: HTTP client for LLM calls

    Returns:
        ChainContext with agent outputs
    """
    from src.agents.chains.sdd import SDDChain
    from src.agents.chains.tdd import TDDChain
    from src.agents.chains.retro import RetroChain
    from src.agents.chains.base import ChainContext

    # Map chain_id to chain class
    chain_classes = {
        "sdd": SDDChain,
        "tdd": TDDChain,
        "retro": RetroChain
    }

    chain_class = chain_classes.get(chain_id)
    if chain_class is None:
        logger.error(f"Unknown chain_id: {chain_id}")
        raise ValueError(f"Unknown chain_id: {chain_id}")

    # Create chain instance
    chain = chain_class()

    # Create chain context
    context = ChainContext(
        user_message=user_message,
        conversation_history=conversation,
        memory_context=[],  # TODO: Integrate with memory service
        agent_outputs={},
        current_agent="",
        chain_id=chain_id
    )

    logger.info(f"Executing chain '{chain_id}' for user request")

    # Execute the chain
    result = await chain.execute(context, http_client=http_client)

    if result.error:
        logger.warning(f"Chain '{chain_id}' completed with error: {result.error}")
    else:
        logger.info(f"Chain '{chain_id}' completed successfully with {len(result.agent_outputs)} agent outputs")

    return result
