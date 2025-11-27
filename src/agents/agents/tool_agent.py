"""
ToolAgent - Agent with tool calling capabilities.

Provides:
- ToolAgent: BaseAgent subclass with tools field
- ToolAgentRunner: Executes agents with tool execution loop
- IndexerAgent: Pre-configured agent for codebase indexing
- default_tool_executor: Default tool dispatcher

Architecture:
    ToolAgent --extends--> BaseAgent
    ToolAgentRunner --uses--> call_llm (with tools)
    IndexerAgent --is-a--> ToolAgent (with INDEXER_TOOLS)
"""

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Awaitable

from src.agents.agents.base import BaseAgent
from src.agents.agents.llm import call_llm


@dataclass
class ToolAgent(BaseAgent):
    """
    Agent that can use tools for function calling.

    Extends BaseAgent with a tools field containing OpenAI-format
    tool definitions that the LLM can invoke.

    Attributes:
        tools: List of tool definitions in OpenAI format.
               Each tool has type="function" and a function spec.
    """

    tools: List[Dict[str, Any]] = field(default_factory=list)


# Type alias for tool executor function
ToolExecutor = Callable[[str, Dict[str, Any]], Awaitable[Any]]


async def default_tool_executor(
    tool_name: str,
    arguments: Dict[str, Any],
    progress_callback: Optional[Callable] = None
) -> Any:
    """
    Default tool executor that dispatches to registered tools.

    Supports:
    - Indexer tools (index_project, search_architecture, etc.)
    - Todo tools (add_task, list_tasks, update_task_status, etc.)

    Args:
        tool_name: Name of the tool to execute
        arguments: Tool arguments dictionary
        progress_callback: Optional progress callback

    Returns:
        Tool execution result
    """
    from src.agents.indexer import dispatch_tool, INDEXER_TOOLS
    from src.agents.todo import dispatch_todo_tool, TODO_TOOLS

    # Check if tool is a known indexer tool
    indexer_tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]
    if tool_name in indexer_tool_names:
        return await dispatch_tool(tool_name, arguments, progress_callback=progress_callback)

    # Check if tool is a known todo tool
    todo_tool_names = [t["function"]["name"] for t in TODO_TOOLS]
    if tool_name in todo_tool_names:
        # dispatch_todo_tool is sync (fast in-memory operations)
        return dispatch_todo_tool(tool_name, arguments)

    # Unknown tool
    return {"error": f"Unknown tool: {tool_name}"}


class ToolAgentRunner:
    """
    Executes ToolAgents with tool calling loop.

    Handles the tool execution cycle:
    1. Call LLM with tools
    2. If LLM returns tool_calls, execute them
    3. Send tool results back to LLM
    4. Repeat until LLM returns final response or max iterations

    Attributes:
        http_client: Async HTTP client for LLM calls
        tool_executor: Async function to execute tools
        max_iterations: Maximum tool call iterations (prevents infinite loops)
    """

    def __init__(
        self,
        http_client=None,
        tool_executor: Optional[ToolExecutor] = None,
        max_iterations: int = 10
    ):
        """
        Initialize ToolAgentRunner.

        Args:
            http_client: Async HTTP client for LLM calls
            tool_executor: Custom tool executor function.
                          If None, uses default_tool_executor.
            max_iterations: Max tool call iterations (default 10)
        """
        self._http_client = http_client
        self._tool_executor = tool_executor or default_tool_executor
        self._max_iterations = max_iterations

    async def run_with_tools(
        self,
        agent: ToolAgent,
        user_message: str,
        external_tools: Optional[List[Dict[str, Any]]] = None,
        context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> str:
        """
        Run a ToolAgent with tool execution loop.

        Merges external_tools with agent's built-in tools (external overrides).
        Executes the LLM -> tool -> LLM cycle until completion.

        Args:
            agent: The ToolAgent to run
            user_message: User's input message
            external_tools: Optional tools from UI/external source
                           (override agent tools with same name)
            context: Optional context to include
            temperature: LLM temperature
            max_tokens: Max tokens for LLM response

        Returns:
            Final text response from LLM

        Raises:
            RuntimeError: If max iterations exceeded
        """
        # Merge tools: agent tools first, external overrides
        merged_tools = self._merge_tools(agent.tools, external_tools or [])

        # Build initial messages
        system_prompt = agent.load_prompt()
        messages = self._build_messages(system_prompt, user_message, context)

        iteration = 0
        while iteration < self._max_iterations:
            iteration += 1

            # Call LLM with tools
            response = await call_llm(
                http_client=self._http_client,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=merged_tools if merged_tools else None
            )

            # Check if LLM wants to call tools
            tool_calls = response.get("tool_calls")

            if not tool_calls:
                # No tool calls - return content as final response
                return response.get("content", "")

            # Add assistant message with tool calls
            # Content must be string (not None) for message processing
            messages.append({
                "role": "assistant",
                "content": response.get("content") or "",
                "tool_calls": tool_calls
            })

            # Execute each tool call
            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                arguments_str = tool_call["function"]["arguments"]
                tool_call_id = tool_call["id"]

                # Parse arguments
                try:
                    arguments = json.loads(arguments_str)
                except json.JSONDecodeError:
                    arguments = {}

                # Execute tool
                result = await self._tool_executor(tool_name, arguments)

                # Convert result to string if needed
                if isinstance(result, dict):
                    result_str = json.dumps(result)
                else:
                    result_str = str(result)

                # Add tool result message
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result_str
                })

        # Max iterations exceeded
        raise RuntimeError(f"Max iterations ({self._max_iterations}) exceeded in tool execution loop")

    def _merge_tools(
        self,
        agent_tools: List[Dict[str, Any]],
        external_tools: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge agent tools with external tools.

        External tools with same name override agent tools.

        Args:
            agent_tools: Agent's built-in tools
            external_tools: External tools (from UI/caller)

        Returns:
            Merged list of tools
        """
        # Build map of agent tools by name
        tools_map = {}
        for tool in agent_tools:
            name = tool.get("function", {}).get("name")
            if name:
                tools_map[name] = tool

        # External tools override
        for tool in external_tools:
            name = tool.get("function", {}).get("name")
            if name:
                tools_map[name] = tool

        return list(tools_map.values())

    def _build_messages(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Build initial message list.

        Args:
            system_prompt: Agent's system prompt
            user_message: User's input
            context: Optional context

        Returns:
            List of messages for LLM
        """
        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({
                "role": "system",
                "content": f"Context:\n{context}"
            })

        messages.append({"role": "user", "content": user_message})

        return messages


class IndexerAgent(ToolAgent):
    """
    Pre-configured ToolAgent for codebase indexing.

    Comes with INDEXER_TOOLS pre-loaded for:
    - index_project: Index a codebase
    - update_project: Update index with changes
    - search_architecture: Search indexed symbols
    - list_projects: List indexed projects
    - delete_project: Remove project index
    """

    def __init__(self):
        """Initialize IndexerAgent with default configuration."""
        from src.agents.indexer import INDEXER_TOOLS

        super().__init__(
            id="indexer",
            name="Project Architecture Indexer",
            prompt_path="indexer",
            description="Indexes codebase structure and enables architecture search",
            tools=list(INDEXER_TOOLS)  # Copy to avoid mutation
        )


__all__ = [
    "ToolAgent",
    "ToolAgentRunner",
    "IndexerAgent",
    "default_tool_executor",
]
