"""
Pydantic models for API request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class QueryRequest(BaseModel):
    """Request model for /query endpoint"""
    query: str = Field(..., description="User query to process")
    max_tokens: int = Field(1024, description="Maximum tokens in response")
    use_rag: Optional[bool] = Field(None, description="Force RAG on/off (None=auto)")
    top_k: int = Field(5, description="Number of context chunks to retrieve")

class QueryResponse(BaseModel):
    """Response model for /query endpoint"""
    response: str = Field(..., description="Generated response")
    model_used: str = Field(..., description="Which model generated the response")
    rag_used: bool = Field(..., description="Whether RAG was used")
    context_chunks: int = Field(0, description="Number of context chunks used")
    latency_ms: float = Field(..., description="Total latency in milliseconds")
    route_decision: str = Field(..., description="Router classification result")

class EmbeddingRequest(BaseModel):
    """Request model for /embed endpoint"""
    texts: List[str] = Field(..., description="List of texts to embed")

class EmbeddingResponse(BaseModel):
    """Response model for /embed endpoint"""
    embeddings: List[List[float]] = Field(..., description="List of embedding vectors")
    dimension: int = Field(..., description="Embedding dimension")
    count: int = Field(..., description="Number of embeddings")

class IndexRequest(BaseModel):
    """Request model for /index endpoint"""
    documents: List[str] = Field(..., description="Documents to index")
    metadata: Optional[List[dict]] = Field(None, description="Optional metadata per document")

class IndexResponse(BaseModel):
    """Response model for /index endpoint"""
    indexed_count: int = Field(..., description="Number of documents indexed")
    collection: str = Field(..., description="Qdrant collection name")
    latency_ms: float = Field(..., description="Indexing latency")
