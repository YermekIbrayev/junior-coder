"""
Data models for Agent Todo Tool.

Defines TaskStatus enum, Task dataclass, and ToolResponse dataclass.
These are full implementations - data classes don't need stubs.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Any
import time


class TaskStatus(str, Enum):
    """Task lifecycle states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """Represents a single work item in the todo list."""
    id: str
    content: str
    status: TaskStatus
    activeForm: str
    created_at: float = field(default_factory=time.time)
    priority: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "status": self.status.value,
            "activeForm": self.activeForm,
            "created_at": self.created_at,
            "priority": self.priority,
        }


@dataclass
class ToolResponse:
    """Standardized response from tool operations."""
    success: bool
    operation: str
    message: str
    task_id: Optional[str] = None
    tasks: Optional[List[Task]] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert response to dictionary for JSON serialization."""
        result = {
            "success": self.success,
            "operation": self.operation,
            "message": self.message,
        }
        if self.task_id is not None:
            result["task_id"] = self.task_id
        if self.tasks is not None:
            result["tasks"] = [t.to_dict() for t in self.tasks]
        if self.error is not None:
            result["error"] = self.error
        return result
