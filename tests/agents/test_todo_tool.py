"""
Tests for Agent Todo Tool

TDD test suite following the stub implementation pattern:
- Phase 1 tests: Verify module structure (should pass immediately)
- Phase 2 tests: Verify stubs exist (should pass after Phase 2)
- Phase 3+ tests: Verify business logic (should FAIL against stubs, pass after implementation)
"""

import pytest
from pathlib import Path


# =============================================================================
# Phase 1: Structural Tests (Module Setup)
# =============================================================================

class TestPhase1ModuleStructure:
    """Verify Phase 1 setup: directory and __init__.py created."""

    def test_todo_module_directory_exists(self):
        """T001: Verify src/agents/todo/ directory exists."""
        module_path = Path(__file__).parent.parent.parent / "src" / "agents" / "todo"
        assert module_path.exists(), f"Directory not found: {module_path}"
        assert module_path.is_dir(), f"Not a directory: {module_path}"

    def test_todo_module_init_exists(self):
        """T002: Verify __init__.py exists with docstring."""
        init_path = Path(__file__).parent.parent.parent / "src" / "agents" / "todo" / "__init__.py"
        assert init_path.exists(), f"__init__.py not found: {init_path}"

        content = init_path.read_text()
        assert '"""' in content or "'''" in content, "__init__.py should have a docstring"
        assert "Agent Todo Tool" in content, "__init__.py docstring should describe the module"

    def test_todo_module_importable(self):
        """Verify the todo module can be imported."""
        try:
            from src.agents import todo
            assert todo is not None
        except ImportError as e:
            pytest.fail(f"Failed to import src.agents.todo: {e}")


# =============================================================================
# Phase 2: Stub Tests (Will pass after Phase 2 creates stubs)
# =============================================================================

class TestPhase2StubsExist:
    """Verify Phase 2 stubs exist. These tests will fail until Phase 2 is complete."""

    def test_models_module_exists(self):
        """T003: Verify models.py exists with TaskStatus and Task."""
        from src.agents.todo import models
        assert hasattr(models, 'TaskStatus'), "models.py should define TaskStatus enum"
        assert hasattr(models, 'Task'), "models.py should define Task dataclass"
        assert hasattr(models, 'ToolResponse'), "models.py should define ToolResponse dataclass"

    def test_store_module_exists(self):
        """T004: Verify store.py exists with stub functions."""
        from src.agents.todo import store
        assert hasattr(store, 'add_task'), "store.py should define add_task()"
        assert hasattr(store, 'get_task'), "store.py should define get_task()"
        assert hasattr(store, 'list_tasks'), "store.py should define list_tasks()"
        assert hasattr(store, 'update_task'), "store.py should define update_task()"
        assert hasattr(store, 'remove_task'), "store.py should define remove_task()"
        assert hasattr(store, 'clear_completed'), "store.py should define clear_completed()"

    def test_handlers_module_exists(self):
        """T005: Verify handlers.py exists with stub functions."""
        from src.agents.todo import handlers
        assert hasattr(handlers, 'dispatch_todo_tool'), "handlers.py should define dispatch_todo_tool()"
        assert hasattr(handlers, 'emit_progress'), "handlers.py should define emit_progress()"

    def test_tools_module_exists(self):
        """T006: Verify tools.py exists with TODO_TOOLS constant."""
        from src.agents.todo import tools
        assert hasattr(tools, 'TODO_TOOLS'), "tools.py should define TODO_TOOLS"
        assert isinstance(tools.TODO_TOOLS, list), "TODO_TOOLS should be a list"


# =============================================================================
# Phase 3: User Story 1 - Create and Track Tasks (TDD Tests)
# These tests will FAIL against stubs and PASS after implementation
# =============================================================================

class TestUserStory1CreateAndTrackTasks:
    """US1: As an AI agent, I need to create tasks and track their progress."""

    def test_add_task_creates_task_with_id(self):
        """T007: Add task returns success=True and valid UUID task_id."""
        from src.agents.todo.handlers import dispatch_todo_tool

        result = dispatch_todo_tool("add_task", {
            "content": "Implement authentication",
            "activeForm": "Implementing authentication"
        })

        # This will FAIL with stub (success=False), PASS after implementation
        assert result["success"] is True, "add_task should return success=True"
        assert result["task_id"] is not None, "add_task should return a task_id"
        assert len(result["task_id"]) == 36, "task_id should be a valid UUID string"

    def test_list_tasks_returns_all_tasks(self):
        """T008: List tasks returns all added tasks."""
        from src.agents.todo.handlers import dispatch_todo_tool
        from src.agents.todo.store import _todo_store

        # Clear store for test isolation
        _todo_store.clear()

        # Add two tasks
        dispatch_todo_tool("add_task", {
            "content": "Task 1",
            "activeForm": "Working on Task 1"
        })
        dispatch_todo_tool("add_task", {
            "content": "Task 2",
            "activeForm": "Working on Task 2"
        })

        result = dispatch_todo_tool("list_tasks", {})

        # This will FAIL with stub (returns empty), PASS after implementation
        assert result["success"] is True, "list_tasks should return success=True"
        assert "tasks" in result, "list_tasks should return tasks list"
        assert len(result["tasks"]) == 2, "Should return 2 tasks"

    def test_update_status_changes_task_state(self):
        """T009: Update status changes task from pending to in_progress."""
        from src.agents.todo.handlers import dispatch_todo_tool
        from src.agents.todo.store import _todo_store

        # Clear store for test isolation
        _todo_store.clear()

        # Add a task
        add_result = dispatch_todo_tool("add_task", {
            "content": "Test task",
            "activeForm": "Testing"
        })
        task_id = add_result["task_id"]

        # Update status
        result = dispatch_todo_tool("update_task_status", {
            "task_id": task_id,
            "status": "in_progress"
        })

        # This will FAIL with stub (success=False), PASS after implementation
        assert result["success"] is True, "update_task_status should return success=True"

        # Verify task status changed
        list_result = dispatch_todo_tool("list_tasks", {})
        task = next(t for t in list_result["tasks"] if t["id"] == task_id)
        assert task["status"] == "in_progress", "Task status should be in_progress"


# =============================================================================
# Phase 4: User Story 2 - Manage Task Lifecycle (TDD Tests)
# =============================================================================

class TestUserStory2ManageTaskLifecycle:
    """US2: As an AI agent, I need to update and complete tasks."""

    def test_remove_task_deletes_task(self):
        """T016: Remove task deletes the task from the store."""
        from src.agents.todo.handlers import dispatch_todo_tool
        from src.agents.todo.store import _todo_store

        _todo_store.clear()

        # Add a task
        add_result = dispatch_todo_tool("add_task", {
            "content": "Task to remove",
            "activeForm": "Removing task"
        })
        task_id = add_result["task_id"]

        # Remove it
        result = dispatch_todo_tool("remove_task", {"task_id": task_id})

        assert result["success"] is True, "remove_task should return success=True"

        # Verify it's gone
        list_result = dispatch_todo_tool("list_tasks", {})
        assert len(list_result["tasks"]) == 0, "Task should be removed"

    def test_clear_completed_removes_only_completed(self):
        """T016: Clear completed removes only completed tasks."""
        from src.agents.todo.handlers import dispatch_todo_tool
        from src.agents.todo.store import _todo_store

        _todo_store.clear()

        # Add tasks with different statuses
        dispatch_todo_tool("add_task", {"content": "Pending task", "activeForm": "Pending"})
        completed_result = dispatch_todo_tool("add_task", {"content": "Completed task", "activeForm": "Completed"})

        # Mark one as completed
        dispatch_todo_tool("update_task_status", {
            "task_id": completed_result["task_id"],
            "status": "completed"
        })

        # Clear completed
        result = dispatch_todo_tool("clear_completed", {})

        assert result["success"] is True, "clear_completed should return success=True"

        # Verify only pending remains
        list_result = dispatch_todo_tool("list_tasks", {})
        assert len(list_result["tasks"]) == 1, "Only pending task should remain"
        assert list_result["tasks"][0]["content"] == "Pending task"


# =============================================================================
# Phase 5: User Story 3 - Multi-Agent Task Sharing (TDD Tests)
# =============================================================================

class TestUserStory3MultiAgentSharing:
    """US3: As an AI agent, I need shared access to the task list."""

    def test_shared_store_across_imports(self):
        """T021: Store is shared singleton across multiple imports."""
        # Import store twice (simulating two agents)
        from src.agents.todo import store as store1
        from src.agents.todo import store as store2

        # Clear and add via first import
        store1._todo_store.clear()
        store1.add_task("Shared task", "Working on shared task")

        # Verify visible via second import
        tasks = store2.list_tasks()
        assert len(tasks) == 1, "Task added by store1 should be visible to store2"
        assert tasks[0].content == "Shared task"
