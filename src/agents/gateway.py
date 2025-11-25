"""
Agent Gateway - OpenAI-compatible API for AI Development Agents.

Place in: /opt/vision_model/src/agents/gateway.py

Connect via Continue.dev or any OpenAI client:
    base_url = "http://CPU_SERVER_IP:9090/v1"

Run:
    python -m src.agents.gateway
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import httpx
import time
import uuid
import json
import os

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
    "orchestrator": "Routes to appropriate flow (SDD/TDD/Retro)",
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
    from src.agents.orchestrator import run_orchestrator
    
    # Extract last user message
    user_message = next(
        (m.content for m in reversed(request.messages) if m.role == "user"),
        ""
    )
    
    # Build conversation history
    conversation = [{"role": m.role, "content": m.content} for m in request.messages]
    
    # Run orchestrator (decides flow, runs agents)
    response_text = await run_orchestrator(
        user_message=user_message,
        conversation=conversation,
        user_id=request.user or "default",
        requested_agent=request.model if request.model != "orchestrator" else None
    )
    
    return ChatResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        created=int(time.time()),
        model=f"agent-gateway/{request.model}",
        choices=[{
            "index": 0,
            "message": {"role": "assistant", "content": response_text},
            "finish_reason": "stop"
        }],
        usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    )

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