"""
AgentRunner - Executes agents by loading prompts and calling the LLM.

Handles agent execution with memory integration.
"""

from typing import List, Dict, Optional, TYPE_CHECKING

from src.agents.agents.base import BaseAgent
from src.agents.agents.config import DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
from src.agents.agents.llm import call_llm
from src.agents.agents.context import retrieve_memories, build_messages

if TYPE_CHECKING:
    from src.agents.memory.client import MemoryClient

# Re-export config for backward compatibility
from src.agents.agents.config import LLM_BASE_URL, LLM_TIMEOUT  # noqa: F401


class AgentRunner:
    """
    Executes agents by loading their prompts and calling the LLM service.

    Attributes:
        http_client: Async HTTP client for LLM calls (injected for testing)
    """

    def __init__(self, http_client=None):
        """
        Initialize the AgentRunner.

        Args:
            http_client: Optional httpx.AsyncClient for LLM calls.
                        If None, calls will fail (requires injection).
        """
        self._http_client = http_client

    async def call_llm(
        self,
        messages: List[Dict[str, str]],
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS
    ) -> str:
        """
        Call the LLM service with the given messages.

        Args:
            messages: List of chat messages in OpenAI format
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate

        Returns:
            The assistant's response content as a string
        """
        message = await call_llm(
            http_client=self._http_client,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return message.get("content", "")

    async def run_agent(
        self,
        agent: BaseAgent,
        user_message: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        memory_client: Optional["MemoryClient"] = None,
        user_id: Optional[str] = None
    ) -> str:
        """
        Run an agent with the given user message.

        Args:
            agent: The agent to run
            user_message: The user's input message
            context: Optional context from previous agents in the chain
            conversation_history: Optional list of previous messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            memory_client: Optional memory client for retrieving past conversations
            user_id: Optional user ID for memory isolation

        Returns:
            The agent's response as a string
        """
        system_prompt = agent.load_prompt()

        memory_context = await retrieve_memories(
            agent, user_message, memory_client, user_id
        )

        messages = build_messages(
            system_prompt, memory_context, context, conversation_history, user_message
        )

        return await self.call_llm(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )


async def run_agent(
    agent: BaseAgent,
    context: str,
    user_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    http_client=None,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    memory_client: Optional["MemoryClient"] = None,
    user_id: Optional[str] = None
) -> str:
    """
    Run an agent with the given context and message.

    This is a convenience function that creates an AgentRunner instance
    and runs the agent. For multiple agent calls, use AgentRunner directly.
    """
    runner = AgentRunner(http_client=http_client)
    return await runner.run_agent(
        agent=agent,
        user_message=user_message,
        context=context,
        conversation_history=conversation_history,
        temperature=temperature,
        max_tokens=max_tokens,
        memory_client=memory_client,
        user_id=user_id
    )


__all__ = ["AgentRunner", "run_agent", "LLM_BASE_URL", "LLM_TIMEOUT"]
