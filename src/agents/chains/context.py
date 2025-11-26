"""
Chain Context - Data structures for chain execution state.

Single Responsibility: Define context passed between agents in a chain.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from src.agents.agents.base import BaseAgent


@dataclass
class ChainContext:
    """
    Context passed between agents during chain execution.

    Attributes:
        user_message: Original user request
        conversation_history: Prior messages in session
        memory_context: Retrieved relevant memories from vector store
        agent_outputs: Map of agent_id to their output
        current_agent: Currently executing agent id
        chain_id: Which chain is running
        error: Error message if chain execution failed (None if successful)
        failed_agent: ID of the agent that failed (None if successful)
    """

    user_message: str
    conversation_history: List[Dict[str, str]]
    memory_context: List[str]
    agent_outputs: Dict[str, str]
    current_agent: str
    chain_id: str
    error: Optional[str] = field(default=None)
    failed_agent: Optional[str] = field(default=None)


def build_agent_context(
    context: ChainContext,
    agent: BaseAgent
) -> str:
    """
    Build the context string to pass to an agent.

    Includes user message, memory context, and previous agent outputs.

    Args:
        context: The current chain context
        agent: The agent that will receive this context

    Returns:
        Formatted context string for the agent
    """
    parts = []

    # Add user message
    parts.append(f"## User Request\n{context.user_message}")

    # Add memory context if available
    if context.memory_context:
        memory_str = "\n".join(f"- {mem}" for mem in context.memory_context)
        parts.append(f"## Relevant Context\n{memory_str}")

    # Add previous agent outputs
    if context.agent_outputs:
        outputs_parts = []
        for agent_id, output in context.agent_outputs.items():
            outputs_parts.append(f"### {agent_id}\n{output}")
        parts.append(f"## Previous Agent Outputs\n" + "\n\n".join(outputs_parts))

    return "\n\n".join(parts)


__all__ = ["ChainContext", "build_agent_context"]
