"""
Agent Context - Build context and messages for agent execution.

Single Responsibility: Construct LLM messages with memory and context.
"""

from typing import List, Dict, Optional, TYPE_CHECKING

from src.agents.logging_config import get_logger, LogEvent

if TYPE_CHECKING:
    from src.agents.agents.base import BaseAgent
    from src.agents.memory.client import MemoryClient

logger = get_logger("agents.context")


async def retrieve_memories(
    agent: "BaseAgent",
    user_message: str,
    memory_client: Optional["MemoryClient"],
    user_id: Optional[str]
) -> List[str]:
    """
    Retrieve relevant memories for an agent execution.

    Args:
        agent: The agent being executed
        user_message: The user's message to search for relevant memories
        memory_client: Optional memory client for retrieval
        user_id: User ID for memory isolation

    Returns:
        List of relevant memory strings, or empty list if unavailable
    """
    if not memory_client or not user_id:
        return []

    try:
        logger.info(
            LogEvent.MEMORY_RETRIEVING,
            extra={
                "agent_id": agent.id,
                "user_id": user_id,
                "query_preview": user_message[:100] if user_message else ""
            }
        )
        memories = await memory_client.retrieve_memories(
            query=user_message,
            user_id=user_id
        )
        logger.info(
            LogEvent.MEMORY_RETRIEVED,
            extra={
                "agent_id": agent.id,
                "user_id": user_id,
                "memory_count": len(memories),
                "total_chars": sum(len(m) for m in memories)
            }
        )
        return memories
    except Exception as e:
        logger.warning(
            LogEvent.MEMORY_ERROR,
            extra={
                "agent_id": agent.id,
                "user_id": user_id,
                "error": str(e),
                "error_type": type(e).__name__,
                "operation": "retrieve"
            }
        )
        return []


def build_messages(
    system_prompt: str,
    memory_context: List[str],
    context: Optional[str],
    conversation_history: Optional[List[Dict[str, str]]],
    user_message: str
) -> List[Dict[str, str]]:
    """
    Build the messages list for an LLM call.

    Args:
        system_prompt: The agent's system prompt
        memory_context: List of relevant memories
        context: Optional context from previous agents
        conversation_history: Optional conversation history
        user_message: The user's current message

    Returns:
        List of messages in OpenAI format
    """
    messages = []

    # Build combined system prompt
    system_parts = [system_prompt]

    # Add memory context if available
    if memory_context:
        memory_str = "\n".join(f"- {mem}" for mem in memory_context)
        system_parts.append(f"## Relevant Memories\n{memory_str}")

    # Add context from previous agents
    if context:
        system_parts.append(f"## Context from Previous Agents\n{context}")

    messages.append({"role": "system", "content": "\n\n".join(system_parts)})

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)

    # Add the current user message
    messages.append({"role": "user", "content": user_message})

    return messages


__all__ = ["retrieve_memories", "build_messages"]
