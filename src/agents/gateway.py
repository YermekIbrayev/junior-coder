"""
Agent Gateway - OpenAI-compatible API for AI Development Agents.

Place in: /opt/vision_model/src/agents/gateway.py

Connect via Continue.dev or any OpenAI client:
    base_url = "http://CPU_SERVER_IP:9090/v1"

Run:
    python -m src.agents.gateway
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
import httpx
import time
import uuid
import os
import json

from src.agents.logging_config import (
    get_logger, setup_logging, set_request_context, clear_request_context,
    LogEvent, log_with_duration
)
from src.agents.orchestrator import run_orchestrator, OrchestratorResult

# Initialize structured logging
setup_logging()
logger = get_logger("gateway")

# ============================================================================
# CONFIGURATION
# ============================================================================

GB10_URL = os.getenv("GB10_URL", "http://192.168.51.22:8080")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
AGENT_PORT = int(os.getenv("AGENT_PORT", "9090"))

# ============================================================================
# MODELS
# ============================================================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "orchestrator"
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False
    user: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list
    usage: dict

# ============================================================================
# GLOBALS
# ============================================================================

http_client: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    http_client = httpx.AsyncClient(timeout=120.0)
    yield
    await http_client.aclose()

# ============================================================================
# APP
# ============================================================================

app = FastAPI(
    title="Agent Gateway",
    description="OpenAI-compatible API for AI development agents",
    version="0.1.0",
    lifespan=lifespan
)

# ============================================================================
# AGENT REGISTRY
# ============================================================================

AGENTS = {
    # Orchestrator (main entry point)
    "orchestrator": "Routes to appropriate flow (SDD/TDD/Retro)",

    # Agent Chains (workflow orchestration)
    "sdd": "Specification-Driven Development chain (5 agents)",
    "tdd": "Test-Driven Development chain (3 agents)",
    "retro": "Retrospective Analysis chain (3 agents)",

    # Individual Agents
    "spec-analyst": "Analyzes requirements, creates specifications",
    "spec-clarifier": "Identifies ambiguities, asks clarifying questions",
    "test-architect": "Designs test strategy, writes failing tests (RED)",
    "code-planner": "Designs architecture using SOLID principles",
    "alignment-analyzer": "Verifies spec/tests/architecture alignment",
    "implementation-specialist": "Makes tests pass (GREEN)",
    "quality-guardian": "Refactors, security scan, production certification",
    "knowledge-curator": "Extracts learnings from development",
    "synthesis-specialist": "Aggregates retrospectives",
    "system-improver": "Recommends system improvements",
    "vibe-check-guardian": "Challenges assumptions, identifies blind spots",
}

# ============================================================================
# MEMORY HELPERS
# ============================================================================

# Global memory client (initialized lazily)
memory_client = None


async def get_memory_client():
    """Get or create the memory client."""
    global memory_client
    if memory_client is None:
        try:
            from qdrant_client import QdrantClient
            from src.agents.memory.client import MemoryClient

            qdrant = QdrantClient(url=QDRANT_URL)
            memory_client = MemoryClient(
                qdrant_client=qdrant,
                http_client=http_client
            )
            logger.info(f"Memory client initialized with Qdrant at {QDRANT_URL}")
        except Exception as e:
            logger.warning(f"Failed to initialize memory client: {e}")
            return None
    return memory_client


async def store_conversation_memory(
    content: str,
    user_id: str,
    metadata: dict | None = None
) -> None:
    """
    Store a conversation exchange in memory.

    Args:
        content: Combined user message and assistant response
        user_id: User identifier for memory isolation
        metadata: Optional metadata (chain_id, model, etc.)
    """
    client = await get_memory_client()
    if client is None:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": "client_not_available", "operation": "store", "user_id": user_id}
        )
        return

    try:
        await client.store_memory(
            content=content,
            user_id=user_id,
            metadata=metadata
        )
        logger.debug(
            LogEvent.MEMORY_STORED,
            extra={"user_id": user_id, "content_length": len(content)}
        )
    except Exception as e:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={"error": str(e), "error_type": type(e).__name__, "operation": "store"}
        )


# ============================================================================
# ERROR HELPERS
# ============================================================================

def create_error_response(message: str, error_type: str, code: str) -> dict:
    """
    Create an OpenAI-style error response.

    Args:
        message: Human-readable error message
        error_type: Error type (e.g., "service_unavailable", "invalid_request")
        code: Error code (e.g., "llm_unavailable")

    Returns:
        Dict in OpenAI error format
    """
    return {
        "error": {
            "message": message,
            "type": error_type,
            "code": code
        }
    }


# ============================================================================
# STREAMING HELPERS
# ============================================================================

async def generate_stream_response(
    response_text: str,
    model: str,
    completion_id: str
) -> AsyncGenerator[str, None]:
    """
    Generate SSE stream chunks for OpenAI-compatible streaming.

    OpenAI streaming format:
    1. First chunk: delta contains {"role": "assistant"}
    2. Content chunks: delta contains {"content": "..."}
    3. Final chunk: delta is {}, finish_reason is "stop"
    4. Stream ends with "data: [DONE]"
    """
    # First chunk: role announcement (required by OpenAI spec)
    first_chunk = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {"role": "assistant", "content": ""},
            "finish_reason": None
        }]
    }
    yield f"data: {json.dumps(first_chunk)}\n\n"

    # Content chunks: stream word by word
    words = response_text.split(' ')
    for i, word in enumerate(words):
        content = word if i == 0 else ' ' + word
        chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": content},
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(chunk)}\n\n"

    # Final chunk: finish_reason
    final_chunk = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "agent-gateway",
        "agents": list(AGENTS.keys()),
        "gb10_url": GB10_URL,
        "qdrant_url": QDRANT_URL
    }

@app.get("/v1/models")
async def list_models():
    """List available agents as 'models'."""
    return {
        "object": "list",
        "data": [
            {
                "id": agent_id,
                "object": "model",
                "owned_by": "agent-gateway",
                "description": desc
            }
            for agent_id, desc in AGENTS.items()
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """
    Main entry point. Routes to appropriate agent.

    Models/Agents:
      - "orchestrator": Auto-route to best flow
      - "spec-analyst": Direct call to Spec Analyst
      - "test-architect": Direct call to Test Architect
      - etc.
    """
    # Track request start time for latency logging
    start_time = time.time()

    # Generate request ID for tracing
    request_id = f"req-{uuid.uuid4().hex[:12]}"

    # Set request context for all subsequent logging
    set_request_context(
        request_id=request_id,
        user_id=request.user or "default",
        model=request.model
    )

    # Extract last user message
    user_message = next(
        (m.content for m in reversed(request.messages) if m.role == "user"),
        ""
    )

    # Build conversation history
    conversation = [{"role": m.role, "content": m.content} for m in request.messages]

    # Log incoming request with structured data
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
        # Run orchestrator (decides flow, runs agents)
        result = await run_orchestrator(
            user_message=user_message,
            conversation=conversation,
            user_id=request.user or "default",
            requested_agent=request.model if request.model != "orchestrator" else None,
            http_client=http_client,
            execute_chain=True
        )

        # Extract response text from OrchestratorResult
        if isinstance(result, OrchestratorResult):
            chain_id = result.chain_id
            intent = result.classification.intent.value if result.classification else "unknown"
            confidence = result.classification.confidence if result.classification else 0.0

            # Use chain output if available (last agent's output)
            if result.chain_output and result.chain_output.agent_outputs:
                # Get the last agent's output as the final response
                last_agent = list(result.chain_output.agent_outputs.keys())[-1]
                response_text = result.chain_output.agent_outputs[last_agent]
            else:
                response_text = result.response
        else:
            # Fallback for backward compatibility
            response_text = str(result)
            chain_id = None
            intent = "unknown"
            confidence = 0.0

        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000

        # Log request completion with structured data
        logger.info(
            LogEvent.REQUEST_COMPLETED,
            extra={
                "intent": intent,
                "confidence": round(confidence, 3),
                "chain_id": chain_id,
                "duration_ms": round(response_time_ms, 2),
                "response_length": len(response_text),
                "response_preview": response_text[:200] + "..." if len(response_text) > 200 else response_text
            }
        )

        # Store conversation to memory (non-blocking, failures logged)
        # Memory storage failures must not affect response delivery
        try:
            logger.debug(
                LogEvent.MEMORY_STORING,
                extra={"content_length": len(user_message) + len(response_text)}
            )
            await store_conversation_memory(
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

        completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
        model_name = f"agent-gateway/{request.model}"

        # Handle streaming response
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

        # Non-streaming response
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
    except Exception as e:
        # Calculate error response time
        error_time_ms = (time.time() - start_time) * 1000
        logger.error(
            LogEvent.REQUEST_FAILED,
            extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "duration_ms": round(error_time_ms, 2)
            },
            exc_info=True  # Include stack trace
        )

        # Return 503 for LLM/service unavailability
        return JSONResponse(
            status_code=503,
            content=create_error_response(
                message=f"LLM service unavailable: {str(e)}",
                error_type="service_unavailable",
                code="llm_unavailable"
            )
        )
    finally:
        # Clear request context after request completes
        clear_request_context()

# ============================================================================
# RUN
# ============================================================================

def run():
    import uvicorn
    print(f"🚀 Agent Gateway starting on port {AGENT_PORT}")
    print(f"   GB10: {GB10_URL}")
    print(f"   Qdrant: {QDRANT_URL}")
    print(f"   Agents: {len(AGENTS)}")
    uvicorn.run(app, host="0.0.0.0", port=AGENT_PORT)

if __name__ == "__main__":
    run()