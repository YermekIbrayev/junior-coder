"""
Tests for the indexer hasher module (Phase 3 - RED Stage).

These tests verify content hashing for change detection.
TDD: Tests FAIL because stubs return None → Implement → Tests PASS.
"""

import tempfile
from pathlib import Path

import pytest

from src.agents.indexer.hasher import (
    compute_file_hash,
    compute_content_hash,
    compare_hashes,
)


class TestT045ComputeFileHashConsistent:
    """T045: compute_file_hash() returns consistent SHA-256 for same content."""

    def test_same_content_same_hash(self):
        """Same content should produce same hash."""
        content = b"def hello():\n    print('world')\n"

        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".py") as f:
            f.write(content)
            path1 = Path(f.name)

        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".py") as f:
            f.write(content)
            path2 = Path(f.name)

        try:
            hash1 = compute_file_hash(path1)
            hash2 = compute_file_hash(path2)

            assert hash1 is not None, "compute_file_hash should return a hash"
            assert hash2 is not None, "compute_file_hash should return a hash"
            assert hash1 == hash2, "Same content should produce same hash"
        finally:
            path1.unlink(missing_ok=True)
            path2.unlink(missing_ok=True)

    def test_hash_is_sha256_hex(self):
        """Hash should be a 64-character hex string (SHA-256)."""
        content = b"test content"

        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(content)
            path = Path(f.name)

        try:
            result = compute_file_hash(path)

            assert result is not None, "compute_file_hash should return a hash"
            assert len(result) == 64, f"SHA-256 should be 64 chars, got {len(result)}"
            assert all(c in "0123456789abcdef" for c in result), "Should be hex string"
        finally:
            path.unlink(missing_ok=True)


class TestT046ComputeFileHashDifferent:
    """T046: compute_file_hash() returns different hash for different content."""

    def test_different_content_different_hash(self):
        """Different content should produce different hashes."""
        content1 = b"def hello():\n    print('world')\n"
        content2 = b"def goodbye():\n    print('world')\n"

        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".py") as f:
            f.write(content1)
            path1 = Path(f.name)

        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".py") as f:
            f.write(content2)
            path2 = Path(f.name)

        try:
            hash1 = compute_file_hash(path1)
            hash2 = compute_file_hash(path2)

            assert hash1 is not None, "compute_file_hash should return a hash"
            assert hash2 is not None, "compute_file_hash should return a hash"
            assert hash1 != hash2, "Different content should produce different hashes"
        finally:
            path1.unlink(missing_ok=True)
            path2.unlink(missing_ok=True)


class TestComputeContentHash:
    """Tests for compute_content_hash function."""

    def test_content_hash_returns_string(self):
        """compute_content_hash should return a hex string."""
        content = b"test content"

        result = compute_content_hash(content)

        assert result is not None, "compute_content_hash should return a hash"
        assert isinstance(result, str), "Should return a string"

    def test_content_hash_consistent(self):
        """Same bytes should produce same hash."""
        content = b"consistent content"

        hash1 = compute_content_hash(content)
        hash2 = compute_content_hash(content)

        assert hash1 == hash2, "Same content should produce same hash"


class TestCompareHashes:
    """Tests for compare_hashes function."""

    def test_compare_detects_added_files(self):
        """compare_hashes should detect added files."""
        current = {"file1.py": "hash1", "file2.py": "hash2", "file3.py": "hash3"}
        stored = {"file1.py": "hash1", "file2.py": "hash2"}

        result = compare_hashes(current, stored)

        assert result is not None, "compare_hashes should return a result"
        added, modified, deleted = result
        assert "file3.py" in added, "Should detect added file"

    def test_compare_detects_modified_files(self):
        """compare_hashes should detect modified files."""
        current = {"file1.py": "hash1_new", "file2.py": "hash2"}
        stored = {"file1.py": "hash1_old", "file2.py": "hash2"}

        result = compare_hashes(current, stored)

        assert result is not None
        added, modified, deleted = result
        assert "file1.py" in modified, "Should detect modified file"

    def test_compare_detects_deleted_files(self):
        """compare_hashes should detect deleted files."""
        current = {"file1.py": "hash1"}
        stored = {"file1.py": "hash1", "file2.py": "hash2"}

        result = compare_hashes(current, stored)

        assert result is not None
        added, modified, deleted = result
        assert "file2.py" in deleted, "Should detect deleted file"
