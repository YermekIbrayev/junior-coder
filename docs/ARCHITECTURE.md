# Vision Model Architecture

**Version**: 1.0.0 | **Last Updated**: 2025-01-25

Multi-model LLM orchestration system designed for NVIDIA GB10 (sm_121) with 128GB unified memory. The system intelligently routes queries between three LLM models based on complexity, with agent-based development workflows and vector-based memory.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM TOPOLOGY                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────┐    ┌─────────────────────┐   │
│   │         GPU SERVER (GB10)               │    │    CPU SERVER       │   │
│   │         128GB Unified Memory            │    │    256GB RAM        │   │
│   │         NVIDIA Blackwell sm_121         │    │    28 Threads       │   │
│   │                                         │    │                     │   │
│   │  ┌─────────────────────────────────┐   │    │  ┌───────────────┐  │   │
│   │  │ GPT-OSS-120B    :8000           │   │    │  │ Qdrant        │  │   │
│   │  │ (60GB, MXFP4)                   │   │    │  │ :6333/:6334   │  │   │
│   │  └─────────────────────────────────┘   │    │  │               │  │   │
│   │  ┌─────────────────────────────────┐   │    │  │ Collections:  │  │   │
│   │  │ BGE-M3          :8001           │   │    │  │ • memories    │  │   │
│   │  │ (2GB, FP8, 1024-dim)            │   │    │  │ • knowledge   │  │   │
│   │  └─────────────────────────────────┘   │    │  │ • context     │  │   │
│   │  ┌─────────────────────────────────┐   │    │  └───────────────┘  │   │
│   │  │ Qwen Router     :8002           │   │    │                     │   │
│   │  │ (3GB, FP8, 1.5B params)         │   │    │  ┌───────────────┐  │   │
│   │  └─────────────────────────────────┘   │    │  │ Agent Gateway │  │   │
│   │  ┌─────────────────────────────────┐   │    │  │ :9090         │  │   │
│   │  │ Orchestrator    :8080           │   │◄───┼──│ (FastAPI)     │  │   │
│   │  │ (FastAPI)                       │   │    │  └───────────────┘  │   │
│   │  └─────────────────────────────────┘   │    │                     │   │
│   │                                         │    │                     │   │
│   │  Free: ~61GB (KV Cache)                │    │                     │   │
│   └─────────────────────────────────────────┘    └─────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## LLM Services Layer

### Service Specifications

| Service | Port | Model | Parameters | Quantization | Memory | Purpose |
|---------|------|-------|------------|--------------|--------|---------|
| GPT-OSS | 8000 | GPT-OSS-120B | 120B | MXFP4 | ~60GB | Main reasoning |
| BGE-M3 | 8001 | BGE-M3 | - | FP8 | ~2GB | Embeddings (1024-dim) |
| Qwen Router | 8002 | Qwen2.5-1.5B | 1.5B | FP8 | ~3GB | Query classification |
| Orchestrator | 8080 | - | - | - | ~2GB | API gateway |

### Query Routing Logic

```mermaid
flowchart TD
    Query[User Query] --> ST[Sequential Thinking]
    ST --> Memory[Memory Retrieval<br/>Qdrant: agent_memories]
    Memory --> Router[Qwen Router<br/>temp=0.0]

    Router --> Decision{Route Decision}

    Decision -->|simple| Qwen[Qwen Direct Response]
    Decision -->|complex| GPT[GPT-OSS-120B<br/>Reasoning]
    Decision -->|factual| RAG[GPT-OSS + RAG]

    RAG --> Embed[BGE-M3 Embedding]
    Embed --> Search[Qdrant Search<br/>project_knowledge]
    Search --> Context[Context Injection]
    Context --> GPT

    Qwen --> Store[Memory Storage]
    GPT --> Store
    Store --> Response[Response]

    classDef router fill:#4c6ef5,stroke:#364fc7,color:#fff
    classDef llm fill:#51cf66,stroke:#2f9e44,color:#fff
    classDef memory fill:#ffd43b,stroke:#fab005,color:#000
    classDef response fill:#ff6b6b,stroke:#c92a2a,color:#fff

    class Router,Decision router
    class Qwen,GPT,RAG llm
    class Memory,Store,Search memory
    class Response response
```

### Routing Categories

| Category | Criteria | Handler | Use RAG |
|----------|----------|---------|---------|
| `simple` | Greetings, basic questions | Qwen 1.5B | No |
| `complex` | Reasoning, analysis, code | GPT-OSS-120B | No |
| `factual` | Documentation, codebase queries | GPT-OSS-120B | Yes |

---

## Agent Architecture

### Agent Gateway (Port 9090)

OpenAI-compatible API that routes requests to 12 specialized agents.

```mermaid
flowchart LR
    Client[OpenAI Client] --> Gateway[Agent Gateway<br/>:9090]

    Gateway --> Orchestrator[orchestrator]

    Orchestrator --> SDD[SDD Flow]
    Orchestrator --> TDD[TDD Flow]
    Orchestrator --> Retro[Retrospective]

    SDD --> SA[spec-analyst]
    SDD --> SC[spec-clarifier]
    SDD --> AA[alignment-analyzer]

    TDD --> TA[test-architect]
    TDD --> CP[code-planner]
    TDD --> IS[implementation-specialist]
    TDD --> QG[quality-guardian]

    Retro --> KC[knowledge-curator]
    Retro --> SS[synthesis-specialist]
    Retro --> SI[system-improver]

    Gateway --> VCG[vibe-check-guardian]

    classDef gateway fill:#845ef7,stroke:#5f3dc4,color:#fff
    classDef flow fill:#4c6ef5,stroke:#364fc7,color:#fff
    classDef agent fill:#20c997,stroke:#12b886,color:#fff
    classDef vibe fill:#ff922b,stroke:#e8590c,color:#fff

    class Gateway gateway
    class SDD,TDD,Retro flow
    class SA,SC,AA,TA,CP,IS,QG,KC,SS,SI agent
    class VCG vibe
```

### Agent Registry

| Agent | Role | Flow |
|-------|------|------|
| `orchestrator` | Routes to appropriate flow (SDD/TDD/Retro) | Entry |
| `spec-analyst` | Analyzes requirements, creates specifications | SDD |
| `spec-clarifier` | Identifies ambiguities, asks clarifying questions | SDD |
| `alignment-analyzer` | Verifies spec/tests/architecture alignment | SDD |
| `test-architect` | Designs test strategy, writes failing tests (RED) | TDD |
| `code-planner` | Designs architecture using SOLID principles | TDD |
| `implementation-specialist` | Makes tests pass (GREEN) | TDD |
| `quality-guardian` | Refactors, security scan, production certification | TDD |
| `knowledge-curator` | Extracts learnings from development | Retro |
| `synthesis-specialist` | Aggregates retrospectives | Retro |
| `system-improver` | Recommends system improvements | Retro |
| `vibe-check-guardian` | Challenges assumptions, identifies blind spots | Cross-cutting |

---

## Data Layer

### Qdrant Collections

```mermaid
flowchart TB
    subgraph Qdrant["Qdrant Vector Database (CPU Server :6333)"]
        subgraph AM["agent_memories"]
            AM1[12K vectors]
            AM2[1024-dim BGE-M3]
            AM3[int8 quantization]
            AM4["< 15ms latency"]
        end

        subgraph PK["project_knowledge"]
            PK1[100K vectors]
            PK2[1024-dim BGE-M3]
            PK3[binary quantization]
            PK4["20-30ms latency"]
        end

        subgraph SC["shared_context"]
            SC1[1K vectors]
            SC2[1024-dim BGE-M3]
            SC3[no quantization]
            SC4["5-8ms latency"]
        end
    end

    Mem0[Mem0 Client] --> AM
    ApeRAG[ApeRAG GraphRAG] --> PK
    Agents[Agent Coordination] --> SC

    classDef collection fill:#74c0fc,stroke:#339af0,color:#000
    classDef client fill:#8ce99a,stroke:#51cf66,color:#000

    class AM,PK,SC collection
    class Mem0,ApeRAG,Agents client
```

### Collection Specifications

| Collection | Purpose | Size | Quantization | Latency | Access Pattern |
|------------|---------|------|--------------|---------|----------------|
| `agent_memories` | Mem0 agent long-term memory | 12K vectors | int8 scalar | <15ms | Frequent R/W |
| `project_knowledge` | ApeRAG GraphRAG storage | 100K vectors | Binary | 20-30ms | Read-heavy (90%) |
| `shared_context` | Cross-agent coordination | 1K vectors | None | 5-8ms | Moderate R, Low W |

### Payload Schemas

**agent_memories**
```yaml
user_id: keyword (indexed)      # User identifier
agent_id: keyword (indexed)     # Agent identifier
timestamp: datetime (indexed)   # ISO 8601
memory_type: keyword (indexed)  # conversation | state | preference | learning
session_id: keyword             # Session grouping
project_id: keyword (indexed)   # Project context
```

**project_knowledge**
```yaml
project_id: keyword (indexed)   # Project identifier
doc_type: keyword (indexed)     # code | documentation | diagram | test
file_path: text (indexed)       # Full file path
language: keyword (indexed)     # python | javascript | yaml | etc.
git_commit: keyword             # Git SHA
timestamp: datetime (indexed)   # Last modified
entities: keyword (indexed)     # GraphRAG entities
relationships: keyword          # Entity relationships
```

**shared_context**
```yaml
context_type: keyword (indexed) # task_definition | workflow | preference | system_state
priority: integer (indexed)     # 1-10 priority
created_by_agent: keyword (indexed)
tags: keyword (indexed)         # Categorization
timestamp: datetime (indexed)
status: keyword (indexed)       # active | completed | archived
related_agents: keyword         # Agents needing this context
```

---

## Sequential Thinking Pipeline

Every query through `/v1/chat/completions` follows this pipeline:

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway :9090
    participant O as Orchestrator :8080
    participant Q as Qwen Router :8002
    participant M as Qdrant (memories)
    participant L as GPT-OSS :8000

    C->>G: POST /v1/chat/completions
    G->>O: Forward request

    O->>M: 1. Retrieve memories (user_id)
    M-->>O: Top-3 relevant memories

    O->>Q: 2. Sequential thinking (query + memories)
    Q-->>O: Reasoning thoughts

    O->>Q: 3. Route classification
    Q-->>O: simple | complex | factual

    alt complex or factual
        O->>L: 4. Generate response
        L-->>O: Response text
    else simple
        O->>Q: 4. Generate response
        Q-->>O: Response text
    end

    O->>M: 5. Store conversation
    O-->>G: Response + metadata
    G-->>C: OpenAI-format response
```

---

## API Endpoints

### Gateway API (Port 9090)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Service health + agent list |
| `/v1/models` | GET | List available agents |
| `/v1/chat/completions` | POST | Main chat endpoint (OpenAI-compatible) |

### Orchestrator API (Port 8080)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Service health + LLM status |
| `/v1/chat/completions` | POST | Primary endpoint (sequential thinking + memory) |
| `/query` | POST | Legacy query (no memory/thinking) |
| `/embed` | POST | Generate embeddings (BGE-M3) |
| `/index` | POST | Index documents to Qdrant |

---

## Constitution Framework

The project follows a structured development constitution with 8 core principles:

| Principle | Focus |
|-----------|-------|
| I. MCP-First Architecture | Use MCP servers for tooling |
| II. Test-First Development | TDD is non-negotiable |
| III. Specification-Driven | Create specs before code |
| IV. Comprehensive Planning | Plan based on complexity |
| V. Security and Quality Gates | Semgrep, tests, coverage |
| VI. Knowledge Management | Capture learnings |
| VII. Documentation Excellence | Keep docs current |
| VIII. Token-Efficient Architecture | Optimize for AI comprehension |

See: [Constitution INDEX](../src/agents/constitution/INDEX.md)

---

## Deployment Topology

```
┌──────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT ARCHITECTURE                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MacBook (Development)                                           │
│  ├── Continue.dev / OpenAI Client                               │
│  └── base_url: http://CPU_SERVER_IP:9090/v1                     │
│           │                                                      │
│           ▼                                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ CPU Server (256GB RAM, 28 threads)                      │     │
│  │ ├── Agent Gateway (:9090) ──────────────────────┐      │     │
│  │ │     FastAPI, routes to agents                  │      │     │
│  │ │                                                │      │     │
│  │ └── Qdrant (:6333) ◄─────────────────────────────┼──┐  │     │
│  │       ├── agent_memories (Mem0)                  │  │  │     │
│  │       ├── project_knowledge (ApeRAG)             │  │  │     │
│  │       └── shared_context                         │  │  │     │
│  └──────────────────────────────────────────────────┼──┼──┘     │
│                                                     │  │         │
│                                                     ▼  │         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ GPU Server - NVIDIA GB10 (128GB unified memory)         │     │
│  │ ├── GPT-OSS-120B (:8000) ◄──────────────────────────────┤     │
│  │ │     Main reasoning, 60GB MXFP4                         │     │
│  │ │                                                        │     │
│  │ ├── BGE-M3 (:8001) ◄─────────────────────────────────────┤     │
│  │ │     Embeddings, 2GB FP8, 1024-dim                      │     │
│  │ │                                                        │     │
│  │ ├── Qwen Router (:8002) ◄────────────────────────────────┤     │
│  │ │     Classification, 3GB FP8, 1.5B params               │     │
│  │ │                                                        │     │
│  │ └── Orchestrator (:8080) ────────────────────────────────┘     │
│  │       FastAPI, query routing, RAG pipeline                     │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Memory Layout (GB10)

| Component | Memory | Notes |
|-----------|--------|-------|
| GPT-OSS-120B | ~60GB | MXFP4 quantization |
| BGE-M3 | ~2GB | FP8 quantization |
| Qwen Router | ~3GB | FP8 quantization |
| Orchestrator | ~2GB | Python runtime |
| **Subtotal** | ~67GB | |
| KV Cache (Free) | ~61GB | Available for inference |
| **Total** | 128GB | |

---

## Network Configuration

| Server | Service | Port | Protocol |
|--------|---------|------|----------|
| GPU (GB10) | GPT-OSS-120B | 8000 | HTTP |
| GPU (GB10) | BGE-M3 | 8001 | HTTP |
| GPU (GB10) | Qwen Router | 8002 | HTTP |
| GPU (GB10) | Orchestrator | 8080 | HTTP |
| CPU | Qdrant REST | 6333 | HTTP |
| CPU | Qdrant gRPC | 6334 | gRPC |
| CPU | Agent Gateway | 9090 | HTTP |

---

## Related Documentation

- [CLAUDE.md](../CLAUDE.md) - Development guidelines and API contracts
- [Constitution INDEX](../src/agents/constitution/INDEX.md) - Development principles
- [Docker Compose (Qdrant)](../docker-compose-qdrant.yaml) - Qdrant deployment
- [Collection Configs](../collections/) - Qdrant collection schemas
