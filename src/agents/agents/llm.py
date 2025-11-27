"""
LLM Client - Communication with the LLM service.

Single Responsibility: Make LLM API calls with logging and error handling.
"""

import time
from typing import List, Dict, Optional, Any, Union

from src.agents.logging_config import get_logger, LogEvent
from src.agents.agents.config import (
    LLM_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    LLM_TIMEOUT,
)

logger = get_logger("agents.llm")


async def call_llm(
    http_client,
    messages: List[Dict[str, Any]],
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    model: str = DEFAULT_MODEL,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Call the LLM service with the given messages.

    Args:
        http_client: Async HTTP client for making requests
        messages: List of chat messages in OpenAI format
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum tokens to generate
        model: Model name to use
        tools: Optional list of tool definitions for function calling
        tool_choice: Optional tool choice strategy ("auto", "none", or specific tool)

    Returns:
        The assistant's message dict (may contain 'content' and/or 'tool_calls')

    Raises:
        RuntimeError: If HTTP client is not provided
        Exception: If the LLM service is unavailable or returns an error
    """
    if http_client is None:
        raise RuntimeError("HTTP client not initialized")

    url = f"{LLM_BASE_URL}/v1/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    if tools:
        payload["tools"] = tools
    if tool_choice is not None:
        payload["tool_choice"] = tool_choice

    # Calculate approximate prompt size
    prompt_chars = sum(len(m.get("content", "")) for m in messages)

    start_time = time.time()
    logger.info(
        LogEvent.LLM_CALLING,
        extra={
            "url": url,
            "model": model,
            "message_count": len(messages),
            "prompt_chars": prompt_chars,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "has_tools": bool(tools),
            "tool_count": len(tools) if tools else 0,
            "tool_choice": tool_choice
        }
    )

    # Debug: log the FULL payload being sent
    import json as json_module
    logger.info(f"FULL_REQUEST_DEBUG: {json_module.dumps(payload, indent=2, default=str)}")

    try:
        response = await http_client.post(
            url,
            json=payload,
            timeout=LLM_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()
        message = data["choices"][0]["message"]
        content = message.get("content", "")
        tool_calls = message.get("tool_calls")
        duration_ms = (time.time() - start_time) * 1000

        # Extract usage if available
        usage = data.get("usage", {})

        logger.info(
            LogEvent.LLM_RESPONSE,
            extra={
                "model": model,
                "duration_ms": round(duration_ms, 2),
                "response_length": len(content) if content else 0,
                "has_tool_calls": bool(tool_calls),
                "tool_call_count": len(tool_calls) if tool_calls else 0,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "response_preview": (content[:200] + "..." if len(content) > 200 else content) if content else "[tool_calls]"
            }
        )

        return message

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            LogEvent.LLM_ERROR,
            extra={
                "url": url,
                "model": model,
                "error": str(e),
                "error_type": type(e).__name__,
                "duration_ms": round(duration_ms, 2)
            },
            exc_info=True
        )
        raise


__all__ = ["call_llm"]
