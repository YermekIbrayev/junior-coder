"""
Orchestrator Classifier - Intent classification using LLM.

Single Responsibility: Classify user intent from natural language.
"""

import json
import time

from src.agents.logging_config import get_logger, LogEvent

from src.agents.orchestrator.models import Intent, IntentClassification
from src.agents.orchestrator.constants import (
    CLASSIFICATION_MODEL,
    CLASSIFICATION_PROMPT,
    CLASSIFICATION_TEMPERATURE,
    CLASSIFICATION_MAX_TOKENS,
)

logger = get_logger("orchestrator.classifier")


async def classify_intent(user_message: str, http_client) -> IntentClassification:
    """
    Classify the user's intent using the LLM.

    Args:
        user_message: The user's input message to classify
        http_client: Async HTTP client for LLM calls

    Returns:
        IntentClassification with intent, confidence, and reasoning
    """
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


__all__ = ["classify_intent"]
