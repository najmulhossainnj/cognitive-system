"""ARC Agent - Thin Application for ARC-AGI-2 tasks.

The ARC Agent follows the COS architectural principle where applications
remain thin and delegate all cognition to the Runtime.

Application Responsibilities:
    - Load ARC JSON data
    - Validate requests
    - Convert to standardized COS Request
    - Submit to Runtime
    - Format Response

Runtime Responsibilities:
    - Execute Cognitive Pipeline
    - Orchestrate cognitive services
    - Manage execution order

See COS-IMPLEMENTATION-001 for architectural guidance.

Example:
    >>> agent = ARCAgent()
    >>> request = agent.prepare_request(task_data)
    >>> response = await agent.execute(request)
    >>> solution = agent.format_response(response)
"""

from __future__ import annotations

from typing import Any

from cos.apps.arc_agent.arc_pipeline import (
    ARCCognitivePipeline,
    ARCRequestBuilder,
    ARCResponseFormatter,
)
from cos.apps.arc_agent.models import ARCRequest, ARCResponse
from cos.broker.cognitive_broker import CognitiveBroker


class ARCAgent:
    """ARC Agent Application (APP-140) - Thin Application.

    The ARC Agent is intentionally lightweight. It does NOT:
        - Execute reasoning directly
        - Access cognitive services
        - Perform learning
        - Make decisions
        - Manage execution order

    Instead, it:
        1. Loads ARC JSON data
        2. Validates requests
        3. Converts to standardized COS Request format
        4. Submits to Runtime via Cognitive Pipeline
        5. Formats the Response

    See COS-IMPLEMENTATION-001 for architectural guidance.

    Example:
        >>> agent = ARCAgent()
        >>> request = agent.prepare_request(task_data)
        >>> response = await agent.execute(request)
        >>> solution = agent.format_response(response)
    """

    def __init__(
        self,
        broker: CognitiveBroker | None = None,
        pipeline: ARCCognitivePipeline | None = None,
    ) -> None:
        """Initialize the ARC Agent.

        Args:
            broker: Cognitive Broker for Runtime access (optional, creates default)
            pipeline: ARC Cognitive Pipeline (optional, creates default)
        """
        self._broker = broker or CognitiveBroker()
        self._pipeline = pipeline
        self._initialized = False
        self._task_history: list[dict[str, Any]] = []

    async def _ensure_initialized(self) -> None:
        """Ensure the agent is initialized."""
        if not self._initialized:
            await self._broker.initialize()
            if self._pipeline is None:
                self._pipeline = ARCCognitivePipeline(self._broker)
            self._initialized = True

    def prepare_request(self, task_data: dict[str, Any]) -> ARCRequest:
        """Prepare a standardized COS Request from ARC JSON data.

        Args:
            task_data: JSON representation of the ARC task

        Returns:
            Standardized ARC request

        Raises:
            ValueError: If task_data is invalid
        """
        # Validate required fields
        if "train" not in task_data or "test" not in task_data:
            raise ValueError("Task must have 'train' and 'test' fields")

        if not task_data.get("train"):
            raise ValueError("Task must have at least one training example")

        # Build standardized request
        return ARCRequestBuilder.from_json(task_data)

    async def execute(self, request: ARCRequest) -> ARCResponse:
        """Execute an ARC request through the Runtime.

        Args:
            request: Standard ARC request

        Returns:
            Standard ARC response from Runtime
        """
        await self._ensure_initialized()
        return await self._pipeline.execute(request)

    async def solve(self, task_data: dict[str, Any]) -> dict[str, Any]:
        """Solve an ARC task using the Runtime.

        This is a convenience method that combines prepare_request,
        execute, and format_response.

        Args:
            task_data: JSON representation of the task

        Returns:
            Solution dictionary
        """
        await self._ensure_initialized()

        request = self.prepare_request(task_data)
        response = await self._pipeline.execute(request)

        # Track history
        self._task_history.append({
            "task_id": task_data.get("id"),
            "confidence": response.confidence,
        })

        return self.format_response(response)

    def format_response(
        self,
        response: ARCResponse,
        format_type: str = "simple",
    ) -> dict[str, Any]:
        """Format a Runtime response for application use.

        Args:
            response: Standard ARC response from Runtime
            format_type: Format type ('simple', 'full', 'solution')

        Returns:
            Formatted response
        """
        if format_type == "simple":
            return ARCResponseFormatter.to_simple_dict(response)
        elif format_type == "solution":
            return ARCResponseFormatter.to_solution(response)
        else:
            # Full format
            return {
                "response_id": response.response_id,
                "request_id": response.request_id,
                "status": response.status,
                "output": response.result.primary_output,
                "confidence": response.confidence,
                "pattern": response.result.pattern_type,
                "learned_from_memory": response.result.learned_from_memory,
                "trace": [
                    {
                        "step": s.step,
                        "stage": s.stage,
                        "action": s.action,
                        "confidence": s.confidence,
                    }
                    for s in response.trace
                ],
                "metadata": response.metadata,
            }

    def get_history(self) -> list[dict[str, Any]]:
        """Get the history of solved tasks.

        Returns:
            List of task metadata
        """
        return self._task_history

    # Legacy compatibility methods
    def load_task(self, task_data: dict[str, Any]) -> dict[str, Any]:
        """Legacy: Load an ARC task from JSON data.

        Deprecated: Use prepare_request() instead.
        This method is provided for backward compatibility.

        Args:
            task_data: JSON representation of the task

        Returns:
            Task data dict
        """
        return task_data

    async def solve_batch(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Solve multiple ARC tasks.

        Args:
            tasks: List of ARC task JSON data

        Returns:
            List of solutions
        """
        return [await self.solve(task) for task in tasks]
