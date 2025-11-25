"""
Generic LLM client for OpenAI-compatible APIs
Handles communication with GPT-OSS-120B and Qwen2.5-1.5B
"""
import httpx
from typing import List, Dict, Optional
from core.config import settings
from core.logger import get_logger
import time

logger = get_logger(__name__)

# Global HTTP client (initialized in main.py lifespan)
http_client: Optional[httpx.AsyncClient] = None

async def init_clients():
    """Initialize HTTP client with connection pooling"""
    global http_client
    logger.debug("Initializing HTTP client...")
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(settings.LLM_TIMEOUT),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    )
    logger.info(f"✓ HTTP client initialized (connection pool: 100 max, 20 keepalive, timeout: {settings.LLM_TIMEOUT}s)")

async def cleanup_clients():
    """Close HTTP client"""
    global http_client
    if http_client:
        await http_client.aclose()

async def call_llm(
    url: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 1024,
    temperature: float = 0.7
) -> str:
    """
    Call an OpenAI-compatible LLM endpoint

    Args:
        url: Base URL of the LLM service
        messages: List of message dicts with 'role' and 'content'
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature

    Returns:
        Generated text response

    Raises:
        httpx.HTTPError: If request fails
    """
    if not http_client:
        error_msg = (
            "HTTP client not initialized. "
            "This usually means the FastAPI lifespan startup hasn't completed yet. "
            "Please wait a few seconds and try again."
        )
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    endpoint = f"{url}/v1/chat/completions"
    logger.debug(f"Calling LLM: url={endpoint}, messages={len(messages)}, max_tokens={max_tokens}, temp={temperature}")

    start_time = time.time()
    try:
        response = await http_client.post(
            endpoint,
            json={
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        latency_ms = (time.time() - start_time) * 1000

        logger.info(f"✓ LLM call successful: url={url}, latency={latency_ms:.1f}ms, response_length={len(content)}")
        return content

    except httpx.TimeoutException as e:
        logger.error(f"❌ LLM call timeout: url={url}, timeout={settings.LLM_TIMEOUT}s, error={e}")
        raise
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ LLM call HTTP error: url={url}, status={e.response.status_code}, response={e.response.text[:500]}")
        raise
    except httpx.RequestError as e:
        logger.error(f"❌ LLM call request error: url={url}, error={e}")
        raise
    except Exception as e:
        logger.error(f"❌ LLM call unexpected error: url={url}, error={e}", exc_info=True)
        raise
