"""Task Manager Implementation.

This module provides the Task Manager for task lifecycle management.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskState(str, Enum):
    """Task state values."""

    CREATED = "created"
    SUBMITTED = "submitted"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ManagedTask:
    """Represents a managed task."""

    id: str
    name: str
    handler: Any
    params: dict[str, Any] | None = None
    state: TaskState = TaskState.CREATED
    result: Any = None
    error: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    submitted_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    future: asyncio.Future | None = None


class TaskManager:
    """Task Manager manages task lifecycle.

    The Task Manager is responsible for:
    - Creating tasks
    - Tracking task state
    - Managing task completion

    See RUNTIME-006 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the task manager."""
        self._tasks: dict[str, ManagedTask] = {}
        self._results: dict[str, Any] = {}
        self._futures: dict[str, asyncio.Future] = {}

    async def create_task(
        self,
        name: str,
        handler: Any,
        params: dict[str, Any] | None = None,
    ) -> str:
        """Create a task.

        Args:
            name: Task name
            handler: Task handler
            params: Task parameters

        Returns:
            Task ID
        """
        task_id = str(uuid4())
        task = ManagedTask(
            id=task_id,
            name=name,
            handler=handler,
            params=params or {},
        )
        self._tasks[task_id] = task
        return task_id

    async def submit_task(self, task_id: str) -> None:
        """Submit a task for execution.

        Args:
            task_id: Task to submit
        """
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        if task.state != TaskState.CREATED:
            raise RuntimeError(f"Task already submitted: {task_id}")

        task.state = TaskState.SUBMITTED
        task.submitted_at = datetime.now()

        async def run_task() -> None:
            task.state = TaskState.RUNNING
            task.started_at = datetime.now()

            try:
                handler = task.handler
                params = task.params or {}

                if asyncio.iscoroutinefunction(handler):
                    result = await handler(**params)
                elif callable(handler):
                    result = handler(**params)
                    if asyncio.iscoroutine(result):
                        result = await result
                else:
                    result = handler

                task.result = result
                task.state = TaskState.COMPLETED
                self._results[task_id] = result

            except Exception as e:
                task.error = str(e)
                task.state = TaskState.FAILED

            finally:
                task.completed_at = datetime.now()

        task.future = asyncio.create_task(run_task())
        self._futures[task_id] = task.future

    async def get_task_result(self, task_id: str) -> Any | None:
        """Get task result.

        Args:
            task_id: Task ID

        Returns:
            Task result or None
        """
        task = self._tasks.get(task_id)
        if not task:
            return None

        if task.state == TaskState.COMPLETED:
            return task.result

        return None

    async def wait_for_task(
        self,
        task_id: str,
        timeout: float | None = None,
    ) -> Any:
        """Wait for task completion.

        Args:
            task_id: Task ID
            timeout: Optional timeout

        Returns:
            Task result

        Raises:
            TimeoutError: If task doesn't complete within timeout
            RuntimeError: If task fails
        """
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        if not task.future:
            raise RuntimeError(f"Task not submitted: {task_id}")

        try:
            return await asyncio.wait_for(task.future, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task.

        Args:
            task_id: Task to cancel

        Returns:
            True if cancelled
        """
        task = self._tasks.get(task_id)
        if not task:
            return False

        if task.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED):
            return False

        if task.future and not task.future.done():
            task.future.cancel()

        task.state = TaskState.CANCELLED
        task.completed_at = datetime.now()
        return True

    async def get_task_state(self, task_id: str) -> str:
        """Get task state.

        Args:
            task_id: Task ID

        Returns:
            Task state
        """
        task = self._tasks.get(task_id)
        return task.state.value if task else "not_found"

    def get_all_tasks(self) -> dict[str, ManagedTask]:
        """Get all tasks.

        Returns:
            Dictionary of task ID to ManagedTask
        """
        return self._tasks.copy()

    def get_tasks_by_state(self, state: TaskState) -> list[ManagedTask]:
        """Get tasks by state.

        Args:
            state: Task state to filter

        Returns:
            List of tasks
        """
        return [t for t in self._tasks.values() if t.state == state]


# Module-level singleton instance
_task_manager: TaskManager | None = None


def get_task_manager() -> TaskManager:
    """Get the global task manager instance.

    Returns:
        TaskManager instance
    """
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager


# Re-export interface for type hints
ITaskManager = TaskManager
