"""
Tests for the indexer models module (Phase 2 - RED Stage).

These tests verify Pydantic model fields and serialization.
TDD: Tests FAIL because models may not have all fields → Implement → Tests PASS.
"""

from datetime import datetime
from uuid import UUID

import pytest

from src.agents.indexer.models import (
    Project,
    FileNode,
    FunctionDef,
    ClassDef,
    Parameter,
    ProjectStatus,
    ParseStatus,
)


class TestT023ProjectModel:
    """T023: Project model has all required fields."""

    def test_project_has_id_field(self):
        """Project should have an auto-generated UUID id."""
        project = Project(name="test", root_path="/opt/test")

        assert hasattr(project, "id")
        assert isinstance(project.id, UUID)

    def test_project_has_name_field(self):
        """Project should have a name field."""
        project = Project(name="my-project", root_path="/opt/test")

        assert project.name == "my-project"

    def test_project_has_root_path_field(self):
        """Project should have a root_path field."""
        project = Project(name="test", root_path="/opt/projects/app")

        assert project.root_path == "/opt/projects/app"

    def test_project_has_status_field(self):
        """Project should have a status field with default INDEXING."""
        project = Project(name="test", root_path="/opt/test")

        assert hasattr(project, "status")
        assert project.status == ProjectStatus.INDEXING

    def test_project_has_indexed_at_field(self):
        """Project should have an optional indexed_at datetime."""
        project = Project(name="test", root_path="/opt/test")

        assert hasattr(project, "indexed_at")
        # Default should be None
        assert project.indexed_at is None

    def test_project_has_file_count_field(self):
        """Project should have file_count with default 0."""
        project = Project(name="test", root_path="/opt/test")

        assert hasattr(project, "file_count")
        assert project.file_count == 0

    def test_project_has_symbol_count_field(self):
        """Project should have symbol_count with default 0."""
        project = Project(name="test", root_path="/opt/test")

        assert hasattr(project, "symbol_count")
        assert project.symbol_count == 0

    def test_project_status_can_be_set(self):
        """Project status can be set to different values."""
        project = Project(
            name="test",
            root_path="/opt/test",
            status=ProjectStatus.ACTIVE,
        )

        assert project.status == ProjectStatus.ACTIVE


class TestT024FileNodeModel:
    """T024: FileNode model has all required fields."""

    def test_file_node_has_id_field(self):
        """FileNode should have an auto-generated UUID id."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert hasattr(file_node, "id")
        assert isinstance(file_node.id, UUID)

    def test_file_node_has_project_id_field(self):
        """FileNode should have an optional project_id field."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert hasattr(file_node, "project_id")

    def test_file_node_has_relative_path_field(self):
        """FileNode should have a relative_path field."""
        file_node = FileNode(
            relative_path="src/utils/helpers.py",
            language="python",
            content_hash="abc123",
            size_bytes=512,
            last_modified=datetime.now(),
        )

        assert file_node.relative_path == "src/utils/helpers.py"

    def test_file_node_has_language_field(self):
        """FileNode should have a language field."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert file_node.language == "python"

    def test_file_node_has_content_hash_field(self):
        """FileNode should have a content_hash field."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="sha256hash",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert file_node.content_hash == "sha256hash"

    def test_file_node_has_size_bytes_field(self):
        """FileNode should have a size_bytes field."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=2048,
            last_modified=datetime.now(),
        )

        assert file_node.size_bytes == 2048

    def test_file_node_has_parse_status_field(self):
        """FileNode should have a parse_status field with default SUCCESS."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert hasattr(file_node, "parse_status")
        assert file_node.parse_status == ParseStatus.SUCCESS

    def test_file_node_has_functions_list(self):
        """FileNode should have a functions list."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert hasattr(file_node, "functions")
        assert isinstance(file_node.functions, list)

    def test_file_node_has_classes_list(self):
        """FileNode should have a classes list."""
        file_node = FileNode(
            relative_path="src/main.py",
            language="python",
            content_hash="abc123",
            size_bytes=1024,
            last_modified=datetime.now(),
        )

        assert hasattr(file_node, "classes")
        assert isinstance(file_node.classes, list)


class TestT025FunctionDefModel:
    """T025: FunctionDef model serializes parameters correctly."""

    def test_function_def_has_required_fields(self):
        """FunctionDef should have name, line_number, signature."""
        func = FunctionDef(
            name="my_function",
            line_number=10,
            signature="def my_function(x: int) -> str",
        )

        assert func.name == "my_function"
        assert func.line_number == 10
        assert func.signature == "def my_function(x: int) -> str"

    def test_function_def_has_parameters_list(self):
        """FunctionDef should have a parameters list."""
        func = FunctionDef(
            name="test",
            line_number=1,
            signature="def test()",
        )

        assert hasattr(func, "parameters")
        assert isinstance(func.parameters, list)

    def test_function_def_serializes_parameters(self):
        """FunctionDef parameters should serialize correctly."""
        param1 = Parameter(name="x", type="int", default=None, is_variadic=False)
        param2 = Parameter(name="y", type="str", default="''", is_variadic=False)

        func = FunctionDef(
            name="add",
            line_number=5,
            signature="def add(x: int, y: str = '') -> int",
            parameters=[param1, param2],
        )

        assert len(func.parameters) == 2
        assert func.parameters[0].name == "x"
        assert func.parameters[0].type == "int"
        assert func.parameters[1].name == "y"
        assert func.parameters[1].default == "''"

    def test_function_def_model_dump_includes_parameters(self):
        """model_dump() should include serialized parameters."""
        param = Parameter(name="data", type="list", is_variadic=False)
        func = FunctionDef(
            name="process",
            line_number=20,
            signature="def process(data: list)",
            parameters=[param],
        )

        dumped = func.model_dump()

        assert "parameters" in dumped
        assert len(dumped["parameters"]) == 1
        assert dumped["parameters"][0]["name"] == "data"
        assert dumped["parameters"][0]["type"] == "list"

    def test_function_def_has_is_async_field(self):
        """FunctionDef should have is_async boolean field."""
        func = FunctionDef(
            name="async_func",
            line_number=1,
            signature="async def async_func()",
            is_async=True,
        )

        assert func.is_async is True

    def test_function_def_has_docstring_field(self):
        """FunctionDef should have optional docstring field."""
        func = FunctionDef(
            name="documented",
            line_number=1,
            signature="def documented()",
            docstring="This function is documented.",
        )

        assert func.docstring == "This function is documented."

    def test_function_def_has_decorators_field(self):
        """FunctionDef should have decorators list."""
        func = FunctionDef(
            name="decorated",
            line_number=1,
            signature="def decorated()",
            decorators=["@staticmethod", "@cache"],
        )

        assert func.decorators == ["@staticmethod", "@cache"]


class TestT026ClassDefModel:
    """T026: ClassDef model serializes parent_classes correctly."""

    def test_class_def_has_required_fields(self):
        """ClassDef should have name and line_number."""
        cls = ClassDef(
            name="MyClass",
            line_number=15,
        )

        assert cls.name == "MyClass"
        assert cls.line_number == 15

    def test_class_def_has_parent_classes_list(self):
        """ClassDef should have a parent_classes list."""
        cls = ClassDef(
            name="ChildClass",
            line_number=1,
        )

        assert hasattr(cls, "parent_classes")
        assert isinstance(cls.parent_classes, list)

    def test_class_def_serializes_parent_classes(self):
        """ClassDef parent_classes should serialize correctly."""
        cls = ClassDef(
            name="MultiInherit",
            line_number=10,
            parent_classes=["BaseModel", "Mixin"],
        )

        assert len(cls.parent_classes) == 2
        assert "BaseModel" in cls.parent_classes
        assert "Mixin" in cls.parent_classes

    def test_class_def_model_dump_includes_parent_classes(self):
        """model_dump() should include parent_classes."""
        cls = ClassDef(
            name="Derived",
            line_number=5,
            parent_classes=["Parent1", "Parent2"],
        )

        dumped = cls.model_dump()

        assert "parent_classes" in dumped
        assert dumped["parent_classes"] == ["Parent1", "Parent2"]

    def test_class_def_has_docstring_field(self):
        """ClassDef should have optional docstring field."""
        cls = ClassDef(
            name="Documented",
            line_number=1,
            docstring="A documented class.",
        )

        assert cls.docstring == "A documented class."

    def test_class_def_has_method_names_field(self):
        """ClassDef should have method_names list."""
        cls = ClassDef(
            name="WithMethods",
            line_number=1,
            method_names=["__init__", "process", "save"],
        )

        assert cls.method_names == ["__init__", "process", "save"]

    def test_class_def_has_decorators_field(self):
        """ClassDef should have decorators list."""
        cls = ClassDef(
            name="DataClass",
            line_number=1,
            decorators=["@dataclass"],
        )

        assert cls.decorators == ["@dataclass"]


class TestParameterModel:
    """Test the Parameter model."""

    def test_parameter_has_name(self):
        """Parameter must have a name."""
        param = Parameter(name="arg1")

        assert param.name == "arg1"

    def test_parameter_has_optional_type(self):
        """Parameter type is optional."""
        param = Parameter(name="arg1", type="int")

        assert param.type == "int"

    def test_parameter_has_optional_default(self):
        """Parameter default is optional."""
        param = Parameter(name="arg1", default="None")

        assert param.default == "None"

    def test_parameter_has_is_variadic(self):
        """Parameter should have is_variadic boolean."""
        param = Parameter(name="args", is_variadic=True)

        assert param.is_variadic is True


class TestEnums:
    """Test the status enums."""

    def test_project_status_values(self):
        """ProjectStatus should have expected values."""
        assert ProjectStatus.ACTIVE.value == "active"
        assert ProjectStatus.INDEXING.value == "indexing"
        assert ProjectStatus.ERROR.value == "error"

    def test_parse_status_values(self):
        """ParseStatus should have expected values."""
        assert ParseStatus.SUCCESS.value == "success"
        assert ParseStatus.SKIPPED.value == "skipped"
        assert ParseStatus.ERROR.value == "error"
