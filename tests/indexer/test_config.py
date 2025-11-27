"""
Tests for the indexer configuration module (Phase 2 - RED Stage).

These tests verify config behavior for path validation and language mapping.
TDD: Tests FAIL because stubs return None/pass → Implement → Tests PASS.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.agents.indexer.config import (
    SUPPORTED_EXTENSIONS,
    validate_path,
    get_output_dir,
    get_language_for_extension,
)


class TestT019ValidatePathAllowed:
    """T019: validate_path() returns (True, None) for allowed path."""

    def test_validate_allowed_path_returns_true(self):
        """An allowed path should return (True, None)."""
        with patch.dict(
            os.environ,
            {"ALLOWED_INDEX_ROOTS": "/opt/projects,/home/user/code"},
        ):
            result = validate_path("/opt/projects/my-app")

        assert result is not None, "validate_path() must not return None"
        assert isinstance(result, tuple), "validate_path() must return a tuple"
        assert len(result) == 2, "validate_path() must return (is_valid, error)"

        is_valid, error = result
        assert is_valid is True, f"Path should be valid, got error: {error}"
        assert error is None, "Error should be None for valid path"

    def test_validate_path_under_allowed_root(self):
        """A path under an allowed root should be valid."""
        with patch.dict(
            os.environ,
            {"ALLOWED_INDEX_ROOTS": "/opt/projects"},
        ):
            is_valid, error = validate_path("/opt/projects/deep/nested/path")

        assert is_valid is True
        assert error is None


class TestT020ValidatePathDisallowed:
    """T020: validate_path() returns (False, error) for disallowed path."""

    def test_validate_disallowed_path_returns_false(self):
        """A path outside allowed roots should return (False, error_message)."""
        with patch.dict(
            os.environ,
            {"ALLOWED_INDEX_ROOTS": "/opt/projects"},
        ):
            result = validate_path("/etc/passwd")

        assert result is not None, "validate_path() must not return None"
        is_valid, error = result
        assert is_valid is False, "Disallowed path should be invalid"
        assert error is not None, "Error message should be provided"
        assert isinstance(error, str), "Error should be a string"

    def test_validate_root_path_not_allowed(self):
        """Root path should be disallowed if not in allowlist."""
        with patch.dict(
            os.environ,
            {"ALLOWED_INDEX_ROOTS": "/opt/projects"},
        ):
            is_valid, error = validate_path("/")

        assert is_valid is False
        assert error is not None


class TestT021ValidatePathTraversal:
    """T021: validate_path() rejects path traversal (..)."""

    def test_validate_path_rejects_dot_dot(self):
        """Path with .. should be rejected."""
        with patch.dict(
            os.environ,
            {"ALLOWED_INDEX_ROOTS": "/opt/projects"},
        ):
            is_valid, error = validate_path("/opt/projects/../etc/passwd")

        assert is_valid is False, "Path traversal should be rejected"
        assert error is not None, "Error message should explain rejection"

    def test_validate_path_rejects_hidden_traversal(self):
        """Path with encoded traversal should be rejected."""
        with patch.dict(
            os.environ,
            {"ALLOWED_INDEX_ROOTS": "/opt/projects"},
        ):
            # Even if it looks like it's under allowed root after resolution
            is_valid, error = validate_path("/opt/projects/app/../../../etc")

        assert is_valid is False


class TestT022GetLanguageForExtension:
    """T022: get_language_for_extension() maps extensions to languages."""

    def test_python_extension_mapping(self):
        """Extension .py should map to 'python'."""
        result = get_language_for_extension(".py")

        assert result is not None, "get_language_for_extension() must not return None for .py"
        assert result == "python", f"Expected 'python', got '{result}'"

    def test_javascript_extension_mapping(self):
        """Extension .js should map to 'javascript'."""
        result = get_language_for_extension(".js")

        assert result == "javascript"

    def test_typescript_extension_mapping(self):
        """Extension .ts should map to 'typescript'."""
        result = get_language_for_extension(".ts")

        assert result == "typescript"

    def test_tsx_extension_mapping(self):
        """Extension .tsx should map to 'typescript'."""
        result = get_language_for_extension(".tsx")

        assert result == "typescript"

    def test_go_extension_mapping(self):
        """Extension .go should map to 'go'."""
        result = get_language_for_extension(".go")

        assert result == "go"

    def test_java_extension_mapping(self):
        """Extension .java should map to 'java'."""
        result = get_language_for_extension(".java")

        assert result == "java"

    def test_unsupported_extension_returns_none(self):
        """Unsupported extension should return None."""
        result = get_language_for_extension(".xyz")

        assert result is None, "Unsupported extension should return None"


class TestSupportedExtensions:
    """Test the SUPPORTED_EXTENSIONS constant."""

    def test_supported_extensions_is_dict(self):
        """SUPPORTED_EXTENSIONS should be a dictionary."""
        assert isinstance(SUPPORTED_EXTENSIONS, dict)

    def test_supported_extensions_has_python(self):
        """SUPPORTED_EXTENSIONS should include .py."""
        assert ".py" in SUPPORTED_EXTENSIONS
        assert SUPPORTED_EXTENSIONS[".py"] == "python"

    def test_supported_extensions_has_all_languages(self):
        """SUPPORTED_EXTENSIONS should have all required languages."""
        required = {".py", ".js", ".ts", ".tsx", ".go", ".java"}
        assert required.issubset(set(SUPPORTED_EXTENSIONS.keys()))


class TestGetOutputDir:
    """Test the get_output_dir function."""

    def test_get_output_dir_returns_path(self):
        """get_output_dir should return a Path object."""
        result = get_output_dir("my-project")

        assert result is not None, "get_output_dir() must not return None"
        assert isinstance(result, Path), "get_output_dir() must return a Path"

    def test_get_output_dir_includes_project_name(self):
        """Output dir should include the project name."""
        result = get_output_dir("test-project")

        assert result is not None
        assert "test-project" in str(result)
