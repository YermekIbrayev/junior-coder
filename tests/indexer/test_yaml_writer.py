"""
Tests for the indexer YAML writer module (Phase 3 - RED Stage).

These tests verify YAML output generation.
TDD: Tests FAIL because stubs return None → Implement → Tests PASS.
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest
import yaml

from src.agents.indexer.yaml_writer import (
    sanitize_path_for_filename,
    write_project_yaml,
    write_structure_yaml,
    write_file_yaml,
)
from src.agents.indexer.models import (
    Project,
    FileNode,
    FunctionDef,
    ClassDef,
    ProjectStatus,
    ParseStatus,
)


class TestT052SanitizePathForFilename:
    """T052: sanitize_path_for_filename() converts / to _."""

    def test_sanitize_converts_slashes(self):
        """Forward slashes should be converted to underscores."""
        path = "src/utils/helpers.py"

        result = sanitize_path_for_filename(path)

        assert result is not None, "sanitize_path_for_filename should return a string"
        assert "/" not in result, "Result should not contain slashes"
        assert "src_utils_helpers.py" == result or "src_utils_helpers_py" == result

    def test_sanitize_handles_root_path(self):
        """Root-level files should be handled."""
        path = "main.py"

        result = sanitize_path_for_filename(path)

        assert result is not None
        assert result == "main.py" or result == "main_py"

    def test_sanitize_handles_deep_path(self):
        """Deep paths should be flattened."""
        path = "src/components/ui/buttons/primary.tsx"

        result = sanitize_path_for_filename(path)

        assert result is not None
        assert "/" not in result


class TestT053WriteProjectYaml:
    """T053: write_project_yaml() creates valid YAML file."""

    @pytest.mark.asyncio
    async def test_write_project_creates_file(self, tmp_path):
        """write_project_yaml should create a YAML file."""
        project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/opt/projects/test",
            status=ProjectStatus.ACTIVE,
            file_count=10,
            symbol_count=50,
            indexed_at=datetime.now(),
        )

        result = await write_project_yaml(project, tmp_path)

        assert result is not None, "write_project_yaml should return a Path"
        assert result.exists(), "YAML file should be created"
        assert result.suffix == ".yaml", "File should have .yaml extension"

    @pytest.mark.asyncio
    async def test_write_project_valid_yaml(self, tmp_path):
        """write_project_yaml should create valid, parseable YAML."""
        project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/opt/projects/test",
            status=ProjectStatus.ACTIVE,
            file_count=10,
            symbol_count=50,
        )

        result = await write_project_yaml(project, tmp_path)

        assert result is not None
        # Parse the YAML to verify it's valid
        content = yaml.safe_load(result.read_text())
        assert content is not None, "YAML should be parseable"
        assert "project" in content or "name" in content, "Should have project data"

    @pytest.mark.asyncio
    async def test_write_project_includes_metadata(self, tmp_path):
        """write_project_yaml should include project metadata."""
        project = Project(
            id=uuid4(),
            name="my-app",
            root_path="/opt/projects/my-app",
            status=ProjectStatus.ACTIVE,
            file_count=100,
            symbol_count=500,
        )

        result = await write_project_yaml(project, tmp_path)

        assert result is not None
        content = yaml.safe_load(result.read_text())

        # Check for expected fields (could be nested under 'project' key)
        data = content.get("project", content)
        assert data.get("name") == "my-app" or "my-app" in str(content)


class TestT054WriteFileYaml:
    """T054: write_file_yaml() includes functions and classes."""

    @pytest.mark.asyncio
    async def test_write_file_includes_functions(self, tmp_path):
        """write_file_yaml should include function definitions."""
        func = FunctionDef(
            name="hello",
            line_number=10,
            signature="def hello() -> str",
            docstring="Say hello",
        )

        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
            functions=[func],
            classes=[],
        )

        result = await write_file_yaml(file_node, tmp_path)

        assert result is not None, "write_file_yaml should return a Path"
        assert result.exists(), "YAML file should be created"

        content = yaml.safe_load(result.read_text())
        assert content is not None

        # Check for functions
        assert "functions" in content or any(
            "hello" in str(v) for v in content.values()
        ), "Should include function data"

    @pytest.mark.asyncio
    async def test_write_file_includes_classes(self, tmp_path):
        """write_file_yaml should include class definitions."""
        cls = ClassDef(
            name="MyClass",
            line_number=20,
            parent_classes=["BaseClass"],
            docstring="A test class",
            method_names=["__init__", "process"],
        )

        file_node = FileNode(
            relative_path="src/models.py",
            language="python",
            content_hash="def456",
            size_bytes=2048,
            last_modified=datetime.now(),
            functions=[],
            classes=[cls],
        )

        result = await write_file_yaml(file_node, tmp_path)

        assert result is not None
        content = yaml.safe_load(result.read_text())

        # Check for classes
        assert "classes" in content or any(
            "MyClass" in str(v) for v in content.values()
        ), "Should include class data"


class TestWriteStructureYaml:
    """Additional tests for write_structure_yaml."""

    @pytest.mark.asyncio
    async def test_write_structure_creates_file(self, tmp_path):
        """write_structure_yaml should create a structure file."""
        project = Project(
            name="test",
            root_path="/opt/test",
        )
        files = [
            FileNode(
                relative_path="src/main.py",
                language="python",
                content_hash="hash1",
                size_bytes=100,
                last_modified=datetime.now(),
            ),
            FileNode(
                relative_path="src/utils.py",
                language="python",
                content_hash="hash2",
                size_bytes=200,
                last_modified=datetime.now(),
            ),
        ]

        result = await write_structure_yaml(project, files, tmp_path)

        assert result is not None, "write_structure_yaml should return a Path"
        assert result.exists(), "Structure file should be created"
