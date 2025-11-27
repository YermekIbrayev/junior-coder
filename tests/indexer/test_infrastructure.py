"""
Infrastructure Tests for Project Architecture Indexer (Phase 1 - RED Stage)

These tests verify that the indexer module infrastructure exists:
- Directory structure
- Module files
- Required exports
- Function signatures

TDD: These tests FAIL when infrastructure doesn't exist, PASS after creation.
"""

import importlib
import os
from pathlib import Path

import pytest


# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
INDEXER_MODULE_PATH = PROJECT_ROOT / "src" / "agents" / "indexer"


class TestT001DirectoryExists:
    """T001: Assert src/agents/indexer/ directory exists."""

    def test_indexer_directory_exists(self):
        """The indexer module directory must exist."""
        assert INDEXER_MODULE_PATH.exists(), (
            f"Directory does not exist: {INDEXER_MODULE_PATH}"
        )

    def test_indexer_directory_is_directory(self):
        """The path must be a directory, not a file."""
        assert INDEXER_MODULE_PATH.is_dir(), (
            f"Path is not a directory: {INDEXER_MODULE_PATH}"
        )


class TestT002InitExports:
    """T002: Assert __init__.py exports required symbols."""

    def test_init_file_exists(self):
        """The __init__.py file must exist."""
        init_path = INDEXER_MODULE_PATH / "__init__.py"
        assert init_path.exists(), f"__init__.py does not exist: {init_path}"

    def test_indexer_module_importable(self):
        """The indexer module must be importable."""
        try:
            import src.agents.indexer
        except ImportError as e:
            pytest.fail(f"Cannot import src.agents.indexer: {e}")

    def test_exports_indexer_tools(self):
        """INDEXER_TOOLS must be exported from __init__.py."""
        from src.agents.indexer import INDEXER_TOOLS

        assert INDEXER_TOOLS is not None

    def test_exports_dispatch_tool(self):
        """dispatch_tool must be exported from __init__.py."""
        from src.agents.indexer import dispatch_tool

        assert callable(dispatch_tool)

    def test_exports_project_model(self):
        """Project model must be exported from __init__.py."""
        from src.agents.indexer import Project

        assert Project is not None

    def test_exports_file_node_model(self):
        """FileNode model must be exported from __init__.py."""
        from src.agents.indexer import FileNode

        assert FileNode is not None

    def test_exports_function_def_model(self):
        """FunctionDef model must be exported from __init__.py."""
        from src.agents.indexer import FunctionDef

        assert FunctionDef is not None

    def test_exports_class_def_model(self):
        """ClassDef model must be exported from __init__.py."""
        from src.agents.indexer import ClassDef

        assert ClassDef is not None

    def test_exports_validate_path(self):
        """validate_path must be exported from __init__.py."""
        from src.agents.indexer import validate_path

        assert callable(validate_path)


class TestT003ModuleFilesExist:
    """T003: Assert all module files exist."""

    REQUIRED_MODULES = [
        "config.py",
        "models.py",
        "scanner.py",
        "hasher.py",
        "parser.py",
        "storage.py",
        "yaml_writer.py",
        "tools.py",
    ]

    @pytest.mark.parametrize("module_file", REQUIRED_MODULES)
    def test_module_file_exists(self, module_file: str):
        """Each required module file must exist."""
        module_path = INDEXER_MODULE_PATH / module_file
        assert module_path.exists(), f"Module file does not exist: {module_path}"

    @pytest.mark.parametrize("module_file", REQUIRED_MODULES)
    def test_module_file_is_file(self, module_file: str):
        """Each module path must be a file, not a directory."""
        module_path = INDEXER_MODULE_PATH / module_file
        assert module_path.is_file(), f"Path is not a file: {module_path}"


class TestT004FunctionsImportable:
    """T004: Assert all functions can be imported from each module."""

    def test_config_validate_path(self):
        """validate_path must be importable from config."""
        from src.agents.indexer.config import validate_path

        assert callable(validate_path)

    def test_config_get_output_dir(self):
        """get_output_dir must be importable from config."""
        from src.agents.indexer.config import get_output_dir

        assert callable(get_output_dir)

    def test_config_supported_extensions(self):
        """SUPPORTED_EXTENSIONS must be importable from config."""
        from src.agents.indexer.config import SUPPORTED_EXTENSIONS

        assert isinstance(SUPPORTED_EXTENSIONS, dict)

    def test_config_get_language_for_extension(self):
        """get_language_for_extension must be importable from config."""
        from src.agents.indexer.config import get_language_for_extension

        assert callable(get_language_for_extension)

    def test_models_project(self):
        """Project must be importable from models."""
        from src.agents.indexer.models import Project

        assert Project is not None

    def test_models_file_node(self):
        """FileNode must be importable from models."""
        from src.agents.indexer.models import FileNode

        assert FileNode is not None

    def test_models_function_def(self):
        """FunctionDef must be importable from models."""
        from src.agents.indexer.models import FunctionDef

        assert FunctionDef is not None

    def test_models_class_def(self):
        """ClassDef must be importable from models."""
        from src.agents.indexer.models import ClassDef

        assert ClassDef is not None

    def test_models_parameter(self):
        """Parameter must be importable from models."""
        from src.agents.indexer.models import Parameter

        assert Parameter is not None

    def test_models_project_status_enum(self):
        """ProjectStatus enum must be importable from models."""
        from src.agents.indexer.models import ProjectStatus

        assert ProjectStatus is not None

    def test_models_parse_status_enum(self):
        """ParseStatus enum must be importable from models."""
        from src.agents.indexer.models import ParseStatus

        assert ParseStatus is not None

    def test_scanner_scan_directory(self):
        """scan_directory must be importable from scanner."""
        from src.agents.indexer.scanner import scan_directory

        assert callable(scan_directory)

    def test_scanner_should_exclude(self):
        """should_exclude must be importable from scanner."""
        from src.agents.indexer.scanner import should_exclude

        assert callable(should_exclude)

    def test_scanner_detect_language(self):
        """detect_language must be importable from scanner."""
        from src.agents.indexer.scanner import detect_language

        assert callable(detect_language)

    def test_hasher_compute_file_hash(self):
        """compute_file_hash must be importable from hasher."""
        from src.agents.indexer.hasher import compute_file_hash

        assert callable(compute_file_hash)

    def test_hasher_compute_content_hash(self):
        """compute_content_hash must be importable from hasher."""
        from src.agents.indexer.hasher import compute_content_hash

        assert callable(compute_content_hash)

    def test_hasher_compare_hashes(self):
        """compare_hashes must be importable from hasher."""
        from src.agents.indexer.hasher import compare_hashes

        assert callable(compare_hashes)

    def test_parser_parse_file(self):
        """parse_file must be importable from parser."""
        from src.agents.indexer.parser import parse_file

        assert callable(parse_file)

    def test_parser_get_parser(self):
        """get_parser must be importable from parser."""
        from src.agents.indexer.parser import get_parser

        assert callable(get_parser)

    def test_parser_extract_functions(self):
        """extract_functions must be importable from parser."""
        from src.agents.indexer.parser import extract_functions

        assert callable(extract_functions)

    def test_parser_extract_classes(self):
        """extract_classes must be importable from parser."""
        from src.agents.indexer.parser import extract_classes

        assert callable(extract_classes)

    def test_storage_store_project(self):
        """store_project must be importable from storage."""
        from src.agents.indexer.storage import store_project

        assert callable(store_project)

    def test_storage_get_project(self):
        """get_project must be importable from storage."""
        from src.agents.indexer.storage import get_project

        assert callable(get_project)

    def test_storage_search_vectors(self):
        """search_vectors must be importable from storage."""
        from src.agents.indexer.storage import search_vectors

        assert callable(search_vectors)

    def test_storage_delete_project(self):
        """delete_project must be importable from storage."""
        from src.agents.indexer.storage import delete_project

        assert callable(delete_project)

    def test_storage_list_projects(self):
        """list_projects must be importable from storage."""
        from src.agents.indexer.storage import list_projects

        assert callable(list_projects)

    def test_storage_ensure_collection(self):
        """ensure_collection must be importable from storage."""
        from src.agents.indexer.storage import ensure_collection

        assert callable(ensure_collection)

    def test_storage_get_file_hashes(self):
        """get_file_hashes must be importable from storage."""
        from src.agents.indexer.storage import get_file_hashes

        assert callable(get_file_hashes)

    def test_storage_delete_symbols_by_file(self):
        """delete_symbols_by_file must be importable from storage."""
        from src.agents.indexer.storage import delete_symbols_by_file

        assert callable(delete_symbols_by_file)

    def test_yaml_writer_write_project_yaml(self):
        """write_project_yaml must be importable from yaml_writer."""
        from src.agents.indexer.yaml_writer import write_project_yaml

        assert callable(write_project_yaml)

    def test_yaml_writer_write_structure_yaml(self):
        """write_structure_yaml must be importable from yaml_writer."""
        from src.agents.indexer.yaml_writer import write_structure_yaml

        assert callable(write_structure_yaml)

    def test_yaml_writer_write_file_yaml(self):
        """write_file_yaml must be importable from yaml_writer."""
        from src.agents.indexer.yaml_writer import write_file_yaml

        assert callable(write_file_yaml)

    def test_yaml_writer_sanitize_path_for_filename(self):
        """sanitize_path_for_filename must be importable from yaml_writer."""
        from src.agents.indexer.yaml_writer import sanitize_path_for_filename

        assert callable(sanitize_path_for_filename)

    def test_tools_indexer_tools(self):
        """INDEXER_TOOLS must be importable from tools."""
        from src.agents.indexer.tools import INDEXER_TOOLS

        assert isinstance(INDEXER_TOOLS, list)

    def test_tools_dispatch_tool(self):
        """dispatch_tool must be importable from tools."""
        from src.agents.indexer.tools import dispatch_tool

        assert callable(dispatch_tool)

    def test_tools_handle_index_project(self):
        """handle_index_project must be importable from tools."""
        from src.agents.indexer.tools import handle_index_project

        assert callable(handle_index_project)

    def test_tools_handle_update_project(self):
        """handle_update_project must be importable from tools."""
        from src.agents.indexer.tools import handle_update_project

        assert callable(handle_update_project)

    def test_tools_handle_search_architecture(self):
        """handle_search_architecture must be importable from tools."""
        from src.agents.indexer.tools import handle_search_architecture

        assert callable(handle_search_architecture)

    def test_tools_handle_list_projects(self):
        """handle_list_projects must be importable from tools."""
        from src.agents.indexer.tools import handle_list_projects

        assert callable(handle_list_projects)

    def test_tools_handle_delete_project(self):
        """handle_delete_project must be importable from tools."""
        from src.agents.indexer.tools import handle_delete_project

        assert callable(handle_delete_project)
