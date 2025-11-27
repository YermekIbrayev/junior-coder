"""
Tests for the indexer parser module (Phase 3 - RED Stage).

These tests verify AST parsing using tree-sitter.
TDD: Tests FAIL because stubs return None → Implement → Tests PASS.
"""

from pathlib import Path

import pytest

from src.agents.indexer.parser import (
    get_parser,
    parse_file,
    extract_functions,
    extract_classes,
)


# Sample Python code for testing
SAMPLE_PYTHON_CODE = '''"""Module docstring."""

def simple_function():
    """A simple function."""
    pass


def function_with_params(name: str, count: int = 10) -> str:
    """Function with typed parameters.

    Args:
        name: The name parameter
        count: The count parameter

    Returns:
        Processed string
    """
    return name * count


async def async_function(data: list) -> dict:
    """An async function."""
    return {"data": data}


class SimpleClass:
    """A simple class."""

    def __init__(self, value: int):
        """Initialize with a value."""
        self.value = value

    def get_value(self) -> int:
        """Get the stored value."""
        return self.value


class InheritedClass(SimpleClass):
    """A class that inherits from SimpleClass."""

    def __init__(self, value: int, name: str):
        """Initialize with value and name."""
        super().__init__(value)
        self.name = name
'''


class TestT047GetParser:
    """T047: get_parser() returns parser for language."""

    def test_get_parser_python(self):
        """get_parser should return a parser for Python."""
        parser = get_parser("python")

        assert parser is not None, "get_parser('python') should return a parser"

    def test_get_parser_javascript(self):
        """get_parser should return a parser for JavaScript."""
        parser = get_parser("javascript")

        assert parser is not None, "get_parser('javascript') should return a parser"

    def test_get_parser_typescript(self):
        """get_parser should return a parser for TypeScript."""
        parser = get_parser("typescript")

        assert parser is not None, "get_parser('typescript') should return a parser"

    def test_get_parser_go(self):
        """get_parser should return a parser for Go."""
        parser = get_parser("go")

        assert parser is not None, "get_parser('go') should return a parser"

    def test_get_parser_java(self):
        """get_parser should return a parser for Java."""
        parser = get_parser("java")

        assert parser is not None, "get_parser('java') should return a parser"

    def test_get_parser_unsupported_returns_none(self):
        """get_parser should return None for unsupported languages."""
        parser = get_parser("brainfuck")

        assert parser is None, "Unsupported language should return None"


class TestT048ParseFileExtractsFunction:
    """T048: parse_file() extracts functions from Python file."""

    @pytest.mark.asyncio
    async def test_parse_extracts_simple_function(self, tmp_path):
        """parse_file should extract a simple function."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None, "parse_file should return a FileNode"
        assert len(result.functions) > 0, "Should extract functions"

        # Find simple_function
        func_names = [f.name for f in result.functions]
        assert "simple_function" in func_names, "Should find simple_function"

    @pytest.mark.asyncio
    async def test_parse_extracts_function_with_params(self, tmp_path):
        """parse_file should extract function with parameters."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        func_names = [f.name for f in result.functions]
        assert "function_with_params" in func_names


class TestT049ParseFileExtractsClass:
    """T049: parse_file() extracts classes from Python file."""

    @pytest.mark.asyncio
    async def test_parse_extracts_simple_class(self, tmp_path):
        """parse_file should extract a simple class."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None, "parse_file should return a FileNode"
        assert len(result.classes) > 0, "Should extract classes"

        # Find SimpleClass
        class_names = [c.name for c in result.classes]
        assert "SimpleClass" in class_names, "Should find SimpleClass"

    @pytest.mark.asyncio
    async def test_parse_extracts_inherited_class(self, tmp_path):
        """parse_file should extract class with inheritance."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        # Find InheritedClass
        inherited = next(
            (c for c in result.classes if c.name == "InheritedClass"),
            None,
        )
        assert inherited is not None, "Should find InheritedClass"
        assert "SimpleClass" in inherited.parent_classes, "Should have parent class"


class TestT050ParseFileExtractsDocstring:
    """T050: parse_file() extracts docstrings from functions."""

    @pytest.mark.asyncio
    async def test_parse_extracts_function_docstring(self, tmp_path):
        """parse_file should extract function docstrings."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        # Find function_with_params which has a docstring
        func = next(
            (f for f in result.functions if f.name == "function_with_params"),
            None,
        )
        assert func is not None, "Should find function_with_params"
        assert func.docstring is not None, "Should have docstring"
        assert "typed parameters" in func.docstring.lower(), "Docstring should contain description"

    @pytest.mark.asyncio
    async def test_parse_extracts_class_docstring(self, tmp_path):
        """parse_file should extract class docstrings."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        # Find SimpleClass
        cls = next(
            (c for c in result.classes if c.name == "SimpleClass"),
            None,
        )
        assert cls is not None
        assert cls.docstring is not None, "Should have docstring"


class TestT051ParseFileExtractsParameters:
    """T051: parse_file() extracts parameters with types."""

    @pytest.mark.asyncio
    async def test_parse_extracts_typed_parameters(self, tmp_path):
        """parse_file should extract parameter types."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        # Find function_with_params
        func = next(
            (f for f in result.functions if f.name == "function_with_params"),
            None,
        )
        assert func is not None

        # Check parameters
        assert len(func.parameters) >= 2, "Should have at least 2 parameters"

        # Check name parameter
        name_param = next((p for p in func.parameters if p.name == "name"), None)
        assert name_param is not None, "Should have 'name' parameter"
        assert name_param.type == "str", f"name should be str, got {name_param.type}"

        # Check count parameter
        count_param = next((p for p in func.parameters if p.name == "count"), None)
        assert count_param is not None, "Should have 'count' parameter"
        assert count_param.type == "int", f"count should be int, got {count_param.type}"

    @pytest.mark.asyncio
    async def test_parse_extracts_return_type(self, tmp_path):
        """parse_file should extract return types."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        func = next(
            (f for f in result.functions if f.name == "function_with_params"),
            None,
        )
        assert func is not None
        assert func.return_type == "str", f"Return type should be str, got {func.return_type}"

    @pytest.mark.asyncio
    async def test_parse_detects_async_function(self, tmp_path):
        """parse_file should detect async functions."""
        test_file = tmp_path / "test.py"
        test_file.write_text(SAMPLE_PYTHON_CODE)

        result = await parse_file(test_file, "python")

        assert result is not None
        func = next(
            (f for f in result.functions if f.name == "async_function"),
            None,
        )
        assert func is not None, "Should find async_function"
        assert func.is_async is True, "Should be marked as async"


class TestT109EncodingErrors:
    """T109: Parser handles encoding errors gracefully."""

    @pytest.mark.asyncio
    async def test_parse_handles_binary_file(self, tmp_path):
        """parse_file should return None for binary files."""
        test_file = tmp_path / "binary.py"
        # Write binary content that's not valid UTF-8
        test_file.write_bytes(b"\x80\x81\x82\x83\x84\x85")

        result = await parse_file(test_file, "python")

        # Should return None or empty FileNode, not crash
        # Parser should gracefully handle undecodable content
        assert result is None or len(result.functions) == 0

    @pytest.mark.asyncio
    async def test_parse_handles_mixed_encoding(self, tmp_path):
        """parse_file should handle files with mixed encoding."""
        test_file = tmp_path / "mixed.py"
        # Valid Python with non-UTF8 bytes in a comment
        content = b"# Comment with invalid: \xff\xfe\n\ndef valid_func():\n    pass\n"
        test_file.write_bytes(content)

        result = await parse_file(test_file, "python")

        # Should either return None or parse what it can
        # Key: should NOT raise an exception
        assert result is None or isinstance(result.functions, list)

    @pytest.mark.asyncio
    async def test_parse_handles_latin1_encoding(self, tmp_path):
        """parse_file should handle Latin-1 encoded files."""
        test_file = tmp_path / "latin1.py"
        # Latin-1 encoded content with special chars
        content = "# -*- coding: latin-1 -*-\n# Café résumé\ndef hello():\n    pass\n"
        test_file.write_bytes(content.encode("latin-1"))

        result = await parse_file(test_file, "python")

        # Should handle gracefully - either parse or return None
        assert result is None or isinstance(result.functions, list)
