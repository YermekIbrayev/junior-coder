"""
Chat Completions Endpoint - Main entry point for chat requests.

Single Responsibility: Handle chat completion requests and orchestration.
"""

import time
import uuid

from fastapi import APIRouter

from src.agents.logging_config import (
    get_logger, set_request_context, clear_request_context, LogEvent
)

# Import from gateway for backward compatibility with test mocks
import src.agents.gateway as gateway
from src.agents.gateway.models import ChatRequest
from src.agents.gateway.endpoints.helpers import (
    extract_result, log_completion, store_memory, build_response, handle_error
)

logger = get_logger("gateway.chat")

router = APIRouter()

# HTTP client reference (set by app factory)
_http_client = None


def set_http_client(client):
    """Set the HTTP client for chat endpoint."""
    global _http_client
    _http_client = client


@router.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """
    Main entry point. Routes to appropriate agent.

    Models/Agents:
      - "orchestrator": Auto-route to best flow
      - "spec-analyst": Direct call to Spec Analyst
      - etc.
    """
    start_time = time.time()
    request_id = f"req-{uuid.uuid4().hex[:12]}"

    set_request_context(
        request_id=request_id,
        user_id=request.user or "default",
        model=request.model
    )

    user_message = next(
        (m.content for m in reversed(request.messages) if m.role == "user"),
        ""
    )
    conversation = [{"role": m.role, "content": m.content} for m in request.messages]

    logger.info(
        LogEvent.REQUEST_RECEIVED,
        extra={
            "method": "POST",
            "path": "/v1/chat/completions",
            "stream": request.stream,
            "message_count": len(request.messages),
            "message_preview": user_message[:100] + "..." if len(user_message) > 100 else user_message,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }
    )

    try:
        result = await gateway.run_orchestrator(
            user_message=user_message,
            conversation=conversation,
            user_id=request.user or "default",
            requested_agent=request.model if request.model != "orchestrator" else None,
            http_client=_http_client,
            execute_chain=True
        )

        response_text, chain_id, intent, confidence = extract_result(result)
        response_time_ms = (time.time() - start_time) * 1000

        log_completion(intent, confidence, chain_id, response_time_ms, response_text)
        await store_memory(user_message, response_text, request, chain_id, intent, response_time_ms)

        return build_response(request, response_text, request_id)

    except Exception as e:
        return handle_error(e, start_time)

    finally:
        clear_request_context()


__all__ = ["router", "set_http_client"]
