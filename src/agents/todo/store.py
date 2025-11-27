"""
In-memory task storage for Agent Todo Tool.

Provides CRUD operations on a module-level dictionary (shared singleton).
"""

from typing import Optional, List, Dict
from uuid import uuid4
from .models import Task, TaskStatus


# Module-level store - shared singleton across all agents
_todo_store: Dict[str, Task] = {}


def add_task(content: str, active_form: str, priority: Optional[int] = None) -> Optional[Task]:
    """
    Add a new task to the store.

    Args:
        content: Description of what needs to be done
        active_form: Present continuous form (e.g., "Implementing authentication")
        priority: Optional priority hint (lower = higher priority)

    Returns:
        Created Task with unique UUID, or None if validation fails
    """
    # Validate content
    if not content or len(content) > 1000:
        return None
    if not active_form or len(active_form) > 200:
        return None
    if priority is not None and priority < 0:
        return None

    # Create task with UUID
    task_id = str(uuid4())
    task = Task(
        id=task_id,
        content=content,
        status=TaskStatus.PENDING,
        activeForm=active_form,
        priority=priority,
    )

    # Store and return
    _todo_store[task_id] = task
    return task


def get_task(task_id: str) -> Optional[Task]:
    """
    Get a task by ID.

    Args:
        task_id: UUID of the task

    Returns:
        Task if found, None otherwise
    """
    return _todo_store.get(task_id)


def list_tasks(status_filter: Optional[TaskStatus] = None) -> List[Task]:
    """
    List all tasks, optionally filtered by status.

    Args:
        status_filter: Optional status to filter by

    Returns:
        List of tasks (all or filtered by status)
    """
    tasks = list(_todo_store.values())

    if status_filter is not None:
        tasks = [t for t in tasks if t.status == status_filter]

    # Sort by priority (None last), then by created_at
    return sorted(
        tasks,
        key=lambda t: (t.priority if t.priority is not None else float('inf'), t.created_at)
    )


def update_task(task_id: str, status: TaskStatus) -> bool:
    """
    Update a task's status.

    Args:
        task_id: UUID of the task to update
        status: New status

    Returns:
        True if task found and updated, False otherwise
    """
    task = _todo_store.get(task_id)
    if task is None:
        return False

    # Update status (create new task to maintain immutability pattern)
    updated_task = Task(
        id=task.id,
        content=task.content,
        status=status,
        activeForm=task.activeForm,
        priority=task.priority,
        created_at=task.created_at,
    )
    _todo_store[task_id] = updated_task
    return True


def remove_task(task_id: str) -> bool:
    """
    Remove a task by ID.

    Args:
        task_id: UUID of the task to remove

    Returns:
        True if task found and removed, False otherwise
    """
    if task_id in _todo_store:
        del _todo_store[task_id]
        return True
    return False


def clear_completed() -> int:
    """
    Remove all completed tasks.

    Returns:
        Number of tasks removed
    """
    global _todo_store
    completed_ids = [
        task_id for task_id, task in _todo_store.items()
        if task.status == TaskStatus.COMPLETED
    ]
    for task_id in completed_ids:
        del _todo_store[task_id]
    return len(completed_ids)
