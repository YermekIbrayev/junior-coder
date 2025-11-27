"""
Content hashing for the Project Architecture Indexer.

Provides SHA-256 hashing for change detection.
"""

import hashlib
from pathlib import Path
from typing import Dict, Optional, Set, Tuple


def compute_file_hash(file_path: Path) -> Optional[str]:
    """
    T063: Compute SHA-256 hash of a file's content.

    Args:
        file_path: Path to the file

    Returns:
        Hexadecimal hash string (64 characters), or None on error
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        return compute_content_hash(content)
    except (OSError, IOError):
        return None


def compute_content_hash(content: bytes) -> str:
    """
    T064: Compute SHA-256 hash of byte content.

    Args:
        content: Bytes to hash

    Returns:
        Hexadecimal hash string (64 characters)
    """
    return hashlib.sha256(content).hexdigest()


def compare_hashes(
    current_hashes: Dict[str, str],
    stored_hashes: Dict[str, str],
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    T090 (US2): Compare current file hashes with stored hashes to detect changes.

    Args:
        current_hashes: Dict mapping file paths to current hashes
        stored_hashes: Dict mapping file paths to stored hashes

    Returns:
        Tuple of (added_files, modified_files, deleted_files)
    """
    current_keys = set(current_hashes.keys())
    stored_keys = set(stored_hashes.keys())

    # Files in current but not in stored = added
    added = current_keys - stored_keys

    # Files in stored but not in current = deleted
    deleted = stored_keys - current_keys

    # Files in both but with different hashes = modified
    common = current_keys & stored_keys
    modified = {
        path for path in common if current_hashes[path] != stored_hashes[path]
    }

    return (added, modified, deleted)
