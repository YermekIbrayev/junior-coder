"""
Agent Todo Tool

Internal todo list tool for AI agents providing task CRUD operations with streaming
progress events. Backend-only, accessible to all agents via ToolAgent infrastructure.

Uses OpenAI function calling format and emits progress events to stdout for IDE
streaming (e.g., Continue.dev).

Exports (populated in Phase 6):
- TODO_TOOLS: Tool definitions in OpenAI function calling format
- dispatch_todo_tool: Main entry point for tool operations
- Task: Task dataclass
- TaskStatus: Status enum (pending, in_progress, completed)
"""

# Public exports
from .tools import TODO_TOOLS
from .handlers import dispatch_todo_tool
from .models import Task, TaskStatus

__all__ = ["TODO_TOOLS", "dispatch_todo_tool", "Task", "TaskStatus"]
