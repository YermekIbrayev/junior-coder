"""
BaseChain - Foundation class for agent workflow chains.

Provides common functionality for sequential agent execution.
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from src.agents.agents.base import BaseAgent
from src.agents.agents.runner import run_agent
from src.agents.logging_config import get_logger, LogEvent

# Module logger with structured logging
logger = get_logger("chains.base")


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


@dataclass
class BaseChain:
    """
    Base class for all agent chains in the orchestration system.

    Attributes:
        id: Chain identifier (e.g., "sdd", "tdd", "retro")
        name: Human-readable name (e.g., "Specification-Driven Development")
        agents: Ordered list of agents to execute
        description: Brief description of what this chain handles
    """

    id: str
    name: str
    agents: List[BaseAgent]
    description: str = field(default="")

    async def execute(
        self,
        context: ChainContext,
        http_client=None
    ) -> ChainContext:
        """
        Execute the chain by running each agent in sequence.

        Each agent receives:
        - The original user message
        - Memory context (if available)
        - Outputs from all previous agents in the chain

        On agent failure:
        - Returns partial results from successful agents
        - Sets error and failed_agent fields in context
        - Does NOT raise exception

        Args:
            context: The chain execution context
            http_client: HTTP client for LLM calls

        Returns:
            Updated ChainContext with all agent outputs (partial on failure)
        """
        chain_start_time = time.time()
        agent_ids = [a.id for a in self.agents]

        logger.info(
            LogEvent.CHAIN_STARTING,
            extra={
                "chain_id": self.id,
                "chain_name": self.name,
                "agent_count": len(self.agents),
                "agents": agent_ids,
                "message_preview": context.user_message[:100] if context.user_message else ""
            }
        )

        for i, agent in enumerate(self.agents):
            # Update current agent
            context.current_agent = agent.id
            agent_start_time = time.time()

            logger.info(
                LogEvent.AGENT_STARTING,
                extra={
                    "chain_id": self.id,
                    "agent_id": agent.id,
                    "agent_index": i + 1,
                    "agent_total": len(self.agents),
                    "previous_outputs": list(context.agent_outputs.keys())
                }
            )

            # Build context string for this agent
            agent_context = build_agent_context(context, agent)

            try:
                # Run the agent
                output = await run_agent(
                    agent=agent,
                    context=agent_context,
                    user_message=context.user_message,
                    conversation_history=context.conversation_history,
                    http_client=http_client
                )

                # Store the output
                context.agent_outputs[agent.id] = output
                agent_duration_ms = (time.time() - agent_start_time) * 1000

                logger.info(
                    LogEvent.AGENT_COMPLETED,
                    extra={
                        "chain_id": self.id,
                        "agent_id": agent.id,
                        "agent_index": i + 1,
                        "duration_ms": round(agent_duration_ms, 2),
                        "output_length": len(output),
                        "output_preview": output[:200] + "..." if len(output) > 200 else output
                    }
                )

            except Exception as e:
                # Handle agent failure - return partial results
                context.error = str(e)
                context.failed_agent = agent.id
                agent_duration_ms = (time.time() - agent_start_time) * 1000
                chain_duration_ms = (time.time() - chain_start_time) * 1000

                logger.error(
                    LogEvent.AGENT_FAILED,
                    extra={
                        "chain_id": self.id,
                        "agent_id": agent.id,
                        "agent_index": i + 1,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "duration_ms": round(agent_duration_ms, 2),
                        "partial_outputs": list(context.agent_outputs.keys())
                    },
                    exc_info=True
                )

                logger.warning(
                    LogEvent.CHAIN_FAILED,
                    extra={
                        "chain_id": self.id,
                        "failed_agent": agent.id,
                        "completed_agents": list(context.agent_outputs.keys()),
                        "duration_ms": round(chain_duration_ms, 2),
                        "error": str(e)
                    }
                )
                return context

        chain_duration_ms = (time.time() - chain_start_time) * 1000
        logger.info(
            LogEvent.CHAIN_COMPLETED,
            extra={
                "chain_id": self.id,
                "chain_name": self.name,
                "agent_count": len(self.agents),
                "duration_ms": round(chain_duration_ms, 2),
                "total_output_length": sum(len(o) for o in context.agent_outputs.values())
            }
        )
        return context
