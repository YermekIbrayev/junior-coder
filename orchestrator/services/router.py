"""
Query routing service using Qwen2.5-1.5B
Classifies queries as: simple, complex, or factual
"""
from services.llm_client import call_llm
from core.config import settings

ROUTER_SYSTEM_PROMPT = """You are a query classifier. Classify each query into exactly ONE category:

- "simple": General knowledge, greetings, simple questions (can be answered by a 1.5B model)
- "complex": Reasoning, math, code, analysis (needs 120B model)
- "factual": Specific facts, dates, entities (needs RAG + 120B model)

Respond with ONLY the category word. No explanation."""

async def route_query(query: str) -> str:
    """
    Classify query complexity using Qwen2.5-1.5B

    Args:
        query: User query string

    Returns:
        Classification: "simple", "complex", or "factual"

    Raises:
        Exception: If routing fails
    """
    messages = [
        {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]

    try:
        result = await call_llm(
            url=settings.QWEN_ROUTER_URL,
            messages=messages,
            max_tokens=10,
            temperature=0.0  # Deterministic classification
        )

        # Parse result (should be single word)
        classification = result.strip().lower()

        # Validate classification
        if classification not in ["simple", "complex", "factual"]:
            # Default to complex if unclear
            return "complex"

        return classification

    except Exception as e:
        # On error, default to complex (safer)
        print(f"Router error: {e}")
        return "complex"
