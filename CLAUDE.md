# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

MUST: use sequentual thinking when solving problems

This is a **multi-model LLM orchestration system** designed for NVIDIA GB10 (sm_121) with 128GB unified memory. The system intelligently routes queries between three LLM models based on complexity, with optional RAG (Retrieval Augmented Generation) support.

## Architecture

### Service Topology

```
Query → Sequential Thinking → Memory Retrieval → Qwen2.5-1.5B (Router) → [Decision]
                                                                          ├→ Simple queries → Qwen (direct)
                                                                          ├→ Complex queries → GPT-OSS-120B (reasoning)
                                                                          └→ Factual queries → GPT-OSS-120B + RAG
                                                                                                    ↓
                                                                                          Memory Storage (Mem0)
```

**CRITICAL RULE**: ALL queries MUST use sequential thinking BEFORE routing. This provides structured reasoning for better classification and response generation.

### Components

1. **LLM Services** (TensorRT-LLM):
   - `gpt-oss-120b` (port 8000): Main reasoning model, 120B params, MXFP4 quantization
   - `bge-m3` (port 8001): Embedding model, 1024-dim vectors, FP8 quantization
   - `qwen-router` (port 8002): Query classifier, 1.5B params, deterministic routing

2. **Vector Database** (external CPU server):
   - `qdrant` (port 6333): COSINE-distance search, "documents" collection

3. **Orchestrator** (FastAPI, port 8080):
   - Routes queries and manages LLM communication
   - Implements RAG pipeline: embedding → search → context injection
   - All HTTP calls use pooled `httpx.AsyncClient` (100 max connections)

## Common Commands

### Development

```bash
# Run tests
cd orchestrator
pytest tests/ -v --asyncio-mode=auto

# Run specific test file
pytest tests/test_mem0_client.py -v

# Run with coverage
pytest tests/ --cov=services --cov-report=html

# Run verification script (full TDD check)
cd orchestrator
./verify_implementation.sh
```

### Deployment

```bash
# Start orchestrator
./start_orchestrator.sh

# Check service health
curl http://localhost:8080/health

# View logs in real-time
tail -f /opt/vision_model/orchestrator_restart.log

# View last 100 lines
tail -n 100 /opt/vision_model/orchestrator_restart.log

# Stop orchestrator
pkill -f "uvicorn main:app"
```

### Testing the API

```bash
# OpenAI-compatible chat completion (PRIMARY ENDPOINT - ALWAYS uses sequential thinking + memory)
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "temperature": 0.7,
    "max_tokens": 1024,
    "user": "user-123"
  }'

# Use with OpenAI Python client
export OPENAI_API_BASE=http://localhost:8080/v1
export OPENAI_API_KEY=dummy  # Not required but some clients need it
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8080/v1', api_key='dummy')
response = client.chat.completions.create(
    model='gpt-4',
    messages=[{'role': 'user', 'content': 'Hello!'}],
    user='user-123'
)
print(response.choices[0].message.content)
"

# Legacy query endpoint (without memory/thinking)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, how are you?"}'

# Generate embeddings
curl -X POST http://localhost:8080/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["test document"]}'

# Index documents
curl -X POST http://localhost:8080/index \
  -H "Content-Type: application/json" \
  -d '{"documents": ["Document 1", "Document 2"]}'
```

## Critical Implementation Patterns

### Sequential Thinking Pipeline (NEW - ALWAYS ENABLED)

**File**: `orchestrator/services/sequential_thinking.py`

Every query through `/v1/chat/completions` undergoes sequential thinking BEFORE routing:

1. **Memory Retrieval**: Fetch relevant past conversations using Mem0Client
2. **Chain-of-Thought**: Qwen performs reasoning with memory context
3. **Query Enrichment**: Original query + reasoning thoughts → enriched query
4. **Routing**: Enriched query classified by router
5. **Generation**: LLM generates response with full context
6. **Memory Storage**: Conversation stored for future retrieval

**Flow**: `Query → Memory → Thinking → Routing → Generation → Storage`

**Why**: Provides context-aware, reasoned responses with conversation continuity across sessions.

### Memory Integration (Mem0Client)

**File**: `orchestrator/services/mem0_client.py`

- **Collection**: `agent_memories` (configured in `core/config.py`)
- **Storage**: Each user message + assistant response stored with metadata
- **Retrieval**: Top-3 relevant memories fetched using semantic search
- **User Tracking**: `user` field in OpenAI request used for isolation

**Memory Payload**:
```python
{
    "content": "user query + assistant response",
    "user_id": "user-123",
    "agent_id": "orchestrator",
    "timestamp": 1234567890.0,
    "route_decision": "complex",
    "model_used": "gpt-oss-120b",
    "thinking": "truncated reasoning"
}
```

**When adding new features**: Always pass `user_id` through the pipeline for memory isolation.

### HTTP Client Lifecycle

**File**: `orchestrator/main.py:12-18`

The global `http_client` is initialized at app startup via `lifespan` context manager and shared across all services. This is async-safe but NOT thread-safe.

**When adding new LLM service calls**: Always use `services/llm_client.call_llm()` which reuses the pooled client. Never create per-request clients.

### Query Routing Logic

**File**: `orchestrator/services/router.py`

- All routing decisions are **stateless and deterministic** (temperature=0.0)
- Three categories: "simple", "complex", "factual"
- Safe-defaults to "complex" on any error
- Returns classification text only (stripped/lowercased)

**When modifying routing**: Keep categories as enum-like strings. Never call router twice for the same query.

### RAG Pipeline

**File**: `orchestrator/api/routes.py:42-61`

Flow: Query → BGE-M3 embedding → Qdrant search → Context injection → GPT-OSS

- Embeddings are always 1024-dim (BGE-M3)
- Context chunks joined with `"\n\n"`
- Top-k defaults to 5 documents
- System message contains context, user message contains query

**When modifying RAG**: Ensure embedding dimensions match Qdrant collection (1024).

### Configuration Management

**File**: `orchestrator/core/config.py`

All timeouts, URLs, and settings centralized in `Settings` class (Pydantic):
- Service URLs: GPT_OSS_URL, BGE_M3_URL, QWEN_ROUTER_URL, QDRANT_URL
- Timeouts: ROUTER_TIMEOUT=10s, EMBEDDING_TIMEOUT=30s, LLM_TIMEOUT=120s
- Qdrant: collection="documents", 1024 dims, COSINE distance

**When adding parameters**: Add to `Settings` class, never hardcode. Load from `.env` or environment variables.

## Testing Infrastructure

**Files**: `orchestrator/tests/conftest.py`, `verify_implementation.sh`

- Uses `pytest` + `pytest-asyncio` for async tests
- Fixtures in `conftest.py` mock Qdrant, HTTP clients, Mem0, ApeRAG
- All async tests use `AsyncMock` (not `MagicMock`)
- Current coverage: Mem0Client (5 tests ✅) and ApeRAGClient (5 tests ✅)

**When writing tests**: Mock `http_client` and `qdrant_client` from conftest fixtures. Don't hit real services in unit tests.

## Deployment Architecture

**Files**: `DEPLOY.md`, `start_orchestrator.sh`

### Two-Server Setup
- **GPU Server (GB10)**: 3 LLM services + Orchestrator
- **CPU Server** (external): Qdrant vector database

**Critical setup**:
1. Set `QDRANT_URL=http://CPU_SERVER_IP:6333` in `.env`
2. Run `./start_orchestrator.sh` to launch orchestrator
3. LLM services should be running on their respective ports (8000, 8001, 8002)

### Service Memory Layout (128GB GB10)
- GPT-OSS: ~60GB (MXFP4)
- BGE-M3: ~2GB (FP8)
- Qwen Router: ~3GB (FP8)
- Orchestrator: ~2GB
- KV Cache: ~61GB free

## Model Configuration

### Latency vs Throughput Modes

**Latency Mode** (default, `gpt-oss-120b-latency.yaml`):
- TTFT < 100ms
- max_batch_size: 128
- Best for: Interactive chat, single-user

**Throughput Mode** (`gpt-oss-120b-throughput.yaml`):
- 1000+ concurrent users
- Higher batch sizes
- Best for: Production, multi-user

**To switch modes**: Update the model configuration file used by the GPT-OSS service and restart the service.

### Blackwell (sm_121) Optimization

**Critical**: All model configs use `moe_config.backend: TRTLLM` (NOT CUTLASS). TRTLLM is faster on Blackwell architecture.

## API Contracts

### POST /v1/chat/completions (PRIMARY ENDPOINT)

**Standard OpenAI-compatible endpoint - use this for all new integrations**

**Request**: Standard OpenAI format
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "user": "user-123"
}
```

**Response**: Standard OpenAI format with custom extensions
```json
{
  "id": "chatcmpl-abc123...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-oss-120b",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "Hello! How can I help you?"},
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 10,
    "total_tokens": 30
  },
  "x_route_decision": "simple",
  "x_rag_used": false,
  "x_memory_used": true,
  "x_thinking_used": true,
  "x_latency_ms": 245.6
}
```

**Features**:
- ✅ OpenAI client drop-in compatible
- ✅ Sequential thinking ALWAYS enabled
- ✅ Memory retrieval and storage per user
- ✅ Conversation history support
- ✅ Auto-routing (simple/complex/factual)
- ✅ RAG integration for complex queries

### POST /query (LEGACY)

**Request**: `QueryRequest`
- `query` (required): User query string
- `max_tokens` (default 1024): Max response tokens
- `use_rag` (None=auto): Force RAG on/off
- `top_k` (default 5): RAG context chunks

**Response**: `QueryResponse`
- `response`: Generated text
- `model_used`: "qwen-2.5-1.5b" or "gpt-oss-120b"
- `rag_used`: Boolean
- `context_chunks`: Number of RAG chunks used
- `latency_ms`: Request latency
- `route_decision`: "simple", "complex", or "factual"

### POST /embed

**Request**: `EmbeddingRequest`
- `texts`: List of strings

**Response**: `EmbeddingResponse`
- `embeddings`: List of 1024-dim vectors
- `dimension`: 1024
- `count`: Number of embeddings

### POST /index

**Request**: `IndexRequest`
- `documents`: List of strings to index

**Response**: `IndexResponse`
- `indexed_count`: Number of documents indexed
- `collection`: Qdrant collection name
- `latency_ms`: Indexing latency

## Integration Status

### ✅ Active Integrations

- **Mem0Client** (`services/mem0_client.py`): ACTIVE - Long-term agent memory with per-user isolation
  - Used in `/v1/chat/completions` for conversation continuity
  - Stores all user interactions with metadata
  - Retrieves top-3 relevant memories per query
  - Collection: `agent_memories` (Qdrant)

- **Sequential Thinking** (`services/sequential_thinking.py`): ACTIVE - Chain-of-thought reasoning
  - ALWAYS enabled for `/v1/chat/completions`
  - Uses Qwen router for fast reasoning (256 tokens, temp=0.3)
  - Enriches queries with structured thoughts before routing

### 🔜 Future Integration Points

- **ApeRAG** (`services/aperag_client.py`): Ready for multi-agent reasoning framework
  - Full test coverage in `tests/test_aperag_client.py`
  - Can be activated for advanced graph-based RAG

## Key Implementation Notes

1. **Async everywhere**: All endpoint handlers, service calls, and DB operations are async
2. **Qdrant client is synchronous**: Wrap searches in async functions
3. **Connection pooling**: Single httpx client shared via lifespan context
4. **Deterministic routing**: Router uses temperature=0.0 for consistent classifications
5. **Safe defaults**: On routing failure, defaults to "complex" (safer choice)
6. **OpenAI-compatible**: All LLM services use `/v1/chat/completions` and `/v1/embeddings` endpoints

## Health Checks

Orchestrator `/health` endpoint lists all service URLs and their status:

```bash
curl http://localhost:8080/health
```

This checks connectivity to:
- GPT-OSS (port 8000)
- BGE-M3 (port 8001)
- Qwen Router (port 8002)
- Qdrant (port 6333)
