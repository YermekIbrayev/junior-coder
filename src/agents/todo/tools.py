"""
Tool definitions for Agent Todo Tool.

Defines TODO_TOOLS constant in OpenAI function calling format.
Full implementation - just data definition, no stubs needed.
"""

from typing import List, Dict, Any


# OpenAI function calling format tool definitions
TODO_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the shared todo list. Emits progress events to stdout.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Description of what needs to be done (max 1000 chars)",
                    },
                    "activeForm": {
                        "type": "string",
                        "description": "Present continuous form shown during execution (e.g., 'Implementing authentication')",
                    },
                    "priority": {
                        "type": "integer",
                        "description": "Optional priority hint (lower number = higher priority)",
                    },
                },
                "required": ["content", "activeForm"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks in the shared todo list with their current status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status_filter": {
                        "type": "string",
                        "enum": ["all", "pending", "in_progress", "completed"],
                        "description": "Filter tasks by status (default: all)",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task_status",
            "description": "Update the status of an existing task. Emits progress events to stdout.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to update",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                        "description": "New status for the task",
                    },
                },
                "required": ["task_id", "status"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_task",
            "description": "Remove a task from the todo list by its ID. Emits progress events to stdout.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to remove",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clear_completed",
            "description": "Remove all completed tasks from the todo list. Emits progress events to stdout.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]
