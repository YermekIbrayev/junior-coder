"""
FastAPI Orchestrator for Multi-Model LLM System
Entry point that coordinates routing, embedding, and query processing
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api import routes
from core.config import settings
from core.logger import setup_logging, get_logger
from services.llm_client import init_clients, cleanup_clients
from services.mem0_client import Mem0Client

# Setup logging first
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    logger.info("🚀 Starting orchestrator initialization...")

    try:
        # Startup: Initialize HTTP clients
        logger.debug("Initializing HTTP clients...")
        await init_clients()
        logger.info("✓ HTTP clients initialized successfully")

        # Initialize Mem0 memory client
        logger.debug(f"Initializing Mem0 client (Qdrant: {settings.QDRANT_URL}, Collection: {settings.QDRANT_COLLECTION_MEMORIES})")
        routes.mem0_client = Mem0Client(
            qdrant_url=settings.QDRANT_URL,
            embedding_url=settings.BGE_M3_URL,
            collection_name=settings.QDRANT_COLLECTION_MEMORIES
        )
        logger.info(f"✓ Mem0 memory client initialized (collection: {settings.QDRANT_COLLECTION_MEMORIES})")
        logger.info("✅ Orchestrator ready to handle requests")

    except Exception as e:
        logger.error(f"❌ Failed to initialize orchestrator: {e}", exc_info=True)
        raise

    yield

    # Shutdown: Close HTTP clients
    logger.info("🛑 Shutting down orchestrator...")
    try:
        await cleanup_clients()
        if routes.mem0_client and hasattr(routes.mem0_client, 'http_client'):
            await routes.mem0_client.http_client.aclose()
        logger.info("✓ Shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)

# Create FastAPI app
app = FastAPI(
    title="LLM Orchestrator API",
    description="Multi-model LLM system with intelligent routing and RAG",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes.router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    health_status = {
        "status": "healthy",
        "services": {
            "gpt_oss": settings.GPT_OSS_URL,
            "bge_m3": settings.BGE_M3_URL,
            "qwen_router": settings.QWEN_ROUTER_URL,
            "qdrant": settings.QDRANT_URL
        }
    }
    logger.debug(f"Health check response: {health_status}")
    return health_status

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "LLM Orchestrator API",
        "docs": "/docs",
        "health": "/health"
    }
