"""Assistant Capability Interface.

This module defines the public interface for the Assistant Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Explanation, Query, Report, Trace


class IAssistantCapability:
    """Assistant Capability provides human-facing interface to cognition.

    The Assistant Capability is responsible for:
    - Explaining reasoning
    - Explaining decisions
    - Visualizing plans
    - Summarizing memory
    - Inspecting the World Model
    - Presenting learning progress
    - Providing developer diagnostics

    See COS-CORE-170 for full specification.
    """

    async def ask(self, query: Query) -> str:
        """Ask a question.

        Args:
            query: The query to answer

        Returns:
            Answer
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def explain(self, result: Any) -> Explanation:
        """Explain a result.

        Args:
            result: The result to explain

        Returns:
            Explanation
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def visualize(self, data: Any) -> dict[str, Any]:
        """Visualize data.

        Args:
            data: Data to visualize

        Returns:
            Visualization data
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def inspect(self, target: str) -> dict[str, Any]:
        """Inspect a system component.

        Args:
            target: What to inspect

        Returns:
            Inspection results
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def trace(self, execution_id: str) -> Trace:
        """Get execution trace.

        Args:
            execution_id: The execution to trace

        Returns:
            Execution trace
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def report(self) -> Report:
        """Generate system report.

        Returns:
            System report
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def summarize(self, data: Any) -> str:
        """Summarize data.

        Args:
            data: Data to summarize

        Returns:
            Summary
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def guide(self, topic: str) -> str:
        """Provide guidance on a topic.

        Args:
            topic: Topic to guide on

        Returns:
            Guidance
        """
        raise NotImplementedError("Will be implemented in Phase 11")
