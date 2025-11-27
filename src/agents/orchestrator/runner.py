"""
Orchestrator Runner - Main orchestration logic and chain execution.

Single Responsibility: Route requests to appropriate workflow chains.
"""

from src.agents.logging_config import get_logger

from src.agents.orchestrator.models import Intent, OrchestratorResult
from src.agents.orchestrator.constants import (
    CONFIDENCE_THRESHOLD,
    CLARIFYING_QUESTION,
    INTENT_DISPLAY_NAMES,
)
from src.agents.orchestrator.classifier import classify_intent

logger = get_logger("orchestrator.runner")


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

    # Handle general questions (not development workflow related)
    # Call LLM directly to generate response
    if classification.intent == Intent.GENERAL:
        logger.info(f"General question from user {user_id}, calling LLM")
        from src.agents.agents.llm import call_llm
        llm_message = await call_llm(
            http_client=http_client,
            messages=[{"role": "user", "content": user_message}]
        )
        llm_response = llm_message.get("content", "")
        return OrchestratorResult(
            classification=classification,
            chain_id=None,
            response=llm_response,
            needs_clarification=False,
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
):
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


__all__ = ["run_orchestrator"]
