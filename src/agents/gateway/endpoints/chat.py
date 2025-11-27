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
from fastapi.responses import StreamingResponse

from src.agents.gateway.endpoints.helpers import (
    extract_result, log_completion, store_memory, build_response, build_tool_response, handle_error
)
from src.agents.gateway.streaming import generate_tool_stream_response
from src.agents.agents.llm import call_llm

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

    has_tools = bool(request.tools)

    logger.info(
        LogEvent.REQUEST_RECEIVED,
        extra={
            "method": "POST",
            "path": "/v1/chat/completions",
            "stream": request.stream,
            "message_count": len(request.messages),
            "message_preview": user_message[:100] + "..." if len(user_message) > 100 else user_message,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "has_tools": has_tools,
            "tool_count": len(request.tools) if request.tools else 0
        }
    )

    try:
        # When tools are provided, call LLM directly with tools (bypass orchestrator)
        if has_tools:
            logger.info(f"Tool-enabled request with {len(request.tools)} tools, calling LLM directly")

            # Convert tools to dict format for LLM (exclude None values)
            tools_dict = [tool.model_dump(exclude_none=True) for tool in request.tools]
            tool_choice = request.tool_choice

            # Build messages including all message types (user, assistant, tool, etc.)
            messages = []
            for m in request.messages:
                msg = {"role": m.role}
                if m.content is not None:
                    msg["content"] = m.content
                if m.tool_calls:
                    msg["tool_calls"] = m.tool_calls
                if m.tool_call_id:
                    msg["tool_call_id"] = m.tool_call_id
                messages.append(msg)

            llm_message = await call_llm(
                http_client=_http_client,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tools=tools_dict,
                tool_choice=tool_choice
            )

            response_time_ms = (time.time() - start_time) * 1000
            log_completion("tool_call", 1.0, None, response_time_ms, str(llm_message))

            # Handle streaming for tool-enabled requests
            if request.stream:
                completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
                model_name = f"agent-gateway/{request.model}"
                logger.debug(f"Streaming tool response: {completion_id}")
                return StreamingResponse(
                    generate_tool_stream_response(llm_message, model_name, completion_id),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                        "X-Accel-Buffering": "no"
                    }
                )

            return build_tool_response(request, llm_message, request_id)

        # Standard orchestrator flow (no tools)
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
