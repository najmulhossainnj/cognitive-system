"""Executive - Core control flow management for COS."""

from __future__ import annotations


class IExecutive:
    """Executive controller for managing task execution flow.

    The executive is responsible for:
    - Task initialization and lifecycle management
    - Coordinating with the scheduler
    - Managing execution state
    - Handling task completion and errors
    """

    async def execute(self, task: object) -> object:
        """Execute a task through the cognitive pipeline.

        Args:
            task: The task to execute

        Returns:
            The task result
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def shutdown(self) -> None:
        """Shutdown the executive and cleanup resources."""
        raise NotImplementedError("Will be implemented in Phase 2")
