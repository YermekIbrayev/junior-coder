"""
YAML output generation for the Project Architecture Indexer.

Writes project structure and symbols to YAML files.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .models import FileNode, Project


def sanitize_path_for_filename(path: str) -> str:
    """
    T074: Convert a file path to a safe filename.

    Replaces path separators with underscores.

    Args:
        path: Original file path

    Returns:
        Sanitized filename string
    """
    # Replace forward slashes with underscores
    return path.replace("/", "_").replace("\\", "_")


def _build_folder_hierarchy(files: List[FileNode]) -> List[Dict[str, Any]]:
    """
    T075: Build a hierarchical folder structure from a flat list of files.
    """
    # Build a tree structure
    root: Dict[str, Any] = {"children": {}}

    for file in files:
        parts = file.relative_path.split("/")
        current = root

        # Navigate/create directories
        for i, part in enumerate(parts[:-1]):
            if part not in current["children"]:
                current["children"][part] = {
                    "path": "/".join(parts[: i + 1]),
                    "type": "directory",
                    "children": {},
                }
            current = current["children"][part]

        # Add the file
        filename = parts[-1]
        current["children"][filename] = {
            "path": file.relative_path,
            "type": "file",
            "language": file.language,
            "size_bytes": file.size_bytes,
            "symbols": len(file.functions) + len(file.classes),
        }

    # Convert to list format
    def convert_to_list(node: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = []
        for name, data in sorted(node.get("children", {}).items()):
            item: Dict[str, Any] = {
                "path": data["path"],
                "type": data["type"],
            }
            if data["type"] == "directory":
                item["children"] = convert_to_list(data)
            else:
                item["language"] = data["language"]
                item["size_bytes"] = data["size_bytes"]
                item["symbols"] = data["symbols"]
            result.append(item)
        return result

    return convert_to_list(root)


async def write_project_yaml(
    project: Project,
    output_dir: Path,
) -> Optional[Path]:
    """
    T076: Write project metadata to project.yaml.

    Args:
        project: Project to write
        output_dir: Output directory

    Returns:
        Path to the written file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "project": {
            "id": str(project.id),
            "name": project.name,
            "root_path": project.root_path,
            "indexed_at": (
                project.indexed_at.isoformat() if project.indexed_at else None
            ),
            "statistics": {
                "total_files": project.file_count,
                "total_symbols": project.symbol_count,
            },
            "status": project.status.value,
            "config": project.config,
        }
    }

    output_path = output_dir / "project.yaml"
    with open(output_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    return output_path


async def write_structure_yaml(
    project: Project,
    files: List[FileNode],
    output_dir: Path,
) -> Optional[Path]:
    """
    T077: Write project structure to structure.yaml.

    Args:
        project: Project metadata
        files: List of files
        output_dir: Output directory

    Returns:
        Path to the written file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    structure = _build_folder_hierarchy(files)

    data = {"structure": structure}

    output_path = output_dir / "structure.yaml"
    with open(output_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    return output_path


async def write_file_yaml(
    file_node: FileNode,
    output_dir: Path,
) -> Optional[Path]:
    """
    T078: Write a file's symbols to YAML.

    Args:
        file_node: File with extracted symbols
        output_dir: Output directory

    Returns:
        Path to the written file
    """
    output_dir = Path(output_dir)
    files_dir = output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    # Build function data
    functions_data = []
    for func in file_node.functions:
        func_dict: Dict[str, Any] = {
            "name": func.name,
            "line": func.line_number,
            "signature": func.signature,
        }
        if func.parameters:
            func_dict["parameters"] = [
                {
                    "name": p.name,
                    "type": p.type,
                    "default": p.default,
                }
                for p in func.parameters
                if p.name not in ("self", "cls")
            ]
        if func.return_type:
            func_dict["return_type"] = func.return_type
        if func.docstring:
            func_dict["docstring"] = func.docstring
        if func.is_async:
            func_dict["is_async"] = True
        functions_data.append(func_dict)

    # Build class data
    classes_data = []
    for cls in file_node.classes:
        cls_dict: Dict[str, Any] = {
            "name": cls.name,
            "line": cls.line_number,
        }
        if cls.parent_classes:
            cls_dict["parent_classes"] = cls.parent_classes
        if cls.docstring:
            cls_dict["docstring"] = cls.docstring
        if cls.method_names:
            cls_dict["methods"] = cls.method_names
        classes_data.append(cls_dict)

    data = {
        "file": {
            "path": file_node.relative_path,
            "language": file_node.language,
            "size_bytes": file_node.size_bytes,
            "content_hash": file_node.content_hash,
        },
        "functions": functions_data,
        "classes": classes_data,
    }

    # Create filename from path
    filename = sanitize_path_for_filename(file_node.relative_path) + ".yaml"
    output_path = files_dir / filename

    with open(output_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    return output_path
