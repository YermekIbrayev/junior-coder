"""
Data models for the Project Architecture Indexer.

Defines Pydantic models for projects, files, functions, and classes.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ProjectStatus(str, Enum):
    """Status of a project in the index."""

    ACTIVE = "active"
    INDEXING = "indexing"
    ERROR = "error"


class ParseStatus(str, Enum):
    """Status of parsing a file."""

    SUCCESS = "success"
    SKIPPED = "skipped"
    ERROR = "error"


class Parameter(BaseModel):
    """Represents a function parameter."""

    name: str
    type: Optional[str] = None
    default: Optional[str] = None
    is_variadic: bool = False


class FunctionDef(BaseModel):
    """Represents a function or method definition."""

    id: UUID = Field(default_factory=uuid4)
    file_id: Optional[UUID] = None
    name: str
    line_number: int
    end_line: Optional[int] = None
    signature: str
    parameters: List[Parameter] = Field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    is_async: bool = False
    is_method: bool = False
    parent_class: Optional[str] = None
    decorators: List[str] = Field(default_factory=list)


class ClassDef(BaseModel):
    """Represents a class definition."""

    id: UUID = Field(default_factory=uuid4)
    file_id: Optional[UUID] = None
    name: str
    line_number: int
    end_line: Optional[int] = None
    parent_classes: List[str] = Field(default_factory=list)
    docstring: Optional[str] = None
    method_names: List[str] = Field(default_factory=list)
    decorators: List[str] = Field(default_factory=list)


class FileNode(BaseModel):
    """Represents a source file in the project."""

    id: UUID = Field(default_factory=uuid4)
    project_id: Optional[UUID] = None
    relative_path: str
    language: str
    content_hash: str
    size_bytes: int
    last_modified: datetime
    parse_status: ParseStatus = ParseStatus.SUCCESS
    error_message: Optional[str] = None
    functions: List[FunctionDef] = Field(default_factory=list)
    classes: List[ClassDef] = Field(default_factory=list)


class Project(BaseModel):
    """Represents a codebase being indexed."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    root_path: str
    indexed_at: Optional[datetime] = None
    file_count: int = 0
    symbol_count: int = 0
    status: ProjectStatus = ProjectStatus.INDEXING
    config: dict = Field(default_factory=dict)
