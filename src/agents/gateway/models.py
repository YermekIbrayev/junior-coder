"""
Gateway Models - Pydantic request/response models.

Single Responsibility: Data validation and serialization.
"""

from pydantic import BaseModel
from typing import Optional, Any, Union


class Message(BaseModel):
    """Chat message in OpenAI format."""
    role: str
    content: Optional[str] = None
    tool_calls: Optional[list[dict]] = None
    tool_call_id: Optional[str] = None


class ToolFunction(BaseModel):
    """Function definition for a tool."""
    name: str
    description: Optional[str] = None
    parameters: Optional[dict[str, Any]] = None


class Tool(BaseModel):
    """Tool definition in OpenAI format."""
    type: str = "function"
    function: ToolFunction


class ChatRequest(BaseModel):
    """OpenAI-compatible chat completion request."""
    model: str = "orchestrator"
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False
    user: Optional[str] = None
    tools: Optional[list[Tool]] = None
    tool_choice: Optional[Union[str, dict]] = None


class ChatResponse(BaseModel):
    """OpenAI-compatible chat completion response."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list
    usage: dict


__all__ = ["Message", "ToolFunction", "Tool", "ChatRequest", "ChatResponse"]
