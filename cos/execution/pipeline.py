"""Cognitive Pipeline Interface.

This module defines the interface for cognitive execution pipelines.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Confidence, Explanation, Trace


class ICognitivePipeline:
    """Cognitive Pipeline interface for cognitive execution.

    The pipeline orchestrates all cognitive capabilities to solve problems.
    """

    async def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        """Execute the pipeline.

        Args:
            request: Request to process

        Returns:
            Pipeline result
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def pause(self, execution_id: str) -> None:
        """Pause execution.

        Args:
            execution_id: Execution to pause
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def resume(self, execution_id: str) -> None:
        """Resume execution.

        Args:
            execution_id: Execution to resume
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def cancel(self, execution_id: str) -> None:
        """Cancel execution.

        Args:
            execution_id: Execution to cancel
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_trace(self, execution_id: str) -> Trace:
        """Get execution trace.

        Args:
            execution_id: Execution ID

        Returns:
            Execution trace
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def explain(self, execution_id: str) -> Explanation:
        """Explain execution.

        Args:
            execution_id: Execution ID

        Returns:
            Explanation
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_confidence(self, execution_id: str) -> Confidence:
        """Get execution confidence.

        Args:
            execution_id: Execution ID

        Returns:
            Confidence estimate
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_status(self, execution_id: str) -> dict[str, Any]:
        """Get execution status.

        Args:
            execution_id: Execution ID

        Returns:
            Status information
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_metrics(self, execution_id: str) -> dict[str, Any]:
        """Get execution metrics.

        Args:
            execution_id: Execution ID

        Returns:
            Metrics
        """
        raise NotImplementedError("Will be implemented in Phase 3")


class IRequestLifecycle:
    """Request Lifecycle interface.

    Manages the lifecycle of requests through the system.
    """

    async def submit(self, request: dict[str, Any]) -> str:
        """Submit a request.

        Args:
            request: Request to submit

        Returns:
            Request ID
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_status(self, request_id: str) -> dict[str, Any]:
        """Get request status.

        Args:
            request_id: Request ID

        Returns:
            Status
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def cancel(self, request_id: str) -> bool:
        """Cancel a request.

        Args:
            request_id: Request to cancel

        Returns:
            True if cancelled
        """
        raise NotImplementedError("Will be implemented in Phase 3")

    async def get_result(self, request_id: str) -> Any | None:
        """Get request result.

        Args:
            request_id: Request ID

        Returns:
            Result or None
        """
        raise NotImplementedError("Will be implemented in Phase 3")
