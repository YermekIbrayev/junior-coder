"""
Sequential Thinking Service
Provides chain-of-thought reasoning before query processing

Uses Qwen router model for lightweight reasoning that enriches context
"""
from services.llm_client import call_llm
from core.config import settings
from typing import Dict, List

THINKING_SYSTEM_PROMPT = """You are a reasoning assistant. For each query, break down your thinking into clear steps.
Analyze what the user is asking and structure your thoughts to help with:
1. Understanding the query intent
2. Identifying key concepts
3. Planning the approach to answer

Keep your reasoning concise and focused. Output your thoughts as numbered steps."""


async def perform_sequential_thinking(query: str, context: str = "") -> Dict[str, any]:
    """
    Perform chain-of-thought reasoning on query

    Args:
        query: User query string
        context: Optional context from memory or RAG

    Returns:
        {
            "thoughts": "Step-by-step reasoning",
            "enriched_query": "Original query with thinking context"
        }
    """
    # Build prompt with context if available
    prompt = query
    if context:
        prompt = f"Context from memory:\n{context}\n\nUser query: {query}"

    messages = [
        {"role": "system", "content": THINKING_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    try:
        # Use Qwen router for fast reasoning
        thoughts = await call_llm(
            url=settings.QWEN_ROUTER_URL,
            messages=messages,
            max_tokens=256,
            temperature=0.3  # Low temperature for focused thinking
        )

        # Enrich query with thinking context
        enriched_query = f"[Reasoning: {thoughts.strip()}]\n\nQuery: {query}"

        return {
            "thoughts": thoughts.strip(),
            "enriched_query": enriched_query
        }

    except Exception as e:
        print(f"Sequential thinking error: {e}")
        # Fallback: return original query
        return {
            "thoughts": "",
            "enriched_query": query
        }
