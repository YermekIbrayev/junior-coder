"""
AST parser for the Project Architecture Indexer.

Uses tree-sitter for multi-language code parsing.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

import tree_sitter_languages

from .hasher import compute_content_hash
from .models import ClassDef, FileNode, FunctionDef, Parameter, ParseStatus


# Language mapping for tree-sitter-languages
LANGUAGE_MAP = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "go": "go",
    "java": "java",
}


def get_parser(language: str) -> Optional[Any]:
    """
    T065: Get a tree-sitter parser for a language.

    Args:
        language: Language identifier (e.g., "python", "javascript")

    Returns:
        Tree-sitter parser or None if unsupported
    """
    ts_lang = LANGUAGE_MAP.get(language)
    if ts_lang is None:
        return None

    try:
        return tree_sitter_languages.get_parser(ts_lang)
    except Exception:
        return None


def _get_node_text(node: Any, source_code: bytes) -> str:
    """Extract text from a tree-sitter node."""
    return source_code[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def _get_docstring(node: Any, source_code: bytes, language: str) -> Optional[str]:
    """
    T066: Extract docstring from a function or class node.
    """
    if language != "python":
        return None

    # For Python, docstring is the first statement if it's a string
    for child in node.children:
        if child.type == "block":
            for stmt in child.children:
                if stmt.type == "expression_statement":
                    for expr in stmt.children:
                        if expr.type == "string":
                            text = _get_node_text(expr, source_code)
                            # Remove quotes
                            if text.startswith('"""') or text.startswith("'''"):
                                return text[3:-3].strip()
                            elif text.startswith('"') or text.startswith("'"):
                                return text[1:-1].strip()
                    break
                elif stmt.type not in ("comment", "pass_statement"):
                    break
            break
    return None


def _get_function_signature(
    node: Any, source_code: bytes, language: str
) -> tuple[str, List[Parameter], Optional[str], bool]:
    """
    T067: Build function signature string and extract parameters.

    Returns:
        Tuple of (signature, parameters, return_type, is_async)
    """
    name = ""
    params: List[Parameter] = []
    return_type: Optional[str] = None
    is_async = False

    if language == "python":
        # Check if async
        for child in node.children:
            if child.type == "async":
                is_async = True
            elif child.type == "name":
                name = _get_node_text(child, source_code)
            elif child.type == "parameters":
                params = _extract_python_params(child, source_code)
            elif child.type == "type":
                return_type = _get_node_text(child, source_code)

        # Build signature
        param_strs = []
        for p in params:
            s = p.name
            if p.type:
                s += f": {p.type}"
            if p.default:
                s += f" = {p.default}"
            param_strs.append(s)

        sig = f"def {name}({', '.join(param_strs)})"
        if return_type:
            sig += f" -> {return_type}"

        if is_async:
            sig = "async " + sig

    else:
        # Generic handling for other languages
        sig = _get_node_text(node, source_code).split("{")[0].strip()

    return sig, params, return_type, is_async


def _extract_python_params(params_node: Any, source_code: bytes) -> List[Parameter]:
    """Extract parameters from a Python parameters node."""
    params: List[Parameter] = []

    for child in params_node.children:
        if child.type in ("identifier", "typed_parameter", "default_parameter",
                          "typed_default_parameter"):
            param = _parse_python_param(child, source_code)
            if param and param.name not in ("self", "cls"):
                params.append(param)
        elif child.type == "list_splat_pattern":
            # *args
            for c in child.children:
                if c.type == "identifier":
                    params.append(Parameter(
                        name=_get_node_text(c, source_code),
                        is_variadic=True
                    ))
        elif child.type == "dictionary_splat_pattern":
            # **kwargs
            for c in child.children:
                if c.type == "identifier":
                    params.append(Parameter(
                        name=_get_node_text(c, source_code),
                        is_variadic=True
                    ))

    return params


def _parse_python_param(node: Any, source_code: bytes) -> Optional[Parameter]:
    """Parse a single Python parameter."""
    if node.type == "identifier":
        return Parameter(name=_get_node_text(node, source_code))

    name = None
    type_str = None
    default = None

    for child in node.children:
        if child.type == "identifier":
            name = _get_node_text(child, source_code)
        elif child.type == "type":
            type_str = _get_node_text(child, source_code)
        elif child.type not in (":", "="):
            if name is not None and type_str is None and child.type != "type":
                # This might be a default value
                default = _get_node_text(child, source_code)

    if name:
        return Parameter(name=name, type=type_str, default=default)
    return None


def extract_functions(
    tree: Any,
    source_code: bytes,
    language: str,
) -> List[FunctionDef]:
    """
    T068: Extract function definitions from a parsed AST.

    Args:
        tree: Parsed tree-sitter tree
        source_code: Original source code bytes
        language: Language identifier

    Returns:
        List of FunctionDef models
    """
    functions: List[FunctionDef] = []

    if language == "python":
        node_types = ("function_definition",)
    elif language in ("javascript", "typescript"):
        node_types = ("function_declaration", "arrow_function", "method_definition")
    elif language == "go":
        node_types = ("function_declaration", "method_declaration")
    elif language == "java":
        node_types = ("method_declaration",)
    else:
        return functions

    def visit(node: Any, parent_class: Optional[str] = None):
        if node.type in node_types:
            func = _extract_function(node, source_code, language, parent_class)
            if func:
                functions.append(func)
        else:
            # Track parent class for methods
            new_parent = parent_class
            if node.type == "class_definition" and language == "python":
                for child in node.children:
                    if child.type == "name":
                        new_parent = _get_node_text(child, source_code)
                        break

            for child in node.children:
                visit(child, new_parent)

    visit(tree.root_node)
    return functions


def _extract_function(
    node: Any,
    source_code: bytes,
    language: str,
    parent_class: Optional[str] = None,
) -> Optional[FunctionDef]:
    """Extract a single function definition."""
    sig, params, return_type, is_async = _get_function_signature(
        node, source_code, language
    )

    # Extract name
    name = ""
    for child in node.children:
        if child.type in ("name", "identifier"):
            name = _get_node_text(child, source_code)
            break

    if not name:
        return None

    docstring = _get_docstring(node, source_code, language)

    return FunctionDef(
        name=name,
        line_number=node.start_point[0] + 1,  # 1-indexed
        end_line=node.end_point[0] + 1,
        signature=sig,
        parameters=params,
        return_type=return_type,
        docstring=docstring,
        is_async=is_async,
        is_method=parent_class is not None,
        parent_class=parent_class,
    )


def extract_classes(
    tree: Any,
    source_code: bytes,
    language: str,
) -> List[ClassDef]:
    """
    T069: Extract class definitions from a parsed AST.

    Args:
        tree: Parsed tree-sitter tree
        source_code: Original source code bytes
        language: Language identifier

    Returns:
        List of ClassDef models
    """
    classes: List[ClassDef] = []

    if language == "python":
        node_type = "class_definition"
    elif language in ("javascript", "typescript"):
        node_type = "class_declaration"
    elif language == "java":
        node_type = "class_declaration"
    elif language == "go":
        # Go doesn't have classes, uses structs
        return classes
    else:
        return classes

    def visit(node: Any):
        if node.type == node_type:
            cls = _extract_class(node, source_code, language)
            if cls:
                classes.append(cls)
        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return classes


def _extract_class(
    node: Any,
    source_code: bytes,
    language: str,
) -> Optional[ClassDef]:
    """Extract a single class definition."""
    name = ""
    parent_classes: List[str] = []
    method_names: List[str] = []

    if language == "python":
        for child in node.children:
            if child.type == "identifier":
                # Class name is an identifier in Python
                name = _get_node_text(child, source_code)
            elif child.type == "argument_list":
                # Parent classes
                for arg in child.children:
                    if arg.type == "identifier":
                        parent_classes.append(_get_node_text(arg, source_code))
            elif child.type == "block":
                # Extract method names
                for stmt in child.children:
                    if stmt.type == "function_definition":
                        for fc in stmt.children:
                            if fc.type == "identifier":
                                method_names.append(_get_node_text(fc, source_code))
                                break

    if not name:
        return None

    docstring = _get_docstring(node, source_code, language)

    return ClassDef(
        name=name,
        line_number=node.start_point[0] + 1,
        end_line=node.end_point[0] + 1,
        parent_classes=parent_classes,
        docstring=docstring,
        method_names=method_names,
    )


async def parse_file(file_path: Path, language: str) -> Optional[FileNode]:
    """
    T070: Parse a source file and extract symbols.

    Args:
        file_path: Path to the source file
        language: Language identifier

    Returns:
        FileNode with extracted functions and classes, or None on error
    """
    parser = get_parser(language)
    if parser is None:
        return None

    try:
        source_code = file_path.read_bytes()
    except (OSError, IOError):
        return None

    # T113: Handle encoding errors gracefully
    # Check if content is likely binary (non-text) by looking for null bytes
    if b"\x00" in source_code[:8192]:  # Check first 8KB for null bytes
        return None  # Skip binary files

    # Try to decode for validation (tree-sitter works with bytes)
    # This helps detect files with invalid encoding
    try:
        # Try UTF-8 first, then fallback to latin-1
        try:
            source_code.decode("utf-8")
        except UnicodeDecodeError:
            try:
                source_code.decode("latin-1")
            except UnicodeDecodeError:
                return None  # Can't decode, skip file
    except Exception:
        return None

    try:
        tree = parser.parse(source_code)
    except Exception:
        return FileNode(
            relative_path=str(file_path),
            language=language,
            content_hash=compute_content_hash(source_code),
            size_bytes=len(source_code),
            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
            parse_status=ParseStatus.ERROR,
            error_message="Failed to parse AST",
        )

    functions = extract_functions(tree, source_code, language)
    classes = extract_classes(tree, source_code, language)

    return FileNode(
        relative_path=str(file_path),
        language=language,
        content_hash=compute_content_hash(source_code),
        size_bytes=len(source_code),
        last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
        parse_status=ParseStatus.SUCCESS,
        functions=functions,
        classes=classes,
    )
