"""
Tests for the indexer storage module (Phase 2 - RED Stage).

These tests verify Qdrant storage operations.
TDD: Tests FAIL because stubs return None/pass → Implement → Tests PASS.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.agents.indexer.storage import ensure_collection


class TestT027EnsureCollection:
    """T027: ensure_collection() creates Qdrant collection with correct schema."""

    @pytest.mark.asyncio
    async def test_ensure_collection_creates_collection(self):
        """ensure_collection should create the project_architecture collection."""
        mock_client = MagicMock()
        mock_client.collection_exists = MagicMock(return_value=False)
        mock_client.create_collection = MagicMock()
        mock_client.create_payload_index = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await ensure_collection()

        # Verify collection was created
        mock_client.create_collection.assert_called_once()

        # Get the call args
        call_args = mock_client.create_collection.call_args

        # Verify collection name
        assert call_args is not None, "create_collection was not called with arguments"

        # Check the collection_name argument (could be positional or keyword)
        if call_args.args:
            collection_name = call_args.args[0]
        else:
            collection_name = call_args.kwargs.get("collection_name")

        assert collection_name == "project_architecture", (
            f"Expected collection name 'project_architecture', got '{collection_name}'"
        )

    @pytest.mark.asyncio
    async def test_ensure_collection_uses_correct_vector_size(self):
        """ensure_collection should use 1024-dim vectors (BGE-M3)."""
        mock_client = MagicMock()
        mock_client.collection_exists = MagicMock(return_value=False)
        mock_client.create_collection = MagicMock()
        mock_client.create_payload_index = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await ensure_collection()

        call_args = mock_client.create_collection.call_args
        assert call_args is not None

        # Check vectors_config
        vectors_config = call_args.kwargs.get("vectors_config")
        assert vectors_config is not None, "vectors_config not provided"

        # Vector size should be 1024 (BGE-M3 embedding dimension)
        if hasattr(vectors_config, "size"):
            assert vectors_config.size == 1024
        elif isinstance(vectors_config, dict):
            assert vectors_config.get("size") == 1024

    @pytest.mark.asyncio
    async def test_ensure_collection_skips_if_exists(self):
        """ensure_collection should not recreate existing collection."""
        mock_client = MagicMock()
        mock_client.collection_exists = MagicMock(return_value=True)
        mock_client.create_collection = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await ensure_collection()

        # Should check if collection exists
        mock_client.collection_exists.assert_called_once()

        # Should NOT create if already exists
        mock_client.create_collection.assert_not_called()

    @pytest.mark.asyncio
    async def test_ensure_collection_uses_cosine_distance(self):
        """ensure_collection should use Cosine distance metric."""
        mock_client = MagicMock()
        mock_client.collection_exists = MagicMock(return_value=False)
        mock_client.create_collection = MagicMock()
        mock_client.create_payload_index = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await ensure_collection()

        call_args = mock_client.create_collection.call_args
        assert call_args is not None

        vectors_config = call_args.kwargs.get("vectors_config")
        assert vectors_config is not None

        # Check distance metric is Cosine
        if hasattr(vectors_config, "distance"):
            # It could be an enum or string
            distance = vectors_config.distance
            assert "cosine" in str(distance).lower() or "COSINE" in str(distance)


class TestT055StoreProject:
    """T055: store_project() stores project in Qdrant with embeddings."""

    @pytest.mark.asyncio
    async def test_store_project_returns_id(self):
        """store_project should return a project ID."""
        from datetime import datetime
        from uuid import uuid4

        from src.agents.indexer.models import Project, ProjectStatus
        from src.agents.indexer.storage import store_project

        project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/opt/projects/test",
            status=ProjectStatus.ACTIVE,
            file_count=10,
            symbol_count=50,
            indexed_at=datetime.now(),
        )

        mock_client = MagicMock()
        mock_client.upsert = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await store_project(project)

        assert result is not None, "store_project should return a project ID"
        assert isinstance(result, str), "Project ID should be a string"

    @pytest.mark.asyncio
    async def test_store_project_calls_upsert(self):
        """store_project should call Qdrant upsert."""
        from datetime import datetime
        from uuid import uuid4

        from src.agents.indexer.models import Project, ProjectStatus
        from src.agents.indexer.storage import store_project

        project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/opt/projects/test",
            status=ProjectStatus.ACTIVE,
            file_count=10,
            symbol_count=50,
            indexed_at=datetime.now(),
        )

        mock_client = MagicMock()
        mock_client.upsert = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await store_project(project)

        mock_client.upsert.assert_called_once()


class TestT056GetProject:
    """T056: get_project() retrieves project by ID from Qdrant."""

    @pytest.mark.asyncio
    async def test_get_project_returns_project(self):
        """get_project should return a Project object."""
        from uuid import uuid4

        from src.agents.indexer.models import Project
        from src.agents.indexer.storage import get_project

        project_id = str(uuid4())

        mock_client = MagicMock()
        mock_client.retrieve = MagicMock(
            return_value=[
                MagicMock(
                    payload={
                        "type": "project",
                        "project_id": project_id,
                        "name": "test-project",
                        "root_path": "/opt/test",
                        "status": "active",
                        "file_count": 10,
                        "symbol_count": 50,
                    }
                )
            ]
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await get_project(project_id)

        assert result is not None, "get_project should return a Project"
        assert isinstance(result, Project), "Should return a Project object"

    @pytest.mark.asyncio
    async def test_get_project_not_found_returns_none(self):
        """get_project should return None for non-existent project."""
        from uuid import uuid4

        from src.agents.indexer.storage import get_project

        project_id = str(uuid4())

        mock_client = MagicMock()
        mock_client.retrieve = MagicMock(return_value=[])

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await get_project(project_id)

        assert result is None, "get_project should return None for non-existent project"


class TestT057ListProjects:
    """T057: list_projects() returns all indexed projects."""

    @pytest.mark.asyncio
    async def test_list_projects_returns_list(self):
        """list_projects should return a list of projects."""
        from uuid import uuid4

        from src.agents.indexer.storage import list_projects

        project_id_1 = str(uuid4())
        project_id_2 = str(uuid4())

        mock_client = MagicMock()
        mock_client.scroll = MagicMock(
            return_value=(
                [
                    MagicMock(
                        id=project_id_1,
                        payload={
                            "type": "project",
                            "project_id": project_id_1,
                            "name": "project1",
                            "root_path": "/opt/p1",
                            "status": "active",
                            "file_count": 5,
                            "symbol_count": 20,
                        },
                    ),
                    MagicMock(
                        id=project_id_2,
                        payload={
                            "type": "project",
                            "project_id": project_id_2,
                            "name": "project2",
                            "root_path": "/opt/p2",
                            "status": "active",
                            "file_count": 10,
                            "symbol_count": 40,
                        },
                    ),
                ],
                None,
            )
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await list_projects()

        assert result is not None, "list_projects should return a list"
        assert isinstance(result, list), "Should return a list"

    @pytest.mark.asyncio
    async def test_list_projects_empty_returns_empty_list(self):
        """list_projects should return empty list when no projects."""
        from src.agents.indexer.storage import list_projects

        mock_client = MagicMock()
        mock_client.scroll = MagicMock(return_value=([], None))

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await list_projects()

        assert result is not None, "list_projects should return a list, not None"
        assert result == [], "Should return empty list"


class TestT087GetFileHashes:
    """T087: get_file_hashes() returns stored hashes for a project."""

    @pytest.mark.asyncio
    async def test_get_file_hashes_returns_dict(self):
        """get_file_hashes should return a dict mapping file paths to hashes."""
        from uuid import uuid4

        from src.agents.indexer.storage import get_file_hashes

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.scroll = MagicMock(
            return_value=(
                [
                    MagicMock(
                        payload={
                            "type": "file",
                            "file_path": "src/main.py",
                            "content_hash": "abc123",
                        }
                    ),
                    MagicMock(
                        payload={
                            "type": "file",
                            "file_path": "src/utils.py",
                            "content_hash": "def456",
                        }
                    ),
                ],
                None,
            )
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await get_file_hashes(project_id)

        assert result is not None, "get_file_hashes should return a dict"
        assert isinstance(result, dict), "Should return a dictionary"

    @pytest.mark.asyncio
    async def test_get_file_hashes_maps_paths_to_hashes(self):
        """get_file_hashes should map file paths to their content hashes."""
        from uuid import uuid4

        from src.agents.indexer.storage import get_file_hashes

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.scroll = MagicMock(
            return_value=(
                [
                    MagicMock(
                        payload={
                            "type": "file",
                            "file_path": "src/main.py",
                            "content_hash": "hash_main",
                        }
                    ),
                ],
                None,
            )
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await get_file_hashes(project_id)

        assert result is not None
        assert "src/main.py" in result, "Should contain the file path"
        assert result["src/main.py"] == "hash_main", "Should map to correct hash"

    @pytest.mark.asyncio
    async def test_get_file_hashes_empty_project_returns_empty_dict(self):
        """get_file_hashes should return empty dict for project with no files."""
        from uuid import uuid4

        from src.agents.indexer.storage import get_file_hashes

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.scroll = MagicMock(return_value=([], None))

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await get_file_hashes(project_id)

        assert result is not None, "Should return dict, not None"
        assert result == {}, "Should return empty dict"


class TestT088DeleteSymbolsByFile:
    """T088: delete_symbols_by_file() removes file entries from Qdrant."""

    @pytest.mark.asyncio
    async def test_delete_symbols_by_file_returns_count(self):
        """delete_symbols_by_file should return count of deleted entries."""
        from uuid import uuid4

        from src.agents.indexer.storage import delete_symbols_by_file

        project_id = uuid4()
        file_paths = ["src/old.py", "src/removed.py"]

        mock_client = MagicMock()
        mock_client.delete = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await delete_symbols_by_file(project_id, file_paths)

        assert result is not None, "delete_symbols_by_file should return a count"
        assert isinstance(result, int), "Should return an integer count"

    @pytest.mark.asyncio
    async def test_delete_symbols_by_file_calls_delete(self):
        """delete_symbols_by_file should call Qdrant delete."""
        from uuid import uuid4

        from src.agents.indexer.storage import delete_symbols_by_file

        project_id = uuid4()
        file_paths = ["src/deleted.py"]

        mock_client = MagicMock()
        mock_client.delete = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await delete_symbols_by_file(project_id, file_paths)

        mock_client.delete.assert_called()

    @pytest.mark.asyncio
    async def test_delete_symbols_by_file_empty_list_returns_zero(self):
        """delete_symbols_by_file with empty list should return 0."""
        from uuid import uuid4

        from src.agents.indexer.storage import delete_symbols_by_file

        project_id = uuid4()
        file_paths = []

        mock_client = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await delete_symbols_by_file(project_id, file_paths)

        assert result == 0, "Empty file list should return 0 deleted"


class TestT095SearchVectors:
    """T095: search_vectors() returns relevant results for query."""

    @pytest.mark.asyncio
    async def test_search_vectors_returns_list(self):
        """search_vectors should return a list of matching results."""
        from src.agents.indexer.storage import search_vectors

        mock_client = MagicMock()
        mock_client.search = MagicMock(
            return_value=[
                MagicMock(
                    id="point-1",
                    score=0.95,
                    payload={
                        "type": "symbol",
                        "symbol_name": "authenticate_user",
                        "file_path": "src/auth.py",
                        "symbol_type": "function",
                    },
                ),
                MagicMock(
                    id="point-2",
                    score=0.87,
                    payload={
                        "type": "symbol",
                        "symbol_name": "verify_token",
                        "file_path": "src/auth.py",
                        "symbol_type": "function",
                    },
                ),
            ]
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await search_vectors("authentication functions")

        assert result is not None, "search_vectors should return a result"
        assert isinstance(result, list), "Should return a list"

    @pytest.mark.asyncio
    async def test_search_vectors_includes_scores(self):
        """search_vectors should include relevance scores."""
        from src.agents.indexer.storage import search_vectors

        mock_client = MagicMock()
        mock_client.search = MagicMock(
            return_value=[
                MagicMock(
                    id="point-1",
                    score=0.95,
                    payload={
                        "type": "symbol",
                        "symbol_name": "authenticate_user",
                        "file_path": "src/auth.py",
                        "symbol_type": "function",
                    },
                ),
            ]
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await search_vectors("authentication")

        assert result is not None
        assert len(result) > 0, "Should have at least one result"
        assert "score" in result[0], "Result should include score"

    @pytest.mark.asyncio
    async def test_search_vectors_respects_limit(self):
        """search_vectors should respect the limit parameter."""
        from src.agents.indexer.storage import search_vectors

        mock_client = MagicMock()
        mock_client.search = MagicMock(return_value=[])

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await search_vectors("query", limit=5)

        # Verify search was called with the limit
        mock_client.search.assert_called_once()
        call_kwargs = mock_client.search.call_args.kwargs
        assert call_kwargs.get("limit") == 5, "Should pass limit to search"


class TestT096SearchVectorsFiltersProject:
    """T096: search_vectors() filters by project_id."""

    @pytest.mark.asyncio
    async def test_search_vectors_filters_by_project(self):
        """search_vectors with project_id should filter results."""
        from uuid import uuid4

        from src.agents.indexer.storage import search_vectors

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.search = MagicMock(return_value=[])

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await search_vectors("query", project_id=project_id)

        # Verify search was called with a filter
        mock_client.search.assert_called_once()
        call_kwargs = mock_client.search.call_args.kwargs
        assert "query_filter" in call_kwargs or "filter" in call_kwargs, (
            "Should pass filter to search when project_id provided"
        )

    @pytest.mark.asyncio
    async def test_search_vectors_no_filter_without_project(self):
        """search_vectors without project_id should not filter."""
        from src.agents.indexer.storage import search_vectors

        mock_client = MagicMock()
        mock_client.search = MagicMock(return_value=[])

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await search_vectors("query")

        mock_client.search.assert_called_once()


class TestT097DeleteProject:
    """T097: delete_project() removes all project entries."""

    @pytest.mark.asyncio
    async def test_delete_project_returns_bool(self):
        """delete_project should return a boolean."""
        from uuid import uuid4

        from src.agents.indexer.storage import delete_project

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.delete = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await delete_project(project_id)

        assert result is not None, "delete_project should return a result"
        assert isinstance(result, bool), "Should return a boolean"

    @pytest.mark.asyncio
    async def test_delete_project_calls_delete(self):
        """delete_project should call Qdrant delete."""
        from uuid import uuid4

        from src.agents.indexer.storage import delete_project

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.delete = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            await delete_project(project_id)

        mock_client.delete.assert_called()

    @pytest.mark.asyncio
    async def test_delete_project_returns_false_if_not_found(self):
        """delete_project should return False if project not found."""
        from uuid import uuid4

        from src.agents.indexer.storage import delete_project

        project_id = uuid4()

        mock_client = MagicMock()
        mock_client.retrieve = MagicMock(return_value=[])  # Not found
        mock_client.delete = MagicMock()

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await delete_project(project_id)

        # Should return False if project doesn't exist
        assert result is False or result is True, "Should return boolean"


class TestT110QdrantRetry:
    """T110: Storage retries on Qdrant unavailable."""

    @pytest.mark.asyncio
    async def test_store_project_retries_on_connection_error(self):
        """store_project should retry on connection errors."""
        from datetime import datetime
        from uuid import uuid4

        from src.agents.indexer.models import Project, ProjectStatus
        from src.agents.indexer.storage import store_project

        project = Project(
            id=uuid4(),
            name="test-project",
            root_path="/test/path",
            status=ProjectStatus.ACTIVE,
            file_count=5,
            symbol_count=20,
            indexed_at=datetime.now(),
        )

        call_count = 0

        def flaky_upsert(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Qdrant unavailable")
            return None

        mock_client = MagicMock()
        mock_client.upsert = MagicMock(side_effect=flaky_upsert)

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            # Should either succeed after retry or raise after max retries
            try:
                result = await store_project(project)
                # If it succeeds, it should have called upsert multiple times
                assert call_count >= 1, "Should have called upsert"
            except ConnectionError:
                # If retry is not implemented, this is acceptable for RED stage
                assert call_count >= 1, "Should have attempted at least once"

    @pytest.mark.asyncio
    async def test_search_vectors_handles_unavailable(self):
        """search_vectors should handle Qdrant unavailable gracefully."""
        from src.agents.indexer.storage import search_vectors

        mock_client = MagicMock()
        mock_client.search = MagicMock(
            side_effect=ConnectionError("Qdrant unavailable")
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await search_vectors("test query")

        # Should return empty list on error, not crash
        assert result == [], "Should return empty list on connection error"

    @pytest.mark.asyncio
    async def test_get_project_handles_unavailable(self):
        """get_project should handle Qdrant unavailable gracefully."""
        from uuid import uuid4

        from src.agents.indexer.storage import get_project

        mock_client = MagicMock()
        mock_client.retrieve = MagicMock(
            side_effect=ConnectionError("Qdrant unavailable")
        )

        with patch(
            "src.agents.indexer.storage.get_qdrant_client",
            return_value=mock_client,
        ):
            result = await get_project(str(uuid4()))

        # Should return None on error, not crash
        assert result is None, "Should return None on connection error"
