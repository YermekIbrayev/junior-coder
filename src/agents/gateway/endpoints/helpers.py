"""
Chat Endpoint Helpers - Result extraction, logging, and response building.

Single Responsibility: Support functions for chat endpoint.
"""

import time
import uuid

from fastapi.responses import JSONResponse, StreamingResponse

from src.agents.logging_config import get_logger, LogEvent
import src.agents.gateway as gateway
from src.agents.gateway.models import ChatRequest, ChatResponse
from src.agents.gateway.responses import create_error_response
from src.agents.gateway.streaming import generate_stream_response

logger = get_logger("gateway.chat")


def extract_result(result) -> tuple[str, str | None, str, float]:
    """Extract response data from orchestrator result."""
    if isinstance(result, gateway.OrchestratorResult):
        chain_id = result.chain_id
        intent = result.classification.intent.value if result.classification else "unknown"
        confidence = result.classification.confidence if result.classification else 0.0

        if result.chain_output and result.chain_output.agent_outputs:
            last_agent = list(result.chain_output.agent_outputs.keys())[-1]
            response_text = result.chain_output.agent_outputs[last_agent]
        else:
            response_text = result.response
    else:
        response_text = str(result)
        chain_id = None
        intent = "unknown"
        confidence = 0.0

    return response_text, chain_id, intent, confidence


def log_completion(intent: str, confidence: float, chain_id: str | None, duration_ms: float, response_text: str):
    """Log request completion."""
    logger.info(
        LogEvent.REQUEST_COMPLETED,
        extra={
            "intent": intent,
            "confidence": round(confidence, 3),
            "chain_id": chain_id,
            "duration_ms": round(duration_ms, 2),
            "response_length": len(response_text),
            "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text
        }
    )


async def store_memory(user_message: str, response_text: str, request: ChatRequest, chain_id: str | None, intent: str, response_time_ms: float):
    """Store conversation to memory (non-blocking)."""
    try:
        logger.debug(
            LogEvent.MEMORY_STORING,
            extra={"content_length": len(user_message) + len(response_text)}
        )
        await gateway.store_conversation_memory(
            content=f"User: {user_message}\nAssistant: {response_text}",
            user_id=request.user or "default",
            metadata={
                "model": request.model,
                "chain_id": chain_id,
                "intent": intent,
                "response_time_ms": response_time_ms
            }
        )
        logger.debug(LogEvent.MEMORY_STORED)
    except Exception as mem_error:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": str(mem_error), "error_type": type(mem_error).__name__}
        )


def build_response(request: ChatRequest, response_text: str, request_id: str):
    """Build the appropriate response (streaming or regular)."""
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    model_name = f"agent-gateway/{request.model}"

    if request.stream:
        logger.debug(
            LogEvent.STREAM_STARTING,
            extra={"completion_id": completion_id, "response_length": len(response_text)}
        )
        return StreamingResponse(
            generate_stream_response(response_text, model_name, completion_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    return ChatResponse(
        id=completion_id,
        created=int(time.time()),
        model=model_name,
        choices=[{
            "index": 0,
            "message": {"role": "assistant", "content": response_text},
            "finish_reason": "stop"
        }],
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    )


def handle_error(e: Exception, start_time: float):
    """Handle request errors."""
    error_time_ms = (time.time() - start_time) * 1000
    logger.error(
        LogEvent.REQUEST_FAILED,
        extra={
            "error": str(e),
            "error_type": type(e).__name__,
            "duration_ms": round(error_time_ms, 2)
        },
        exc_info=True
    )

    return JSONResponse(
        status_code=503,
        content=create_error_response(
            message=f"LLM service unavailable: {str(e)}",
            error_type="service_unavailable",
            code="llm_unavailable"
        )
    )


__all__ = ["extract_result", "log_completion", "store_memory", "build_response", "handle_error"]
