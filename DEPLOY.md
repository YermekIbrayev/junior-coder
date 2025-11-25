# GB10 Server Deployment Guide

**Server Role**: GPU Server (LLM Models + Orchestrator API)
**Hardware**: NVIDIA GB10 (sm_121) with 128GB unified memory

---

## 📦 What's Included

- `docker-compose.yml` - Multi-container setup for all LLM services
- `gpt-oss-120b-latency.yaml` - GPT-OSS-120B config (low latency)
- `gpt-oss-120b-throughput.yaml` - GPT-OSS-120B config (high throughput)
- `bge-m3-embedding.yaml` - BGE-M3 embedding model config
- `qwen-router.yaml` - Qwen2.5-1.5B router config
- `.env.example` - Environment variables template
- `start_all.sh` - Automated startup script
- `orchestrator/` - FastAPI orchestrator with Mem0 + ApeRAG

---

## 🚀 Quick Deployment

### Step 1: Copy Files to GB10 Server

```bash
# From your MacBook, copy entire folder to GB10
scp -r gb10-server/ user@GB10_IP:/opt/vision_model/
```

### Step 2: Setup Environment on GB10

```bash
# SSH into GB10 server
ssh user@GB10_IP

# Navigate to deployment folder
cd /opt/vision_model

# Set Qdrant URL to CPU server
export QDRANT_URL=http://CPU_SERVER_IP:6333

# Or edit .env file
cp .env.example .env
nano .env  # Set QDRANT_URL=http://CPU_SERVER_IP:6333
```

### Step 3: Start All Services

```bash
# Run deployment script
./start_all.sh

# Or manually with docker-compose
docker-compose up -d
```

### Step 4: Verify Services

```bash
# Check all containers are running
docker-compose ps

# Check health
curl http://localhost:8080/health

# View logs
docker-compose logs -f orchestrator
```

---

## 🎯 Services Running

| Service | Port | Purpose | Memory |
|---------|------|---------|--------|
| GPT-OSS-120B | 8000 | Main reasoning | 60GB |
| BGE-M3 | 8001 | Embeddings | 2GB |
| Qwen Router | 8002 | Query routing | 3GB |
| Orchestrator | 8080 | API gateway | 2GB |

**Total Memory Used**: 67GB
**Free for KV Cache**: 61GB (20% more than single-server!)

---

## 🔧 Configuration

### Switch Between Latency/Throughput Modes

**Latency Mode** (default, <100ms response):
```bash
# In docker-compose.yml, GPT-OSS uses:
volumes:
  - ./gpt-oss-120b-latency.yaml:/config/model.yaml:ro
```

**Throughput Mode** (1000+ concurrent users):
```bash
# Change to:
volumes:
  - ./gpt-oss-120b-throughput.yaml:/config/model.yaml:ro

# Restart
docker-compose restart gpt-oss
```

### Update Qdrant URL

Edit `.env` file:
```bash
QDRANT_URL=http://192.168.1.100:6333  # Replace with actual CPU server IP
```

Restart orchestrator:
```bash
docker-compose restart orchestrator
```

---

## 🧪 Testing

### Test Individual Models

```bash
# Test GPT-OSS
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-oss", "messages": [{"role": "user", "content": "Hello"}]}'

# Test BGE-M3
curl http://localhost:8001/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"input": "test", "model": "BAAI/bge-m3"}'

# Test Qwen Router
curl http://localhost:8002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen", "messages": [{"role": "user", "content": "Hi"}]}'
```

### Test Orchestrator

```bash
# Simple query (should use Qwen)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, how are you?"}'

# Complex query (should use GPT-OSS + RAG)
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain the architecture of this system"}'
```

---

## 🛠️ Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs <service_name>

# Common issues:
# 1. GPU not detected: nvidia-smi
# 2. Port conflict: Change ports in docker-compose.yml
# 3. Out of memory: Use latency mode instead of throughput
```

### Can't connect to Qdrant on CPU server
```bash
# Verify network connectivity
ping CPU_SERVER_IP

# Verify Qdrant is running on CPU server
curl http://CPU_SERVER_IP:6333/health

# Check QDRANT_URL in .env
cat .env | grep QDRANT_URL
```

### Slow responses
```bash
# Check GPU utilization
nvidia-smi

# Switch to latency mode if using throughput mode
# Edit docker-compose.yml and change model config
```

---

## 📊 Monitoring

### GPU Usage
```bash
watch -n 1 nvidia-smi
```

### Container Stats
```bash
docker stats
```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f gpt-oss
docker-compose logs -f orchestrator
```

---

## 🔄 Stopping/Restarting

```bash
# Stop all services
docker-compose down

# Restart specific service
docker-compose restart orchestrator

# Restart all
docker-compose restart
```

---

## 📁 File Structure

```
gb10-server/
├── docker-compose.yml          # Main compose file
├── gpt-oss-120b-latency.yaml  # GPT-OSS config (latency)
├── gpt-oss-120b-throughput.yaml  # GPT-OSS config (throughput)
├── bge-m3-embedding.yaml       # BGE-M3 config
├── qwen-router.yaml            # Qwen router config
├── .env.example                # Environment template
├── start_all.sh                # Startup script
├── orchestrator/               # FastAPI app
│   ├── main.py
│   ├── api/
│   ├── services/
│   │   ├── mem0_client.py
│   │   ├── aperag_client.py
│   │   └── ...
│   ├── tests/
│   └── requirements.txt
└── DEPLOY.md                   # This file
```

---

## 🎉 Next Steps

1. ✅ GB10 services deployed
2. Ensure CPU server is running (see `../cpu-server/DEPLOY.md`)
3. Test from MacBook (see `../macbook-client/CONNECT.md`)

**Your GB10 server is ready!** 🚀
