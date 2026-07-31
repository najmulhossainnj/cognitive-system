"""Scheduler Implementation.

This module provides the Scheduler for task scheduling and execution.
"""

from __future__ import annotations

import asyncio
import heapq
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskStatus(str, Enum):
    """Task status values."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(order=True)
class ScheduledTask:
    """Represents a scheduled task."""

    priority: int
    task_id: str = field(compare=False)
    task: Any = field(compare=False)
    created_at: datetime = field(compare=False, default_factory=datetime.now)
    scheduled_at: datetime | None = field(compare=False, default=None)


@dataclass
class Task:
    """Represents a task in the scheduler."""

    id: str
    task: Any
    priority: int
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: Any = None
    error: str | None = None


class Scheduler:
    """Scheduler manages task scheduling and execution.

    The Scheduler is responsible for:
    - Prioritizing tasks
    - Managing task queues
    - Coordinating execution

    See RUNTIME-004 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the scheduler."""
        self._tasks: dict[str, Task] = {}
        self._queue: list[ScheduledTask] = []
        self._running: asyncio.Queue[Task] | None = None
        self._paused: bool = False
        self._worker_task: asyncio.Task | None = None
        self._results: dict[str, Any] = {}

    async def _worker(self) -> None:
        """Worker coroutine that processes tasks."""
        while not self._paused:
            if not self._queue:
                await asyncio.sleep(0.1)
                continue

            scheduled = heapq.heappop(self._queue)
            task = self._tasks.get(scheduled.task_id)
            if not task or task.status == TaskStatus.CANCELLED:
                continue

            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()

            try:
                if asyncio.iscoroutine(scheduled.task):
                    result = await scheduled.task
                elif callable(scheduled.task):
                    result = scheduled.task()
                    if asyncio.iscoroutine(result):
                        result = await result
                else:
                    result = scheduled.task

                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                self._results[task.id] = result
            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()

    async def schedule(self, task: Any, priority: int = 0) -> str:
        """Schedule a task.

        Args:
            task: Task to schedule (can be coroutine or callable)
            priority: Task priority (higher = more urgent)

        Returns:
            Task ID
        """
        task_id = str(uuid4())
        new_task = Task(id=task_id, task=task, priority=priority)
        self._tasks[task_id] = new_task

        scheduled = ScheduledTask(
            priority=-priority,
            task_id=task_id,
            task=task,
        )
        heapq.heappush(self._queue, scheduled)
        new_task.status = TaskStatus.SCHEDULED

        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker())

        return task_id

    async def get_next(self) -> Task | None:
        """Get the next task (without removing it).

        Returns:
            Next task or None
        """
        if not self._queue:
            return None

        scheduled = self._queue[0]
        return self._tasks.get(scheduled.task_id)

    async def cancel(self, task_id: str) -> bool:
        """Cancel a task.

        Args:
            task_id: Task to cancel

        Returns:
            True if cancelled
        """
        task = self._tasks.get(task_id)
        if not task:
            return False

        if task.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            return False

        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()

        self._queue = [t for t in self._queue if t.task_id != task_id]
        heapq.heapify(self._queue)

        return True

    async def get_status(self, task_id: str) -> str:
        """Get task status.

        Args:
            task_id: Task ID

        Returns:
            Task status
        """
        task = self._tasks.get(task_id)
        return task.status.value if task else "not_found"

    async def get_queue_size(self) -> int:
        """Get queue size.

        Returns:
            Number of queued tasks
        """
        return len(self._queue)

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

        if task.status == TaskStatus.COMPLETED:
            return task.result

        return None

    async def pause(self) -> None:
        """Pause the scheduler."""
        self._paused = True

    async def resume(self) -> None:
        """Resume the scheduler."""
        self._paused = False
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker())

    async def get_all_tasks(self) -> list[dict[str, Any]]:
        """Get all tasks.

        Returns:
            List of task information
        """
        return [
            {
                "id": t.id,
                "status": t.status.value,
                "priority": t.priority,
                "created_at": t.created_at.isoformat(),
                "started_at": t.started_at.isoformat() if t.started_at else None,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
            for t in self._tasks.values()
        ]

    async def wait_for_task(self, task_id: str, timeout: float | None = None) -> Any:
        """Wait for a task to complete.

        Args:
            task_id: Task ID
            timeout: Optional timeout in seconds

        Returns:
            Task result

        Raises:
            TimeoutError: If task doesn't complete within timeout
        """
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")

        start = asyncio.get_event_loop().time()
        while task.status not in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED):
            if timeout and (asyncio.get_event_loop().time() - start) > timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
            await asyncio.sleep(0.1)

        if task.status == TaskStatus.FAILED:
            raise RuntimeError(f"Task failed: {task.error}")

        return task.result


# Module-level singleton instance
_scheduler: Scheduler | None = None


def get_scheduler() -> Scheduler:
    """Get the global scheduler instance.

    Returns:
        Scheduler instance
    """
    global _scheduler
    if _scheduler is None:
        _scheduler = Scheduler()
    return _scheduler


# Re-export interface for type hints
IScheduler = Scheduler
