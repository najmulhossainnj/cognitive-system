"""Scheduler - Task scheduling and prioritization for COS."""

from __future__ import annotations


class IScheduler:
    """Task scheduler for managing execution priorities and ordering.

    The scheduler is responsible for:
    - Prioritizing tasks based on importance and urgency
    - Managing task queues
    - Coordinating parallel execution
    - Handling task dependencies
    """

    async def schedule(self, task: object, priority: int = 0) -> None:
        """Schedule a task for execution.

        Args:
            task: The task to schedule
            priority: Task priority (higher = more urgent)
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def get_next(self) -> object | None:
        """Get the next task to execute.

        Returns:
            The next task or None if queue is empty
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def cancel(self, task_id: str) -> bool:
        """Cancel a scheduled task.

        Args:
            task_id: The task identifier

        Returns:
            True if task was cancelled, False if not found
        """
        raise NotImplementedError("Will be implemented in Phase 2")
