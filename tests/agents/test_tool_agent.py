"""
Tests for ToolAgent and ToolAgentRunner - TDD RED Stage.

TDD: Tests FAIL because classes don't exist yet.

Architecture:
- ToolAgent: Agent that can use tools (extends BaseAgent)
- ToolAgentRunner: Runs agents with tool execution loop
- IndexerAgent: Specialized agent for codebase indexing
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json


# =============================================================================
# T01: ToolAgent Class Tests
# =============================================================================

class TestToolAgentFields:
    """T01: ToolAgent extends BaseAgent with tools field."""

    def test_tool_agent_exists(self):
        """ToolAgent class must exist."""
        from src.agents.agents.tool_agent import ToolAgent
        assert ToolAgent is not None

    def test_tool_agent_extends_base_agent(self):
        """ToolAgent must extend BaseAgent."""
        from src.agents.agents.tool_agent import ToolAgent
        from src.agents.agents.base import BaseAgent
        assert issubclass(ToolAgent, BaseAgent)

    def test_tool_agent_has_tools_field(self):
        """ToolAgent must have a 'tools' field."""
        from src.agents.agents.tool_agent import ToolAgent

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="test-agent",
            tools=[]
        )
        assert hasattr(agent, "tools")

    def test_tool_agent_tools_default_empty(self):
        """ToolAgent tools should default to empty list."""
        from src.agents.agents.tool_agent import ToolAgent

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="test-agent"
        )
        assert agent.tools == []

    def test_tool_agent_accepts_tool_definitions(self):
        """ToolAgent must accept OpenAI-format tool definitions."""
        from src.agents.agents.tool_agent import ToolAgent

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"}
                        },
                        "required": ["path"]
                    }
                }
            }
        ]

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="test-agent",
            tools=tools
        )
        assert len(agent.tools) == 1
        assert agent.tools[0]["function"]["name"] == "read_file"


# =============================================================================
# T02: ToolAgentRunner.run_with_tools() Tests
# =============================================================================

class TestToolAgentRunnerBasic:
    """T02: ToolAgentRunner has run_with_tools method."""

    def test_tool_agent_runner_exists(self):
        """ToolAgentRunner class must exist."""
        from src.agents.agents.tool_agent import ToolAgentRunner
        assert ToolAgentRunner is not None

    @pytest.mark.asyncio
    async def test_run_with_tools_method_exists(self):
        """ToolAgentRunner must have run_with_tools async method."""
        from src.agents.agents.tool_agent import ToolAgentRunner

        runner = ToolAgentRunner()
        assert hasattr(runner, "run_with_tools")

    @pytest.mark.asyncio
    async def test_run_with_tools_accepts_agent(self, mock_httpx_client):
        """run_with_tools must accept a ToolAgent."""
        from src.agents.agents.tool_agent import ToolAgent, ToolAgentRunner

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="spec-analyst",  # Use existing prompt
            tools=[]
        )
        runner = ToolAgentRunner(http_client=mock_httpx_client)

        result = await runner.run_with_tools(
            agent=agent,
            user_message="Hello"
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_run_with_tools_accepts_external_tools(self, mock_httpx_client):
        """run_with_tools must accept external tools parameter."""
        from src.agents.agents.tool_agent import ToolAgent, ToolAgentRunner

        external_tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List directory contents",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="spec-analyst",
            tools=[]
        )
        runner = ToolAgentRunner(http_client=mock_httpx_client)

        # Should accept external_tools parameter
        result = await runner.run_with_tools(
            agent=agent,
            user_message="List files",
            external_tools=external_tools
        )
        assert result is not None


# =============================================================================
# T03: Tool Execution Loop Tests
# =============================================================================

class TestToolExecutionLoop:
    """T03: ToolAgentRunner executes tool calls from LLM."""

    @pytest.mark.asyncio
    async def test_run_with_tools_executes_tool_calls(self):
        """run_with_tools must execute tool calls returned by LLM."""
        from src.agents.agents.tool_agent import ToolAgent, ToolAgentRunner

        # Mock LLM returning a tool call
        mock_client = AsyncMock()

        # First response: tool call
        tool_call_response = MagicMock()
        tool_call_response.status_code = 200
        tool_call_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "read_file",
                            "arguments": json.dumps({"path": "/test/file.py"})
                        }
                    }]
                }
            }]
        }
        tool_call_response.raise_for_status = MagicMock()

        # Second response: final answer after tool result
        final_response = MagicMock()
        final_response.status_code = 200
        final_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "Based on the file content, here's my analysis..."
                }
            }]
        }
        final_response.raise_for_status = MagicMock()

        mock_client.post.side_effect = [tool_call_response, final_response]

        # Mock tool executor
        mock_executor = AsyncMock()
        mock_executor.return_value = "File content: def hello(): pass"

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="spec-analyst",
            tools=[{
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a file",
                    "parameters": {"type": "object", "properties": {"path": {"type": "string"}}}
                }
            }]
        )
        runner = ToolAgentRunner(
            http_client=mock_client,
            tool_executor=mock_executor
        )

        result = await runner.run_with_tools(
            agent=agent,
            user_message="Read the file"
        )

        # Should have called tool executor
        mock_executor.assert_called_once()

        # Should return final answer
        assert "analysis" in result.lower()

    @pytest.mark.asyncio
    async def test_run_with_tools_max_iterations(self):
        """run_with_tools must have max iteration limit to prevent infinite loops."""
        from src.agents.agents.tool_agent import ToolAgent, ToolAgentRunner

        mock_client = AsyncMock()

        # Always return tool call (would cause infinite loop)
        tool_call_response = MagicMock()
        tool_call_response.status_code = 200
        tool_call_response.json.return_value = {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "read_file",
                            "arguments": json.dumps({"path": "/test"})
                        }
                    }]
                }
            }]
        }
        tool_call_response.raise_for_status = MagicMock()

        mock_client.post.return_value = tool_call_response

        mock_executor = AsyncMock(return_value="result")

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="spec-analyst",
            tools=[{"type": "function", "function": {"name": "read_file", "parameters": {}}}]
        )
        runner = ToolAgentRunner(
            http_client=mock_client,
            tool_executor=mock_executor,
            max_iterations=3
        )

        # Should stop after max_iterations
        with pytest.raises(RuntimeError, match="Max iterations"):
            await runner.run_with_tools(agent=agent, user_message="Read files")


# =============================================================================
# T04: IndexerAgent Tests
# =============================================================================

class TestIndexerAgent:
    """T04: IndexerAgent is a ToolAgent with INDEXER_TOOLS."""

    def test_indexer_agent_exists(self):
        """IndexerAgent class must exist."""
        from src.agents.agents.tool_agent import IndexerAgent
        assert IndexerAgent is not None

    def test_indexer_agent_is_tool_agent(self):
        """IndexerAgent must be a ToolAgent."""
        from src.agents.agents.tool_agent import IndexerAgent, ToolAgent
        assert issubclass(IndexerAgent, ToolAgent)

    def test_indexer_agent_has_indexer_tools(self):
        """IndexerAgent must have INDEXER_TOOLS by default."""
        from src.agents.agents.tool_agent import IndexerAgent
        from src.agents.indexer import INDEXER_TOOLS

        agent = IndexerAgent()

        # Should have all indexer tools
        tool_names = [t["function"]["name"] for t in agent.tools]
        indexer_tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]

        for name in indexer_tool_names:
            assert name in tool_names, f"Missing tool: {name}"

    def test_indexer_agent_has_correct_id(self):
        """IndexerAgent must have id='indexer'."""
        from src.agents.agents.tool_agent import IndexerAgent

        agent = IndexerAgent()
        assert agent.id == "indexer"


# =============================================================================
# T05: Tool Merging Tests
# =============================================================================

class TestToolMerging:
    """T05: External tools merge with agent's built-in tools."""

    @pytest.mark.asyncio
    async def test_external_tools_merge_with_agent_tools(self, mock_httpx_client):
        """run_with_tools should merge external tools with agent's tools."""
        from src.agents.agents.tool_agent import ToolAgent, ToolAgentRunner

        agent_tools = [
            {"type": "function", "function": {"name": "tool_a", "parameters": {}}}
        ]
        external_tools = [
            {"type": "function", "function": {"name": "tool_b", "parameters": {}}}
        ]

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="spec-analyst",
            tools=agent_tools
        )
        runner = ToolAgentRunner(http_client=mock_httpx_client)

        await runner.run_with_tools(
            agent=agent,
            user_message="Use tools",
            external_tools=external_tools
        )

        # Check that LLM was called with both tools
        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        tool_names = [t["function"]["name"] for t in json_data.get("tools", [])]

        assert "tool_a" in tool_names
        assert "tool_b" in tool_names

    @pytest.mark.asyncio
    async def test_external_tools_override_agent_tools(self, mock_httpx_client):
        """External tools with same name should override agent tools."""
        from src.agents.agents.tool_agent import ToolAgent, ToolAgentRunner

        agent_tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Agent version",
                    "parameters": {}
                }
            }
        ]
        external_tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "External version",
                    "parameters": {}
                }
            }
        ]

        agent = ToolAgent(
            id="test-agent",
            name="Test Agent",
            prompt_path="spec-analyst",
            tools=agent_tools
        )
        runner = ToolAgentRunner(http_client=mock_httpx_client)

        await runner.run_with_tools(
            agent=agent,
            user_message="Read file",
            external_tools=external_tools
        )

        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        tools = json_data.get("tools", [])

        # Should only have one read_file (external version)
        read_file_tools = [t for t in tools if t["function"]["name"] == "read_file"]
        assert len(read_file_tools) == 1
        assert read_file_tools[0]["function"]["description"] == "External version"


# =============================================================================
# T06: Tool Executor Tests
# =============================================================================

class TestToolExecutor:
    """T06: Default tool executor dispatches to indexer tools."""

    @pytest.mark.asyncio
    async def test_default_executor_dispatches_indexer_tools(self):
        """Default executor should dispatch to indexer's dispatch_tool."""
        from src.agents.agents.tool_agent import default_tool_executor

        with patch("src.agents.indexer.dispatch_tool", new_callable=AsyncMock) as mock_dispatch:
            mock_dispatch.return_value = {"status": "success"}

            result = await default_tool_executor(
                "index_project",
                {"path": "/test/project"}
            )

            mock_dispatch.assert_called_once_with(
                "index_project",
                {"path": "/test/project"},
                progress_callback=None
            )

    @pytest.mark.asyncio
    async def test_executor_handles_unknown_tools(self):
        """Executor should handle unknown tool names gracefully."""
        from src.agents.agents.tool_agent import default_tool_executor

        result = await default_tool_executor(
            "unknown_tool",
            {}
        )

        assert "error" in result or "unknown" in str(result).lower()


# =============================================================================
# T07: Integration with Classifier Tests
# =============================================================================

class TestClassifierIntegration:
    """T07: IndexerAgent can be called by classifier."""

    def test_indexer_agent_in_registry(self):
        """IndexerAgent should be registered in agent registry."""
        from src.agents.gateway.registry import AGENTS

        assert "indexer" in AGENTS

    @pytest.mark.asyncio
    async def test_run_indexer_agent_with_user_tools(self, mock_httpx_client):
        """Should be able to run IndexerAgent with UI-provided tools."""
        from src.agents.agents.tool_agent import IndexerAgent, ToolAgentRunner

        # UI provides read/list tools
        ui_tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read file from UI",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "List directory from UI",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            }
        ]

        agent = IndexerAgent()
        runner = ToolAgentRunner(http_client=mock_httpx_client)

        result = await runner.run_with_tools(
            agent=agent,
            user_message="Index the project at /workspace",
            external_tools=ui_tools
        )

        # Should have merged all tools
        call_args = mock_httpx_client.post.call_args
        json_data = call_args[1].get("json", {})
        tool_names = [t["function"]["name"] for t in json_data.get("tools", [])]

        # UI tools
        assert "read_file" in tool_names
        assert "list_directory" in tool_names

        # Indexer tools
        assert "index_project" in tool_names
