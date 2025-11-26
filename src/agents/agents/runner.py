"""
AgentRunner - Executes agents by loading prompts and calling the LLM.

Handles communication with the GB10 LLM service.
"""

import time
from typing import List, Dict, Optional, TYPE_CHECKING
from src.agents.agents.base import BaseAgent
from src.agents.logging_config import get_logger, LogEvent

if TYPE_CHECKING:
    from src.agents.memory.client import MemoryClient

# Module logger with structured logging
logger = get_logger("agents.runner")

# Configuration constants
LLM_BASE_URL = "http://192.168.51.22:8080"
DEFAULT_MODEL = "gpt-oss"  # Default model for agent execution
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
LLM_TIMEOUT = 120.0  # seconds


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

        Raises:
            Exception: If the LLM service is unavailable or returns an error
        """
        if self._http_client is None:
            raise RuntimeError("HTTP client not initialized")

        url = f"{LLM_BASE_URL}/v1/chat/completions"

        payload = {
            "model": DEFAULT_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Calculate approximate prompt size
        prompt_chars = sum(len(m.get("content", "")) for m in messages)

        start_time = time.time()
        logger.info(
            LogEvent.LLM_CALLING,
            extra={
                "url": url,
                "model": DEFAULT_MODEL,
                "message_count": len(messages),
                "prompt_chars": prompt_chars,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )

        try:
            response = await self._http_client.post(
                url,
                json=payload,
                timeout=LLM_TIMEOUT
            )
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"]
            duration_ms = (time.time() - start_time) * 1000

            # Extract usage if available
            usage = data.get("usage", {})

            logger.info(
                LogEvent.LLM_RESPONSE,
                extra={
                    "model": DEFAULT_MODEL,
                    "duration_ms": round(duration_ms, 2),
                    "response_length": len(content),
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                    "response_preview": content[:200] + "..." if len(content) > 200 else content
                }
            )

            return content

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                LogEvent.LLM_ERROR,
                extra={
                    "url": url,
                    "model": DEFAULT_MODEL,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_ms": round(duration_ms, 2)
                },
                exc_info=True
            )
            raise

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

        Loads the agent's prompt, constructs the message list,
        and calls the LLM to get a response.

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
        # Load the agent's prompt
        system_prompt = agent.load_prompt()

        # Retrieve memories if memory_client is provided
        memory_context = []
        if memory_client and user_id:
            try:
                logger.info(
                    LogEvent.MEMORY_RETRIEVING,
                    extra={
                        "agent_id": agent.id,
                        "user_id": user_id,
                        "query_preview": user_message[:100] if user_message else ""
                    }
                )
                memory_context = await memory_client.retrieve_memories(
                    query=user_message,
                    user_id=user_id
                )
                logger.info(
                    LogEvent.MEMORY_RETRIEVED,
                    extra={
                        "agent_id": agent.id,
                        "user_id": user_id,
                        "memory_count": len(memory_context),
                        "total_chars": sum(len(m) for m in memory_context)
                    }
                )
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
                memory_context = []

        # Build messages list
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

        # Call the LLM
        return await self.call_llm(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )


# Module-level function for convenience
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

    Args:
        agent: The agent to run
        context: Context string (from previous agents, memory, etc.)
        user_message: The user's input message
        conversation_history: Optional list of previous messages
        http_client: HTTP client for LLM calls
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        memory_client: Optional memory client for retrieving past conversations
        user_id: Optional user ID for memory isolation

    Returns:
        The agent's response as a string
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
