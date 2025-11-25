"""
API routes for the orchestrator
Handles query, embedding, and indexing endpoints
Includes OpenAI-compatible /v1/chat/completions endpoint
"""
from fastapi import APIRouter, HTTPException, Request
from api.models import (
    QueryRequest, QueryResponse,
    EmbeddingRequest, EmbeddingResponse,
    IndexRequest, IndexResponse
)
from services.router import route_query
from services.embedding import get_embeddings
from services.vector_db import search_similar, index_documents
from services.llm_client import call_llm
from services.sequential_thinking import perform_sequential_thinking
from core.config import settings
from core.logger import get_logger
import time
import uuid

logger = get_logger(__name__)
router = APIRouter()

# Global memory client (initialized in main.py)
mem0_client = None

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main query endpoint with intelligent routing and RAG
    """
    start_time = time.time()
    logger.info(f"Query endpoint called: query_length={len(request.query)}, use_rag={request.use_rag}")

    try:
        # Step 1: Route the query
        route_decision = await route_query(request.query)
        logger.debug(f"Route decision: {route_decision}")

        # Step 2: Handle based on routing decision
        if request.use_rag is False or route_decision == "simple":
            # Simple query: Use Qwen directly
            response_text = await call_llm(
                url=settings.QWEN_ROUTER_URL,
                messages=[{"role": "user", "content": request.query}],
                max_tokens=request.max_tokens
            )
            model_used = "qwen-2.5-1.5b"
            rag_used = False
            context_chunks = 0

        else:
            # Complex/Factual: Use RAG + GPT-OSS
            # Get embedding
            embeddings = await get_embeddings([request.query])
            query_embedding = embeddings[0]

            # Search similar documents
            contexts = await search_similar(query_embedding, top_k=request.top_k)
            context_text = "\n\n".join([c["text"] for c in contexts])

            # Build messages with context
            messages = [
                {"role": "system", "content": f"Context:\n{context_text}"},
                {"role": "user", "content": request.query}
            ]

            # Call GPT-OSS
            response_text = await call_llm(
                url=settings.GPT_OSS_URL,
                messages=messages,
                max_tokens=request.max_tokens
            )
            model_used = "gpt-oss-120b"
            rag_used = True
            context_chunks = len(contexts)

        latency_ms = (time.time() - start_time) * 1000

        return QueryResponse(
            response=response_text,
            model_used=model_used,
            rag_used=rag_used,
            context_chunks=context_chunks,
            latency_ms=latency_ms,
            route_decision=route_decision
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed", response_model=EmbeddingResponse)
async def embed_endpoint(request: EmbeddingRequest):
    """Generate embeddings for texts"""
    try:
        embeddings = await get_embeddings(request.texts)
        return EmbeddingResponse(
            embeddings=embeddings,
            dimension=1024,
            count=len(embeddings)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index", response_model=IndexResponse)
async def index_endpoint(request: IndexRequest):
    """Index documents into Qdrant"""
    start_time = time.time()

    try:
        # Generate embeddings
        embeddings = await get_embeddings(request.documents)

        # Index into Qdrant
        count = await index_documents(request.documents, embeddings)

        latency_ms = (time.time() - start_time) * 1000

        return IndexResponse(
            indexed_count=count,
            collection=settings.QDRANT_COLLECTION,
            latency_ms=latency_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/chat/completions")
async def chat_completions_endpoint(request: Request):
    """
    OpenAI-compatible chat completions endpoint

    Accepts standard OpenAI format and returns standard OpenAI response
    ALWAYS uses sequential thinking and memory integration

    Standard OpenAI format:
    {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.7,
        "max_tokens": 1024,
        "user": "optional-user-id"
    }
    """
    start_time = time.time()
    request_id = uuid.uuid4().hex[:8]

    try:
        # Parse OpenAI-format request
        body = await request.json()
        messages = body.get("messages", [])
        model = body.get("model", "gpt-oss-120b")
        temperature = body.get("temperature", 0.7)
        max_tokens = body.get("max_tokens", 1024)
        user_id = body.get("user", f"session-{uuid.uuid4().hex[:8]}")

        logger.info(f"[{request_id}] Chat completion request received: user={user_id}, messages={len(messages)}, model={model}, temp={temperature}, max_tokens={max_tokens}")

        if not messages:
            logger.error(f"[{request_id}] No messages in request")
            raise HTTPException(status_code=400, detail="messages field is required")

        # Extract last user message as query
        user_messages = [m for m in messages if m.get("role") == "user"]
        if not user_messages:
            logger.error(f"[{request_id}] No user messages found")
            raise HTTPException(status_code=400, detail="At least one user message required")

        query = user_messages[-1].get("content", "")
        logger.debug(f"[{request_id}] Extracted query (length={len(query)}): {query[:100]}...")

        # STEP 1: Retrieve memories
        memory_context = ""
        memory_used = False
        logger.debug(f"[{request_id}] STEP 1: Retrieving memories for user={user_id}")
        if mem0_client:
            try:
                memories = await mem0_client.search_memories(
                    query=query,
                    user_id=user_id,
                    agent_id="orchestrator",
                    limit=3
                )
                if memories:
                    memory_used = True
                    memory_texts = [m["content"] for m in memories]
                    memory_context = "\n".join(memory_texts)
                    logger.info(f"[{request_id}] ✓ Retrieved {len(memories)} memories (total chars: {len(memory_context)})")
                else:
                    logger.debug(f"[{request_id}] No memories found for user")
            except Exception as e:
                logger.warning(f"[{request_id}] Memory retrieval error: {e}", exc_info=True)
        else:
            logger.warning(f"[{request_id}] Mem0 client not initialized")

        # STEP 2: Sequential thinking (ALWAYS ENABLED)
        logger.debug(f"[{request_id}] STEP 2: Performing sequential thinking")
        thinking_result = await perform_sequential_thinking(query, memory_context)
        thoughts = thinking_result["thoughts"]
        enriched_query = thinking_result["enriched_query"]
        logger.info(f"[{request_id}] ✓ Thinking complete (thoughts: {len(thoughts)} chars, enriched query: {len(enriched_query)} chars)")
        logger.debug(f"[{request_id}] Thoughts: {thoughts[:200]}...")

        # STEP 3: Route the query
        logger.debug(f"[{request_id}] STEP 3: Routing query")
        route_decision = await route_query(enriched_query)
        logger.info(f"[{request_id}] ✓ Route decision: {route_decision}")

        # STEP 4: Generate response based on routing
        logger.debug(f"[{request_id}] STEP 4: Generating response")
        if route_decision == "simple":
            # Simple: Use Qwen directly
            logger.debug(f"[{request_id}] Calling Qwen at {settings.QWEN_ROUTER_URL}")
            response_text = await call_llm(
                url=settings.QWEN_ROUTER_URL,
                messages=[{"role": "user", "content": enriched_query}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            model_used = "qwen-2.5-1.5b"
            rag_used = False
            logger.info(f"[{request_id}] ✓ Qwen response received (length: {len(response_text)} chars)")

        else:
            # Complex/Factual: Use RAG + GPT-OSS
            logger.debug(f"[{request_id}] Getting embeddings for query")
            embeddings = await get_embeddings([enriched_query])
            query_embedding = embeddings[0]

            logger.debug(f"[{request_id}] Searching for similar contexts (top_k=5)")
            contexts = await search_similar(query_embedding, top_k=5)
            context_text = "\n\n".join([c["text"] for c in contexts])
            logger.info(f"[{request_id}] ✓ Retrieved {len(contexts)} context chunks (total: {len(context_text)} chars)")

            # Build messages with all context
            full_context = []
            if memory_context:
                full_context.append(f"Previous conversation context:\n{memory_context}")
            if thoughts:
                full_context.append(f"Reasoning:\n{thoughts}")
            if context_text:
                full_context.append(f"Knowledge base:\n{context_text}")

            system_message = {"role": "system", "content": "\n\n".join(full_context)}

            # Include conversation history from messages
            conversation_messages = [system_message]
            for msg in messages:
                if msg.get("role") in ["user", "assistant"]:
                    conversation_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            logger.debug(f"[{request_id}] Calling GPT-OSS at {settings.GPT_OSS_URL} with {len(conversation_messages)} messages")
            response_text = await call_llm(
                url=settings.GPT_OSS_URL,
                messages=conversation_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            model_used = "gpt-oss-120b"
            rag_used = True
            logger.info(f"[{request_id}] ✓ GPT-OSS response received (length: {len(response_text)} chars)")

        # STEP 5: Store memory
        logger.debug(f"[{request_id}] STEP 5: Storing memory")
        if mem0_client:
            try:
                await mem0_client.add_memory(
                    user_id=user_id,
                    agent_id="orchestrator",
                    messages=[
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": response_text}
                    ],
                    metadata={
                        "route_decision": route_decision,
                        "model_used": model_used,
                        "thinking": thoughts[:200] if thoughts else ""  # Store truncated thoughts
                    }
                )
                logger.info(f"[{request_id}] ✓ Memory stored for user={user_id}")
            except Exception as e:
                logger.warning(f"[{request_id}] Memory storage error: {e}", exc_info=True)
        else:
            logger.debug(f"[{request_id}] Mem0 client not available, skipping memory storage")

        # STEP 6: Return OpenAI-format response
        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] ✅ Request complete: model={model_used}, rag={rag_used}, latency={latency_ms:.1f}ms")

        # Estimate token counts (rough approximation)
        prompt_tokens = sum(len(m.get("content", "").split()) for m in messages) * 1.3
        completion_tokens = len(response_text.split()) * 1.3

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model_used,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": int(prompt_tokens),
                "completion_tokens": int(completion_tokens),
                "total_tokens": int(prompt_tokens + completion_tokens)
            },
            # Custom metadata (OpenAI clients will ignore these)
            "x_route_decision": route_decision,
            "x_rag_used": rag_used,
            "x_memory_used": memory_used,
            "x_thinking_used": bool(thoughts),
            "x_latency_ms": latency_ms
        }

    except HTTPException as e:
        logger.error(f"[{request_id}] HTTP exception: {e.status_code} - {e.detail}")
        raise
    except Exception as e:
        logger.error(f"[{request_id}] ❌ Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
