"""
Filesystem scanner for the Project Architecture Indexer.

Scans directories to find source files, respecting exclude patterns.
"""

import fnmatch
from pathlib import Path
from typing import AsyncIterator, List, Optional, Tuple

from src.agents.indexer.config import SUPPORTED_EXTENSIONS


async def scan_directory(
    root_path: Path,
    exclude_patterns: Optional[List[str]] = None,
    max_file_size: int = 1024 * 1024,  # 1MB default
) -> AsyncIterator[Tuple[Path, str]]:
    """
    T062: Scan a directory for source files.

    Args:
        root_path: Root directory to scan
        exclude_patterns: Glob patterns to exclude
        max_file_size: Maximum file size in bytes (default 1MB)

    Yields:
        Tuples of (file_path, language)
    """
    if exclude_patterns is None:
        exclude_patterns = []

    root = Path(root_path)
    if not root.exists() or not root.is_dir():
        return

    # T112: Track visited real file paths to detect circular symlinks
    visited_files: set = set()

    # Walk directory tree
    for file_path in root.rglob("*"):
        # Skip directories
        if file_path.is_dir():
            continue

        # T112: Handle symlinks - check for circular references
        try:
            # Check if path exists (handles broken symlinks)
            if not file_path.exists():
                continue

            # Resolve to real path for cycle detection
            real_path = file_path.resolve()

            # Check if this real file was already visited (circular symlink)
            if real_path in visited_files:
                continue
            visited_files.add(real_path)

        except (OSError, ValueError):
            # Skip files we can't resolve
            continue

        # T115: Skip files larger than max_file_size
        try:
            if file_path.stat().st_size > max_file_size:
                continue
        except (OSError, ValueError):
            continue

        # Get relative path for pattern matching
        try:
            relative_path = file_path.relative_to(root)
        except ValueError:
            continue

        # Check exclusion patterns
        if should_exclude(relative_path, exclude_patterns):
            continue

        # Detect language
        language = detect_language(file_path)
        if language is not None:
            yield file_path, language


def should_exclude(path: Path, patterns: List[str]) -> bool:
    """
    T060: Check if a path should be excluded based on patterns.

    Uses fnmatch for glob-style pattern matching.

    Args:
        path: Path to check (relative to root)
        patterns: Glob patterns to match against

    Returns:
        True if the path should be excluded
    """
    if not patterns:
        return False

    path_str = str(path)

    for pattern in patterns:
        # Handle patterns like "node_modules/**" and "**/__pycache__/**"
        if fnmatch.fnmatch(path_str, pattern):
            return True

        # Also check each component of the path
        # This handles patterns like ".git/**" matching ".git/objects/abc"
        parts = path.parts
        for i in range(len(parts)):
            partial_path = "/".join(parts[: i + 1])
            # Match patterns that should exclude this directory subtree
            if pattern.endswith("/**"):
                base_pattern = pattern[:-3]  # Remove "/**"
                if fnmatch.fnmatch(partial_path, base_pattern):
                    return True
                # Also try matching just the directory name
                if fnmatch.fnmatch(parts[i], base_pattern):
                    return True

    return False


def detect_language(path: Path) -> Optional[str]:
    """
    T061: Detect the programming language of a file.

    Uses the file extension to determine the language.

    Args:
        path: Path to the file

    Returns:
        Language identifier or None if unsupported
    """
    suffix = path.suffix.lower()
    return SUPPORTED_EXTENSIONS.get(suffix)
