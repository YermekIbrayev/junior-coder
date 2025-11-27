"""
Project Architecture Indexer

Multi-language code indexing system that parses codebase structure using tree-sitter,
generates YAML architecture files, and stores semantic embeddings in Qdrant.

Exposed as internal LLM tools via existing OpenAI-compatible chat completions.
"""

# Config exports
from .config import (
    SUPPORTED_EXTENSIONS,
    validate_path,
    get_output_dir,
    get_language_for_extension,
)

# Model exports
from .models import (
    Project,
    FileNode,
    FunctionDef,
    ClassDef,
    Parameter,
    ProjectStatus,
    ParseStatus,
)

# Scanner exports
from .scanner import (
    scan_directory,
    should_exclude,
    detect_language,
)

# Hasher exports
from .hasher import (
    compute_file_hash,
    compute_content_hash,
    compare_hashes,
)

# Parser exports
from .parser import (
    parse_file,
    get_parser,
    extract_functions,
    extract_classes,
)

# Storage exports
from .storage import (
    ensure_collection,
    store_project,
    get_project,
    list_projects,
    search_vectors,
    delete_project,
    get_file_hashes,
    delete_symbols_by_file,
)

# YAML writer exports
from .yaml_writer import (
    write_project_yaml,
    write_structure_yaml,
    write_file_yaml,
    sanitize_path_for_filename,
)

# Tool exports
from .tools import (
    INDEXER_TOOLS,
    dispatch_tool,
    handle_index_project,
    handle_update_project,
    handle_search_architecture,
    handle_list_projects,
    handle_delete_project,
)

# Logging exports
from .logging import (
    configure_logging,
    log_operation,
    log_timing,
)

__all__ = [
    # Config
    "SUPPORTED_EXTENSIONS",
    "validate_path",
    "get_output_dir",
    "get_language_for_extension",
    # Models
    "Project",
    "FileNode",
    "FunctionDef",
    "ClassDef",
    "Parameter",
    "ProjectStatus",
    "ParseStatus",
    # Scanner
    "scan_directory",
    "should_exclude",
    "detect_language",
    # Hasher
    "compute_file_hash",
    "compute_content_hash",
    "compare_hashes",
    # Parser
    "parse_file",
    "get_parser",
    "extract_functions",
    "extract_classes",
    # Storage
    "ensure_collection",
    "store_project",
    "get_project",
    "list_projects",
    "search_vectors",
    "delete_project",
    "get_file_hashes",
    "delete_symbols_by_file",
    # YAML Writer
    "write_project_yaml",
    "write_structure_yaml",
    "write_file_yaml",
    "sanitize_path_for_filename",
    # Tools
    "INDEXER_TOOLS",
    "dispatch_tool",
    "handle_index_project",
    "handle_update_project",
    "handle_search_architecture",
    "handle_list_projects",
    "handle_delete_project",
    # Logging
    "configure_logging",
    "log_operation",
    "log_timing",
]
