"""
BaseChain - Foundation class for agent workflow chains.

Provides common functionality for sequential agent execution.
"""

import time
from dataclasses import dataclass, field
from typing import List

from src.agents.agents.base import BaseAgent
from src.agents.agents.runner import run_agent
from src.agents.chains.context import ChainContext, build_agent_context
from src.agents.logging_config import get_logger, LogEvent

logger = get_logger("chains.base")


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
            result = await self._execute_agent(
                context, agent, i, chain_start_time, http_client
            )
            if result is not None:
                # Agent failed, return partial results
                return result

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

    async def _execute_agent(
        self,
        context: ChainContext,
        agent: BaseAgent,
        index: int,
        chain_start_time: float,
        http_client
    ) -> ChainContext | None:
        """
        Execute a single agent in the chain.

        Returns None on success, or the context with error info on failure.
        """
        context.current_agent = agent.id
        agent_start_time = time.time()

        logger.info(
            LogEvent.AGENT_STARTING,
            extra={
                "chain_id": self.id,
                "agent_id": agent.id,
                "agent_index": index + 1,
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
                    "agent_index": index + 1,
                    "duration_ms": round(agent_duration_ms, 2),
                    "output_length": len(output),
                    "output_preview": output[:200] + "..." if len(output) > 200 else output
                }
            )
            return None  # Success

        except Exception as e:
            return self._handle_agent_failure(
                context, agent, index, e, agent_start_time, chain_start_time
            )

    def _handle_agent_failure(
        self,
        context: ChainContext,
        agent: BaseAgent,
        index: int,
        error: Exception,
        agent_start_time: float,
        chain_start_time: float
    ) -> ChainContext:
        """Handle agent failure and return context with error info."""
        context.error = str(error)
        context.failed_agent = agent.id
        agent_duration_ms = (time.time() - agent_start_time) * 1000
        chain_duration_ms = (time.time() - chain_start_time) * 1000

        logger.error(
            LogEvent.AGENT_FAILED,
            extra={
                "chain_id": self.id,
                "agent_id": agent.id,
                "agent_index": index + 1,
                "error": str(error),
                "error_type": type(error).__name__,
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
                "error": str(error)
            }
        )
        return context

# Re-export for backward compatibility
__all__ = ["BaseChain", "ChainContext", "build_agent_context"]
