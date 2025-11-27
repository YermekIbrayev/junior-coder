"""
Vector storage operations for the Project Architecture Indexer.

Handles Qdrant operations for storing and querying project architecture.
"""

import asyncio
import os
from typing import Callable, Dict, List, Optional, TypeVar
from uuid import UUID

from .models import Project, FileNode


# T114: Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_BASE = 0.5  # seconds

T = TypeVar("T")


async def _with_retry(
    operation: Callable[[], T],
    max_retries: int = MAX_RETRIES,
    delay_base: float = RETRY_DELAY_BASE,
) -> T:
    """
    T114: Execute an operation with exponential backoff retry.

    Args:
        operation: Callable to execute
        max_retries: Maximum number of retry attempts
        delay_base: Base delay in seconds (multiplied exponentially)

    Returns:
        Result of the operation

    Raises:
        Last exception if all retries fail
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            return operation()
        except (ConnectionError, OSError, TimeoutError) as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = delay_base * (2 ** attempt)
                await asyncio.sleep(delay)
            continue
        except Exception as e:
            # Don't retry on other exceptions
            raise e

    # All retries failed
    if last_error:
        raise last_error
    raise RuntimeError("Retry failed without exception")


# Collection name for project architecture data
COLLECTION_NAME = "project_architecture"

# Vector dimensions (BGE-M3 embeddings)
VECTOR_SIZE = 1024

# Qdrant client singleton
_qdrant_client = None


def get_qdrant_client():
    """
    Get or create the Qdrant client.

    Returns:
        QdrantClient instance
    """
    global _qdrant_client

    if _qdrant_client is None:
        from qdrant_client import QdrantClient

        qdrant_url = os.environ.get("QDRANT_URL", "http://localhost:6333")
        _qdrant_client = QdrantClient(url=qdrant_url)

    return _qdrant_client


def _reset_client():
    """Reset the Qdrant client (for testing)."""
    global _qdrant_client
    _qdrant_client = None


async def ensure_collection() -> None:
    """
    T039: Ensure the project_architecture collection exists in Qdrant.

    Creates the collection with correct schema if it doesn't exist:
    - Vector size: 1024 (BGE-M3)
    - Distance: Cosine

    Payload indexes for efficient filtering:
    - project_id: keyword
    - file_path: keyword
    - symbol_type: keyword
    - symbol_name: keyword
    - language: keyword
    - content_hash: keyword
    """
    from qdrant_client.models import Distance, VectorParams

    client = get_qdrant_client()

    # Check if collection already exists
    if client.collection_exists(collection_name=COLLECTION_NAME):
        return

    # Create collection with vector configuration
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )

    # Create payload indexes for efficient filtering
    # Note: Qdrant creates indexes automatically on first query,
    # but explicit creation is more efficient for large datasets
    payload_indexes = [
        "project_id",
        "file_path",
        "symbol_type",
        "symbol_name",
        "language",
        "content_hash",
    ]

    for field_name in payload_indexes:
        try:
            client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field_name,
                field_schema="keyword",
            )
        except Exception:
            # Index might already exist or creation might fail
            # Qdrant will still work, just potentially slower
            pass


async def store_project(project: Project) -> str:
    """
    T079: Store a project in Qdrant.

    Args:
        project: Project metadata

    Returns:
        Project ID as string
    """
    from qdrant_client.models import PointStruct

    client = get_qdrant_client()
    await ensure_collection()

    # Store project as a point with a dummy vector
    # Real embeddings would be generated for searchable content
    project_id_str = str(project.id)

    # Create a point for the project metadata
    point = PointStruct(
        id=project_id_str,
        vector=[0.0] * VECTOR_SIZE,  # Placeholder vector
        payload={
            "type": "project",
            "project_id": project_id_str,
            "name": project.name,
            "root_path": project.root_path,
            "status": project.status.value,
            "file_count": project.file_count,
            "symbol_count": project.symbol_count,
            "indexed_at": (
                project.indexed_at.isoformat() if project.indexed_at else None
            ),
        },
    )

    # T114: Use retry for upsert operation
    await _with_retry(
        lambda: client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point],
        )
    )

    return project_id_str


async def get_project(project_id: str) -> Optional[Project]:
    """
    T080: Retrieve a project by ID.

    Args:
        project_id: UUID string of the project

    Returns:
        Project or None if not found
    """
    from datetime import datetime

    from .models import ProjectStatus

    client = get_qdrant_client()

    try:
        result = client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[project_id],
        )
    except Exception:
        return None

    if not result:
        return None

    payload = result[0].payload
    if payload.get("type") != "project":
        return None

    # Reconstruct the Project from payload
    indexed_at = None
    if payload.get("indexed_at"):
        try:
            indexed_at = datetime.fromisoformat(payload["indexed_at"])
        except (ValueError, TypeError):
            pass

    return Project(
        id=project_id,
        name=payload.get("name", ""),
        root_path=payload.get("root_path", ""),
        status=ProjectStatus(payload.get("status", "active")),
        file_count=payload.get("file_count", 0),
        symbol_count=payload.get("symbol_count", 0),
        indexed_at=indexed_at,
    )


async def list_projects() -> List[Project]:
    """
    T081: List all indexed projects.

    Returns:
        List of all projects
    """
    from datetime import datetime

    from qdrant_client.models import Filter, FieldCondition, MatchValue

    from .models import ProjectStatus

    client = get_qdrant_client()

    try:
        # Scroll through all project-type points
        results, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="type",
                        match=MatchValue(value="project"),
                    )
                ]
            ),
            limit=1000,
        )
    except Exception:
        return []

    projects = []
    for point in results:
        payload = point.payload

        indexed_at = None
        if payload.get("indexed_at"):
            try:
                indexed_at = datetime.fromisoformat(payload["indexed_at"])
            except (ValueError, TypeError):
                pass

        project = Project(
            id=payload.get("project_id", str(point.id)),
            name=payload.get("name", ""),
            root_path=payload.get("root_path", ""),
            status=ProjectStatus(payload.get("status", "active")),
            file_count=payload.get("file_count", 0),
            symbol_count=payload.get("symbol_count", 0),
            indexed_at=indexed_at,
        )
        projects.append(project)

    return projects


async def search_vectors(
    query: str,
    project_id: Optional[UUID] = None,
    limit: int = 10,
) -> List[dict]:
    """
    Search indexed architecture using semantic similarity.

    Args:
        query: Natural language search query
        project_id: Optional project filter
        limit: Maximum results to return

    Returns:
        List of matching symbols with scores
    """
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client = get_qdrant_client()

    # Build query filter if project_id provided
    query_filter = None
    if project_id is not None:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="project_id",
                    match=MatchValue(value=str(project_id)),
                )
            ]
        )

    # For now, use a placeholder vector for the query
    # In production, this would embed the query using BGE-M3
    query_vector = [0.0] * VECTOR_SIZE

    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
        )
    except Exception:
        return []

    # Convert results to dicts
    matches = []
    for point in results:
        match = {
            "id": str(point.id),
            "score": point.score,
            **point.payload,
        }
        matches.append(match)

    return matches


async def delete_project(project_id: UUID) -> bool:
    """
    Delete a project and all its indexed data.

    Args:
        project_id: UUID of the project to delete

    Returns:
        True if deleted, False if not found
    """
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client = get_qdrant_client()
    project_id_str = str(project_id)

    # Check if project exists
    try:
        result = client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[project_id_str],
        )
        if not result:
            return False
    except Exception:
        return False

    # Delete all points for this project (project itself and all its files/symbols)
    try:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="project_id",
                        match=MatchValue(value=project_id_str),
                    )
                ]
            ),
        )
    except Exception:
        return False

    return True


async def get_file_hashes(project_id: UUID) -> Dict[str, str]:
    """
    Get stored content hashes for all files in a project.

    Args:
        project_id: UUID of the project

    Returns:
        Dict mapping file paths to content hashes
    """
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client = get_qdrant_client()

    try:
        # Scroll through all file-type points for this project
        results, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="type",
                        match=MatchValue(value="file"),
                    ),
                    FieldCondition(
                        key="project_id",
                        match=MatchValue(value=str(project_id)),
                    ),
                ]
            ),
            limit=10000,  # Support large projects
        )
    except Exception:
        return {}

    # Build dict mapping file paths to content hashes
    file_hashes: Dict[str, str] = {}
    for point in results:
        payload = point.payload
        file_path = payload.get("file_path")
        content_hash = payload.get("content_hash")
        if file_path and content_hash:
            file_hashes[file_path] = content_hash

    return file_hashes


async def delete_symbols_by_file(
    project_id: UUID,
    file_paths: List[str],
) -> int:
    """
    Delete symbols for specific files.

    Args:
        project_id: UUID of the project
        file_paths: List of file paths to delete symbols for

    Returns:
        Number of symbols deleted
    """
    from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny

    if not file_paths:
        return 0

    client = get_qdrant_client()

    try:
        # Delete all points matching the project and file paths
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="project_id",
                        match=MatchValue(value=str(project_id)),
                    ),
                    FieldCondition(
                        key="file_path",
                        match=MatchAny(any=file_paths),
                    ),
                ]
            ),
        )
    except Exception:
        return 0

    # Return the count of file paths requested for deletion
    # (actual count would require querying before deletion)
    return len(file_paths)
