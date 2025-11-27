"""
LLM tool definitions and handlers for the Project Architecture Indexer.

Exposes indexer functionality as tools for LLM function calling.
"""

from typing import Any, Callable, Dict, List, Optional


# Tool definitions for LLM function calling (OpenAI format)
INDEXER_TOOLS: List[dict] = [
    {
        "type": "function",
        "function": {
            "name": "index_project",
            "description": "Index a codebase to understand its architecture",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to project directory",
                    },
                    "exclude_patterns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Glob patterns to exclude (optional)",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_project_index",
            "description": "Update index for changed files in a project",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project identifier (UUID)",
                    },
                    "force_full": {
                        "type": "boolean",
                        "description": "Force full re-index instead of incremental",
                    },
                },
                "required": ["project_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_architecture",
            "description": "Search indexed project architecture",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query",
                    },
                    "project_id": {
                        "type": "string",
                        "description": "Project to search (optional, searches all if omitted)",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_indexed_projects",
            "description": "List all indexed projects",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_project_index",
            "description": "Remove a project from the index",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "Project identifier (UUID)",
                    },
                },
                "required": ["project_id"],
            },
        },
    },
]


async def handle_index_project(
    path: str,
    exclude_patterns: Optional[List[str]] = None,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    """
    Handle the index_project tool call.

    Args:
        path: Absolute path to project directory
        exclude_patterns: Glob patterns to exclude
        progress_callback: Optional callback for progress updates

    Returns:
        Dict with project_id and statistics
    """
    from datetime import datetime
    from pathlib import Path as PathLib
    from uuid import uuid4

    from .models import Project, ProjectStatus
    from .parser import parse_file
    from .scanner import scan_directory
    from .storage import store_project
    from .yaml_writer import write_file_yaml, write_project_yaml, write_structure_yaml

    # Security: Reject path traversal (paths containing ..) BEFORE resolving
    if ".." in path:
        return {"error": "Path traversal not allowed", "status": "error"}

    # Validate path exists
    try:
        project_path = PathLib(path).resolve()
    except Exception:
        return {"error": "Invalid path", "status": "error"}

    if not project_path.exists():
        return {"error": "Path does not exist", "status": "error"}

    if not project_path.is_dir():
        return {"error": "Path is not a directory", "status": "error"}

    def report_progress(msg: str) -> None:
        if progress_callback:
            progress_callback(msg)

    report_progress(f"Starting indexing of {path}")

    # Build exclude patterns list
    default_excludes = [
        ".git/**",
        "node_modules/**",
        "__pycache__/**",
        "*.pyc",
        ".venv/**",
        "venv/**",
        "dist/**",
        "build/**",
    ]
    all_excludes = list(set(default_excludes + (exclude_patterns or [])))

    # Scan directory for files
    report_progress("Scanning directory...")
    files = []
    file_count = 0
    symbol_count = 0

    async for file_path, language in scan_directory(project_path, all_excludes):
        file_node = await parse_file(file_path, language)
        if file_node:
            # Make path relative
            try:
                file_node.relative_path = str(file_path.relative_to(project_path))
            except ValueError:
                file_node.relative_path = str(file_path)
            files.append(file_node)
            file_count += 1
            symbol_count += len(file_node.functions) + len(file_node.classes)
            report_progress(f"Parsed {file_node.relative_path}")

    report_progress(f"Found {file_count} files with {symbol_count} symbols")

    # Create project
    project = Project(
        id=uuid4(),
        name=project_path.name,
        root_path=str(project_path),
        status=ProjectStatus.ACTIVE,
        file_count=file_count,
        symbol_count=symbol_count,
        indexed_at=datetime.now(),
    )

    # Store in Qdrant
    report_progress("Storing project in vector database...")
    project_id = await store_project(project)

    # Write YAML output
    output_dir = project_path / ".agents" / "architecture"
    report_progress(f"Writing YAML output to {output_dir}")

    await write_project_yaml(project, output_dir)
    await write_structure_yaml(project, files, output_dir)
    for file_node in files:
        await write_file_yaml(file_node, output_dir)

    report_progress("Indexing complete!")

    return {
        "project_id": project_id,
        "status": "success",
        "file_count": file_count,
        "files_indexed": file_count,
        "symbol_count": symbol_count,
        "output_dir": str(output_dir),
    }


async def handle_update_project(
    project_id: str,
    force_full: bool = False,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    """
    Handle the update_project_index tool call.

    Args:
        project_id: UUID of project to update
        force_full: Force full re-index
        progress_callback: Optional callback for progress updates

    Returns:
        Dict with update statistics
    """
    from pathlib import Path as PathLib

    from .hasher import compare_hashes, compute_file_hash
    from .models import ProjectStatus
    from .parser import parse_file
    from .scanner import scan_directory
    from .storage import (
        delete_symbols_by_file,
        get_file_hashes,
        get_project,
        store_project,
    )
    from .yaml_writer import write_file_yaml, write_project_yaml, write_structure_yaml

    def report_progress(msg: str) -> None:
        if progress_callback:
            progress_callback(msg)

    # Get the existing project
    project = await get_project(project_id)
    if project is None:
        return {"status": "error", "error": f"Project not found: {project_id}"}

    project_path = PathLib(project.root_path)
    if not project_path.exists():
        return {"status": "error", "error": f"Project path no longer exists: {project.root_path}"}

    report_progress(f"Updating project: {project.name}")

    # Get stored file hashes
    stored_hashes = await get_file_hashes(project.id)
    report_progress(f"Found {len(stored_hashes)} previously indexed files")

    # Scan current files and compute new hashes
    current_hashes: Dict[str, str] = {}
    default_excludes = [
        ".git/**",
        "node_modules/**",
        "__pycache__/**",
        "*.pyc",
        ".venv/**",
        "venv/**",
        "dist/**",
        "build/**",
    ]

    report_progress("Scanning for changes...")
    async for file_path, language in scan_directory(project_path, default_excludes):
        try:
            relative_path = str(file_path.relative_to(project_path))
            content_hash = compute_file_hash(file_path)
            current_hashes[relative_path] = content_hash
        except (ValueError, OSError):
            continue

    # Compare hashes to detect changes
    if force_full:
        # Force full re-index: treat all files as added
        added = set(current_hashes.keys())
        modified = set()
        deleted = set()
        report_progress("Force full re-index requested")
    else:
        added, modified, deleted = compare_hashes(stored_hashes, current_hashes)

    report_progress(f"Changes: {len(added)} added, {len(modified)} modified, {len(deleted)} deleted")

    # Delete symbols for removed and modified files
    files_to_remove = list(deleted | modified)
    if files_to_remove:
        await delete_symbols_by_file(project.id, files_to_remove)
        report_progress(f"Removed {len(files_to_remove)} file entries")

    # Re-index added and modified files
    files_to_index = added | modified
    files = []
    file_count = 0
    symbol_count = 0

    for relative_path in files_to_index:
        file_path = project_path / relative_path
        if not file_path.exists():
            continue

        # Determine language from extension
        ext = file_path.suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "tsx",
            ".jsx": "jsx",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
        }
        language = language_map.get(ext)
        if not language:
            continue

        file_node = await parse_file(file_path, language)
        if file_node:
            file_node.relative_path = relative_path
            files.append(file_node)
            file_count += 1
            symbol_count += len(file_node.functions) + len(file_node.classes)
            report_progress(f"Re-indexed {relative_path}")

    # Update project metadata
    from datetime import datetime

    project.file_count = len(current_hashes)
    project.symbol_count = symbol_count
    project.indexed_at = datetime.now()
    project.status = ProjectStatus.ACTIVE

    await store_project(project)

    # Write updated YAML output
    output_dir = project_path / ".agents" / "architecture"
    report_progress(f"Writing YAML output to {output_dir}")

    await write_project_yaml(project, output_dir)

    report_progress("Update complete!")

    return {
        "status": "success",
        "project_id": project_id,
        "added": len(added),
        "modified": len(modified),
        "deleted": len(deleted),
        "files_processed": file_count,
        "symbol_count": symbol_count,
    }


async def handle_search_architecture(
    query: str,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Handle the search_architecture tool call.

    Args:
        query: Natural language search query
        project_id: Optional project filter

    Returns:
        Dict with search results
    """
    from uuid import UUID

    from .storage import search_vectors

    try:
        # Convert project_id to UUID if provided
        project_uuid = UUID(project_id) if project_id else None

        results = await search_vectors(
            query=query,
            project_id=project_uuid,
            limit=10,
        )

        return {
            "status": "success",
            "query": query,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "results": [],
        }


async def handle_list_projects() -> Dict[str, Any]:
    """
    Handle the list_indexed_projects tool call.

    Returns:
        Dict with list of projects
    """
    from .storage import list_projects

    try:
        projects = await list_projects()

        project_list = []
        for project in projects:
            project_list.append({
                "project_id": str(project.id),
                "name": project.name,
                "root_path": project.root_path,
                "status": project.status.value,
                "file_count": project.file_count,
                "symbol_count": project.symbol_count,
                "indexed_at": (
                    project.indexed_at.isoformat() if project.indexed_at else None
                ),
            })

        return {
            "status": "success",
            "projects": project_list,
            "count": len(project_list),
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "projects": [],
        }


async def handle_delete_project(project_id: str) -> Dict[str, Any]:
    """
    Handle the delete_project_index tool call.

    Args:
        project_id: UUID of project to delete

    Returns:
        Dict with deletion status
    """
    from uuid import UUID

    from .storage import delete_project

    try:
        project_uuid = UUID(project_id)
        deleted = await delete_project(project_uuid)

        if deleted:
            return {
                "status": "success",
                "message": f"Project {project_id} deleted successfully",
                "project_id": project_id,
            }
        else:
            return {
                "status": "error",
                "error": f"Project not found: {project_id}",
            }
    except ValueError:
        return {
            "status": "error",
            "error": f"Invalid project ID: {project_id}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }


async def dispatch_tool(
    tool_name: str,
    arguments: Dict[str, Any],
    progress_callback: Optional[Callable[[str], None]] = None,
) -> Dict[str, Any]:
    """
    Dispatch a tool call to the appropriate handler.

    Args:
        tool_name: Name of the tool to invoke
        arguments: Tool arguments
        progress_callback: Optional progress callback

    Returns:
        Tool result dict
    """
    if tool_name == "index_project":
        return await handle_index_project(
            path=arguments.get("path", ""),
            exclude_patterns=arguments.get("exclude_patterns"),
            progress_callback=progress_callback,
        )
    elif tool_name == "update_project_index":
        return await handle_update_project(
            project_id=arguments.get("project_id", ""),
            force_full=arguments.get("force_full", False),
            progress_callback=progress_callback,
        )
    elif tool_name == "search_architecture":
        return await handle_search_architecture(
            query=arguments.get("query", ""),
            project_id=arguments.get("project_id"),
        )
    elif tool_name == "list_indexed_projects":
        return await handle_list_projects()
    elif tool_name == "delete_project_index":
        return await handle_delete_project(
            project_id=arguments.get("project_id", ""),
        )
    else:
        return {
            "status": "error",
            "error": f"Unknown tool: {tool_name}",
        }
