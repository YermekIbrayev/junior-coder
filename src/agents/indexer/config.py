"""
Configuration for the Project Architecture Indexer.

Provides path validation, language mappings, and output directory configuration.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple


# T028: Mapping of file extensions to language identifiers
SUPPORTED_EXTENSIONS: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".java": "java",
}


def _get_allowed_roots() -> List[Path]:
    """
    T029: Get allowed index roots from environment variable.

    Returns:
        List of resolved Path objects for allowed roots
    """
    roots_str = os.environ.get("ALLOWED_INDEX_ROOTS", "/opt/projects")
    roots = [r.strip() for r in roots_str.split(",") if r.strip()]
    return [Path(r).resolve() for r in roots]


def validate_path(path: str) -> Tuple[bool, Optional[str]]:
    """
    T030: Validate that a path is allowed for indexing.

    Checks:
    1. Path doesn't contain traversal sequences (..)
    2. Resolved path is under an allowed root

    Args:
        path: Absolute path to validate

    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    # Check for path traversal in the original path string
    if ".." in path:
        return (False, "Path traversal (..) is not allowed")

    try:
        resolved = Path(path).resolve()
    except (ValueError, OSError) as e:
        return (False, f"Invalid path: {e}")

    # Double-check resolved path doesn't escape (in case of symlinks)
    resolved_str = str(resolved)
    if ".." in resolved_str:
        return (False, "Path traversal detected after resolution")

    # Check against allowed roots
    allowed_roots = _get_allowed_roots()

    for root in allowed_roots:
        try:
            # Check if resolved path is under this root
            resolved.relative_to(root)
            return (True, None)
        except ValueError:
            # Not under this root, try next
            continue

    allowed_str = ", ".join(str(r) for r in allowed_roots)
    return (False, f"Path not under allowed roots: {allowed_str}")


def get_output_dir(project_name: str) -> Path:
    """
    T031: Get the output directory for a project's YAML files.

    Uses INDEXER_OUTPUT_DIR environment variable or defaults to
    /var/lib/vision_model/indexes/{project_name}

    Args:
        project_name: Name of the project

    Returns:
        Path to the output directory
    """
    base_dir = os.environ.get(
        "INDEXER_OUTPUT_DIR",
        "/var/lib/vision_model/indexes",
    )
    return Path(base_dir) / project_name


def get_language_for_extension(extension: str) -> Optional[str]:
    """
    T032: Get the language identifier for a file extension.

    Args:
        extension: File extension including dot (e.g., ".py")

    Returns:
        Language identifier or None if unsupported
    """
    return SUPPORTED_EXTENSIONS.get(extension)
