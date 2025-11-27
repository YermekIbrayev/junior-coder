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


async def generate_tool_stream_response(
    llm_message: dict,
    model: str,
    completion_id: str
) -> AsyncGenerator[str, None]:
    """
    Generate SSE stream for tool-enabled responses.

    Handles both content-only and tool_calls responses.

    Args:
        llm_message: LLM response dict with 'content' and/or 'tool_calls'
        model: Model name for chunk metadata
        completion_id: Unique completion ID

    Yields:
        SSE-formatted chunks
    """
    content = llm_message.get("content", "")
    tool_calls = llm_message.get("tool_calls")

    # First chunk: role announcement
    first_chunk = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {"role": "assistant"},
            "finish_reason": None
        }]
    }
    yield f"data: {json.dumps(first_chunk)}\n\n"

    # Stream content if present
    if content:
        words = content.split(' ')
        for i, word in enumerate(words):
            word_content = word if i == 0 else ' ' + word
            chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "delta": {"content": word_content},
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(chunk)}\n\n"

    # Stream tool_calls if present
    if tool_calls:
        for tc in tool_calls:
            chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "delta": {"tool_calls": [tc]},
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(chunk)}\n\n"

    # Final chunk
    finish_reason = "tool_calls" if tool_calls else "stop"
    final_chunk = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": finish_reason
        }]
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"
    yield "data: [DONE]\n\n"


__all__ = ["generate_stream_response", "generate_tool_stream_response"]
