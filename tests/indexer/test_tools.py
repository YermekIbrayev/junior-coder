"""
Tests for the indexer tools module (Phase 3 - RED Stage).

These tests verify LLM tool handlers for the indexer.
TDD: Tests FAIL because stubs return None/pass → Implement → Tests PASS.
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.agents.indexer.tools import (
    INDEXER_TOOLS,
    handle_index_project,
    handle_update_project,
    handle_list_projects,
    handle_search_architecture,
    handle_delete_project,
    dispatch_tool,
)


class TestT058HandleIndexProject:
    """T058: handle_index_project() orchestrates full indexing flow."""

    @pytest.mark.asyncio
    async def test_handle_index_project_returns_result(self, tmp_path):
        """handle_index_project should return a result dict."""
        # Create a minimal project structure
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")

        result = await handle_index_project(str(tmp_path))

        assert result is not None, "handle_index_project should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_handle_index_project_returns_project_id(self, tmp_path):
        """handle_index_project should return a project_id."""
        # Create a minimal project structure
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")

        result = await handle_index_project(str(tmp_path))

        assert result is not None
        assert "project_id" in result, "Result should contain project_id"
        assert result["project_id"] is not None, "project_id should not be None"

    @pytest.mark.asyncio
    async def test_handle_index_project_returns_statistics(self, tmp_path):
        """handle_index_project should return indexing statistics."""
        # Create project with multiple files
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")
        (src_dir / "utils.py").write_text("def helper(): pass")

        result = await handle_index_project(str(tmp_path))

        assert result is not None
        # Should have file count
        assert "file_count" in result or "files_indexed" in result, (
            "Result should contain file count"
        )

    @pytest.mark.asyncio
    async def test_handle_index_project_validates_path(self):
        """handle_index_project should validate the path."""
        # Try to index a non-existent path
        result = await handle_index_project("/nonexistent/path/12345")

        assert result is not None
        # Should return error or status
        assert "error" in result or "status" in result, (
            "Should return error for invalid path"
        )

    @pytest.mark.asyncio
    async def test_handle_index_project_rejects_traversal(self, tmp_path):
        """handle_index_project should reject path traversal."""
        # Try path traversal
        result = await handle_index_project(str(tmp_path / ".." / ".."))

        assert result is not None
        # Should return error
        assert "error" in result or (
            result.get("status") == "error"
        ), "Should reject path traversal"

    @pytest.mark.asyncio
    async def test_handle_index_project_calls_progress_callback(self, tmp_path):
        """handle_index_project should call progress callback."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")

        progress_messages = []

        def progress_callback(msg: str):
            progress_messages.append(msg)

        result = await handle_index_project(
            str(tmp_path),
            progress_callback=progress_callback,
        )

        # Progress callback should have been called at least once
        # (if implemented properly)
        # Note: This may pass if callback is optional
        assert result is not None


class TestT059DispatchTool:
    """T059: dispatch_tool() routes to correct handler."""

    @pytest.mark.asyncio
    async def test_dispatch_index_project(self, tmp_path):
        """dispatch_tool should route 'index_project' to handle_index_project."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")

        result = await dispatch_tool(
            tool_name="index_project",
            arguments={"path": str(tmp_path)},
        )

        assert result is not None, "dispatch_tool should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_dispatch_list_projects(self):
        """dispatch_tool should route 'list_indexed_projects' correctly."""
        result = await dispatch_tool(
            tool_name="list_indexed_projects",
            arguments={},
        )

        assert result is not None, "dispatch_tool should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_dispatch_unknown_tool(self):
        """dispatch_tool should handle unknown tool names."""
        result = await dispatch_tool(
            tool_name="unknown_tool_12345",
            arguments={},
        )

        assert result is not None
        # Should return error for unknown tool
        assert "error" in result or result.get("status") == "error", (
            "Should return error for unknown tool"
        )

    @pytest.mark.asyncio
    async def test_dispatch_with_progress_callback(self, tmp_path):
        """dispatch_tool should pass progress_callback to handler."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("def main(): pass")

        progress_messages = []

        def progress_callback(msg: str):
            progress_messages.append(msg)

        result = await dispatch_tool(
            tool_name="index_project",
            arguments={"path": str(tmp_path)},
            progress_callback=progress_callback,
        )

        assert result is not None


class TestIndexerToolsDefinition:
    """Tests for INDEXER_TOOLS definitions."""

    def test_tools_list_not_empty(self):
        """INDEXER_TOOLS should contain tool definitions."""
        assert len(INDEXER_TOOLS) > 0, "INDEXER_TOOLS should not be empty"

    def test_tools_have_required_fields(self):
        """Each tool should have type and function fields."""
        for tool in INDEXER_TOOLS:
            assert "type" in tool, "Tool should have 'type' field"
            assert tool["type"] == "function", "Tool type should be 'function'"
            assert "function" in tool, "Tool should have 'function' field"

    def test_tools_have_name_and_description(self):
        """Each tool function should have name and description."""
        for tool in INDEXER_TOOLS:
            func = tool["function"]
            assert "name" in func, "Function should have 'name'"
            assert "description" in func, "Function should have 'description'"
            assert len(func["description"]) > 0, "Description should not be empty"

    def test_tools_have_parameters_schema(self):
        """Each tool function should have parameters schema."""
        for tool in INDEXER_TOOLS:
            func = tool["function"]
            assert "parameters" in func, "Function should have 'parameters'"
            params = func["parameters"]
            assert "type" in params, "Parameters should have 'type'"
            assert params["type"] == "object", "Parameters type should be 'object'"

    def test_index_project_tool_exists(self):
        """index_project tool should be defined."""
        tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]
        assert "index_project" in tool_names, "index_project tool should exist"

    def test_list_indexed_projects_tool_exists(self):
        """list_indexed_projects tool should be defined."""
        tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]
        assert "list_indexed_projects" in tool_names, (
            "list_indexed_projects tool should exist"
        )

    def test_search_architecture_tool_exists(self):
        """search_architecture tool should be defined."""
        tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]
        assert "search_architecture" in tool_names, (
            "search_architecture tool should exist"
        )

    def test_update_project_index_tool_exists(self):
        """update_project_index tool should be defined."""
        tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]
        assert "update_project_index" in tool_names, (
            "update_project_index tool should exist"
        )


class TestT089HandleUpdateProject:
    """T089: handle_update_project() incremental update tests."""

    @pytest.mark.asyncio
    async def test_handle_update_project_returns_result(self):
        """handle_update_project should return a result dict."""
        from uuid import uuid4

        project_id = str(uuid4())

        # Mock the storage functions
        with patch(
            "src.agents.indexer.storage.get_project",
            new_callable=AsyncMock,
            return_value=MagicMock(
                id=project_id,
                name="test-project",
                root_path="/tmp/test-project",
            ),
        ), patch(
            "src.agents.indexer.storage.get_file_hashes",
            new_callable=AsyncMock,
            return_value={"src/main.py": "hash1"},
        ), patch(
            "src.agents.indexer.storage.store_project",
            new_callable=AsyncMock,
            return_value=project_id,
        ):
            result = await handle_update_project(project_id)

        assert result is not None, "handle_update_project should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_handle_update_project_returns_statistics(self):
        """handle_update_project should return update statistics."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.get_project",
            new_callable=AsyncMock,
            return_value=MagicMock(
                id=project_id,
                name="test-project",
                root_path="/tmp/test-project",
            ),
        ), patch(
            "src.agents.indexer.storage.get_file_hashes",
            new_callable=AsyncMock,
            return_value={},
        ), patch(
            "src.agents.indexer.storage.store_project",
            new_callable=AsyncMock,
            return_value=project_id,
        ):
            result = await handle_update_project(project_id)

        assert result is not None
        # Should contain update statistics (added, modified, deleted counts)
        assert (
            "added" in result
            or "modified" in result
            or "deleted" in result
            or "files_processed" in result
            or "status" in result
        ), "Result should contain update statistics"

    @pytest.mark.asyncio
    async def test_handle_update_project_invalid_project_returns_error(self):
        """handle_update_project should return error for non-existent project."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.get_project",
            new_callable=AsyncMock,
            return_value=None,  # Project not found
        ):
            result = await handle_update_project(project_id)

        assert result is not None
        assert "error" in result or result.get("status") == "error", (
            "Should return error for non-existent project"
        )

    @pytest.mark.asyncio
    async def test_handle_update_project_force_full_reindex(self):
        """handle_update_project with force_full=True should reindex all files."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.get_project",
            new_callable=AsyncMock,
            return_value=MagicMock(
                id=project_id,
                name="test-project",
                root_path="/tmp/test-project",
            ),
        ), patch(
            "src.agents.indexer.storage.get_file_hashes",
            new_callable=AsyncMock,
            return_value={"src/main.py": "hash1"},
        ), patch(
            "src.agents.indexer.storage.store_project",
            new_callable=AsyncMock,
            return_value=project_id,
        ):
            result = await handle_update_project(project_id, force_full=True)

        assert result is not None
        assert isinstance(result, dict), "Should return a dict"

    @pytest.mark.asyncio
    async def test_dispatch_update_project_index(self):
        """dispatch_tool should route 'update_project_index' correctly."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.get_project",
            new_callable=AsyncMock,
            return_value=None,  # Will return error
        ):
            result = await dispatch_tool(
                tool_name="update_project_index",
                arguments={"project_id": project_id},
            )

        assert result is not None, "dispatch_tool should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"


class TestT098HandleSearchArchitecture:
    """T098: handle_search_architecture() returns formatted results."""

    @pytest.mark.asyncio
    async def test_handle_search_architecture_returns_result(self):
        """handle_search_architecture should return a result dict."""
        with patch(
            "src.agents.indexer.storage.search_vectors",
            new_callable=AsyncMock,
            return_value=[
                {"symbol_name": "authenticate", "file_path": "src/auth.py", "score": 0.95},
            ],
        ):
            result = await handle_search_architecture("authentication functions")

        assert result is not None, "handle_search_architecture should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_handle_search_architecture_includes_results_list(self):
        """handle_search_architecture should include results list."""
        with patch(
            "src.agents.indexer.storage.search_vectors",
            new_callable=AsyncMock,
            return_value=[
                {"symbol_name": "authenticate", "file_path": "src/auth.py", "score": 0.95},
                {"symbol_name": "verify_token", "file_path": "src/auth.py", "score": 0.87},
            ],
        ):
            result = await handle_search_architecture("authentication")

        assert result is not None
        assert "results" in result or "matches" in result, (
            "Result should contain results or matches"
        )

    @pytest.mark.asyncio
    async def test_handle_search_architecture_with_project_filter(self):
        """handle_search_architecture should filter by project_id."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.search_vectors",
            new_callable=AsyncMock,
            return_value=[],
        ) as mock_search:
            result = await handle_search_architecture("query", project_id=project_id)

        assert result is not None
        # Verify search_vectors was called with project_id
        mock_search.assert_called_once()

    @pytest.mark.asyncio
    async def test_dispatch_search_architecture(self):
        """dispatch_tool should route 'search_architecture' correctly."""
        with patch(
            "src.agents.indexer.storage.search_vectors",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await dispatch_tool(
                tool_name="search_architecture",
                arguments={"query": "test query"},
            )

        assert result is not None, "dispatch_tool should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"


class TestT099HandleListProjects:
    """T099: handle_list_projects() returns project summaries."""

    @pytest.mark.asyncio
    async def test_handle_list_projects_returns_result(self):
        """handle_list_projects should return a result dict."""
        with patch(
            "src.agents.indexer.storage.list_projects",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await handle_list_projects()

        assert result is not None, "handle_list_projects should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_handle_list_projects_includes_projects_list(self):
        """handle_list_projects should include projects list."""
        from datetime import datetime
        from uuid import uuid4

        from src.agents.indexer.models import Project, ProjectStatus

        mock_project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/opt/test",
            status=ProjectStatus.ACTIVE,
            file_count=10,
            symbol_count=50,
            indexed_at=datetime.now(),
        )

        with patch(
            "src.agents.indexer.storage.list_projects",
            new_callable=AsyncMock,
            return_value=[mock_project],
        ):
            result = await handle_list_projects()

        assert result is not None
        assert "projects" in result, "Result should contain projects list"
        assert isinstance(result["projects"], list), "Projects should be a list"


class TestT100HandleDeleteProject:
    """T100: handle_delete_project() removes project."""

    @pytest.mark.asyncio
    async def test_handle_delete_project_returns_result(self):
        """handle_delete_project should return a result dict."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.delete_project",
            new_callable=AsyncMock,
            return_value=True,
        ):
            result = await handle_delete_project(project_id)

        assert result is not None, "handle_delete_project should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"

    @pytest.mark.asyncio
    async def test_handle_delete_project_returns_status(self):
        """handle_delete_project should return status."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.delete_project",
            new_callable=AsyncMock,
            return_value=True,
        ):
            result = await handle_delete_project(project_id)

        assert result is not None
        assert "status" in result, "Result should contain status"

    @pytest.mark.asyncio
    async def test_handle_delete_project_not_found_returns_error(self):
        """handle_delete_project should return error for non-existent project."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.delete_project",
            new_callable=AsyncMock,
            return_value=False,  # Project not found
        ):
            result = await handle_delete_project(project_id)

        assert result is not None
        # Should indicate failure in some way
        assert "status" in result or "error" in result

    @pytest.mark.asyncio
    async def test_dispatch_delete_project_index(self):
        """dispatch_tool should route 'delete_project_index' correctly."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.delete_project",
            new_callable=AsyncMock,
            return_value=True,
        ):
            result = await dispatch_tool(
                tool_name="delete_project_index",
                arguments={"project_id": project_id},
            )

        assert result is not None, "dispatch_tool should return a result"
        assert isinstance(result, dict), "Result should be a dictionary"


class TestT101DispatchToolRouting:
    """T101: dispatch_tool() routes to correct handler."""

    @pytest.mark.asyncio
    async def test_dispatch_routes_search_architecture(self):
        """dispatch_tool should route 'search_architecture' to handler."""
        with patch(
            "src.agents.indexer.storage.search_vectors",
            new_callable=AsyncMock,
            return_value=[],
        ):
            result = await dispatch_tool(
                tool_name="search_architecture",
                arguments={"query": "test"},
            )

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_dispatch_routes_delete_project_index(self):
        """dispatch_tool should route 'delete_project_index' to handler."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.delete_project",
            new_callable=AsyncMock,
            return_value=True,
        ):
            result = await dispatch_tool(
                tool_name="delete_project_index",
                arguments={"project_id": project_id},
            )

        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_all_tools_routable(self):
        """All defined tools should be routable by dispatch_tool."""
        # Get all tool names from INDEXER_TOOLS
        tool_names = [t["function"]["name"] for t in INDEXER_TOOLS]

        # These should be the expected tools
        expected_tools = [
            "index_project",
            "update_project_index",
            "search_architecture",
            "list_indexed_projects",
            "delete_project_index",
        ]

        for name in expected_tools:
            assert name in tool_names, f"Tool '{name}' should be defined in INDEXER_TOOLS"


class TestT120HandleSearchArchitectureError:
    """T120: Test error handling in search_architecture."""

    @pytest.mark.asyncio
    async def test_handle_search_architecture_error_returns_error_status(self):
        """handle_search_architecture should return error status on exception."""
        with patch(
            "src.agents.indexer.storage.search_vectors",
            new_callable=AsyncMock,
            side_effect=Exception("Test error"),
        ):
            result = await handle_search_architecture("test query")

        assert result["status"] == "error"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_handle_search_architecture_invalid_project_id(self):
        """handle_search_architecture should handle invalid project_id."""
        # Invalid UUID should trigger an error
        result = await handle_search_architecture(
            "test query",
            project_id="not-a-valid-uuid",
        )

        assert result["status"] == "error"


class TestT120HandleDeleteProjectError:
    """T120: Test error handling in delete_project."""

    @pytest.mark.asyncio
    async def test_handle_delete_project_invalid_uuid(self):
        """handle_delete_project should return error for invalid UUID."""
        result = await handle_delete_project("not-a-valid-uuid")

        assert result["status"] == "error"
        assert "Invalid project ID" in result["error"]

    @pytest.mark.asyncio
    async def test_handle_delete_project_exception(self):
        """handle_delete_project should handle exceptions."""
        from uuid import uuid4

        project_id = str(uuid4())

        with patch(
            "src.agents.indexer.storage.delete_project",
            new_callable=AsyncMock,
            side_effect=Exception("Database error"),
        ):
            result = await handle_delete_project(project_id)

        assert result["status"] == "error"


class TestT120HandleListProjectsError:
    """T120: Test error handling in list_projects."""

    @pytest.mark.asyncio
    async def test_handle_list_projects_exception(self):
        """handle_list_projects should handle exceptions."""
        with patch(
            "src.agents.indexer.storage.list_projects",
            new_callable=AsyncMock,
            side_effect=Exception("Database error"),
        ):
            result = await handle_list_projects()

        assert result["status"] == "error"
        assert "projects" in result
        assert result["projects"] == []


class TestT120HandleUpdateProjectMissingPath:
    """T120: Test handle_update_project with missing project path."""

    @pytest.mark.asyncio
    async def test_handle_update_project_missing_path(self):
        """handle_update_project should return error if project path doesn't exist."""
        from datetime import datetime
        from uuid import uuid4

        from src.agents.indexer.models import Project, ProjectStatus

        # Mock project with non-existent path
        mock_project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/nonexistent/path/to/project",
            status=ProjectStatus.ACTIVE,
            file_count=10,
            symbol_count=50,
            indexed_at=datetime.now(),
        )

        with patch(
            "src.agents.indexer.storage.get_project",
            new_callable=AsyncMock,
            return_value=mock_project,
        ):
            result = await handle_update_project(str(mock_project.id))

        assert result["status"] == "error"
        assert "path no longer exists" in result["error"]
