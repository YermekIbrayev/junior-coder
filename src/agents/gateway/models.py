"""
Gateway Models - Pydantic request/response models.

Single Responsibility: Data validation and serialization.
"""

from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    """Chat message in OpenAI format."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """OpenAI-compatible chat completion request."""
    model: str = "orchestrator"
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False
    user: Optional[str] = None


class ChatResponse(BaseModel):
    """OpenAI-compatible chat completion response."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list
    usage: dict


__all__ = ["Message", "ChatRequest", "ChatResponse"]
