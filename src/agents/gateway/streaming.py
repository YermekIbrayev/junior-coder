"""
Streaming Helpers - Server-Sent Events (SSE) streaming.

Single Responsibility: OpenAI-compatible streaming response generation.
"""

import json
import time
from typing import AsyncGenerator


async def generate_stream_response(
    response_text: str,
    model: str,
    completion_id: str
) -> AsyncGenerator[str, None]:
    """
    Generate SSE stream chunks for OpenAI-compatible streaming.

    OpenAI streaming format:
    1. First chunk: delta contains {"role": "assistant"}
    2. Content chunks: delta contains {"content": "..."}
    3. Final chunk: delta is {}, finish_reason is "stop"
    4. Stream ends with "data: [DONE]"

    Args:
        response_text: Full response to stream
        model: Model name for chunk metadata
        completion_id: Unique completion ID

    Yields:
        SSE-formatted chunks
    """
    # First chunk: role announcement (required by OpenAI spec)
    first_chunk = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {"role": "assistant", "content": ""},
            "finish_reason": None
        }]
    }
    yield f"data: {json.dumps(first_chunk)}\n\n"

    # Content chunks: stream word by word
    words = response_text.split(' ')
    for i, word in enumerate(words):
        content = word if i == 0 else ' ' + word
        chunk = {
            "id": completion_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "index": 0,
                "delta": {"content": content},
                "finish_reason": None
            }]
        }
        yield f"data: {json.dumps(chunk)}\n\n"

    # Final chunk: finish_reason
    final_chunk = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


__all__ = ["generate_stream_response"]
