"""
Tool dispatch and progress event handlers for Agent Todo Tool.

Provides dispatch_todo_tool() entry point and emit_progress() for streaming output.
"""

from typing import Dict, Any, Optional
from . import store
from .models import TaskStatus


def emit_progress(operation: str, summary: str, status: str) -> None:
    """
    Emit a progress event to stdout for IDE streaming.

    Format: [TODO] <operation>: <summary> (<status>)
    Status values: started, success, failed

    Args:
        operation: Operation name (add_task, list_tasks, etc.)
        summary: Brief description of what's happening
        status: Event status (started, success, failed)
    """
    print(f"[TODO] {operation}: {summary} ({status})")


def handle_add_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle add_task operation.

    Args:
        params: {"content": str, "activeForm": str, "priority": int?}

    Returns:
        ToolResponse as dict
    """
    content = params.get("content", "")
    active_form = params.get("activeForm", "")
    priority = params.get("priority")

    emit_progress("add_task", f'Adding "{content[:50]}..."' if len(content) > 50 else f'Adding "{content}"', "started")

    task = store.add_task(content, active_form, priority)

    if task is None:
        emit_progress("add_task", "Failed to create task", "failed")
        return {
            "success": False,
            "operation": "add_task",
            "message": "Failed to create task - invalid parameters",
            "task_id": None,
            "tasks": None,
            "error": "Validation failed: content and activeForm are required, must be non-empty"
        }

    emit_progress("add_task", f"Task {task.id[:8]}... created successfully", "success")
    return {
        "success": True,
        "operation": "add_task",
        "message": "Task created successfully",
        "task_id": task.id,
        "tasks": None,
        "error": None
    }


def handle_list_tasks(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle list_tasks operation.

    Args:
        params: {"status_filter": str?}

    Returns:
        ToolResponse as dict
    """
    status_filter_str = params.get("status_filter", "all")

    emit_progress("list_tasks", "Retrieving tasks", "started")

    # Parse status filter
    status_filter: Optional[TaskStatus] = None
    if status_filter_str and status_filter_str != "all":
        try:
            status_filter = TaskStatus(status_filter_str)
        except ValueError:
            emit_progress("list_tasks", f"Invalid status filter: {status_filter_str}", "failed")
            return {
                "success": False,
                "operation": "list_tasks",
                "message": f"Invalid status filter: {status_filter_str}",
                "task_id": None,
                "tasks": None,
                "error": "Valid values: all, pending, in_progress, completed"
            }

    tasks = store.list_tasks(status_filter)
    tasks_dict = [t.to_dict() for t in tasks]

    emit_progress("list_tasks", f"Retrieved {len(tasks)} tasks", "success")
    return {
        "success": True,
        "operation": "list_tasks",
        "message": f"Retrieved {len(tasks)} tasks",
        "task_id": None,
        "tasks": tasks_dict,
        "error": None
    }


def handle_update_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle update_task_status operation.

    Args:
        params: {"task_id": str, "status": str}

    Returns:
        ToolResponse as dict
    """
    task_id = params.get("task_id", "")
    status_str = params.get("status", "")

    emit_progress("update_task_status", f"Updating task {task_id[:8]}..." if len(task_id) > 8 else f"Updating task {task_id}", "started")

    # Validate task_id
    if not task_id:
        emit_progress("update_task_status", "Task ID is required", "failed")
        return {
            "success": False,
            "operation": "update_task_status",
            "message": "Task ID is required",
            "task_id": task_id,
            "tasks": None,
            "error": "Missing task_id parameter"
        }

    # Parse status
    try:
        new_status = TaskStatus(status_str)
    except ValueError:
        emit_progress("update_task_status", f"Invalid status: {status_str}", "failed")
        return {
            "success": False,
            "operation": "update_task_status",
            "message": f"Invalid status: {status_str}",
            "task_id": task_id,
            "tasks": None,
            "error": "Valid values: pending, in_progress, completed"
        }

    # Update task
    success = store.update_task(task_id, new_status)

    if not success:
        emit_progress("update_task_status", f"Task {task_id[:8]}... not found", "failed")
        return {
            "success": False,
            "operation": "update_task_status",
            "message": f"Task not found: {task_id}",
            "task_id": task_id,
            "tasks": None,
            "error": "Task does not exist"
        }

    emit_progress("update_task_status", f"Task {task_id[:8]}... now {status_str}", "success")
    return {
        "success": True,
        "operation": "update_task_status",
        "message": f"Task status updated to {status_str}",
        "task_id": task_id,
        "tasks": None,
        "error": None
    }


def handle_remove_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle remove_task operation.

    Args:
        params: {"task_id": str}

    Returns:
        ToolResponse as dict
    """
    task_id = params.get("task_id", "")

    emit_progress("remove_task", f"Removing task {task_id[:8]}..." if len(task_id) > 8 else f"Removing task {task_id}", "started")

    if not task_id:
        emit_progress("remove_task", "Task ID is required", "failed")
        return {
            "success": False,
            "operation": "remove_task",
            "message": "Task ID is required",
            "task_id": task_id,
            "tasks": None,
            "error": "Missing task_id parameter"
        }

    success = store.remove_task(task_id)

    if not success:
        emit_progress("remove_task", f"Task {task_id[:8]}... not found", "failed")
        return {
            "success": False,
            "operation": "remove_task",
            "message": f"Task not found: {task_id}",
            "task_id": task_id,
            "tasks": None,
            "error": "Task does not exist"
        }

    emit_progress("remove_task", "Task removed successfully", "success")
    return {
        "success": True,
        "operation": "remove_task",
        "message": "Task removed successfully",
        "task_id": task_id,
        "tasks": None,
        "error": None
    }


def handle_clear_completed(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle clear_completed operation.

    Args:
        params: {} (no parameters)

    Returns:
        ToolResponse as dict
    """
    emit_progress("clear_completed", "Clearing completed tasks", "started")

    count = store.clear_completed()

    emit_progress("clear_completed", f"Removed {count} completed tasks", "success")
    return {
        "success": True,
        "operation": "clear_completed",
        "message": f"Removed {count} completed tasks",
        "task_id": None,
        "tasks": None,
        "error": None
    }


def dispatch_todo_tool(operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch a todo tool operation.

    Args:
        operation: Operation name (add_task, list_tasks, update_task_status, etc.)
        params: Operation parameters

    Returns:
        ToolResponse as dict
    """
    handlers = {
        "add_task": handle_add_task,
        "list_tasks": handle_list_tasks,
        "update_task_status": handle_update_status,
        "remove_task": handle_remove_task,
        "clear_completed": handle_clear_completed,
    }

    handler = handlers.get(operation)
    if handler is None:
        return {
            "success": False,
            "operation": operation,
            "message": f"Unknown operation: {operation}",
            "task_id": None,
            "tasks": None,
            "error": f"Valid operations: {', '.join(handlers.keys())}"
        }

    return handler(params)
