"""Assistant Service Interfaces.

This module defines interfaces for assistant services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Explanation, Trace


class IAssistantService(IService):
    """Assistant Service interface.

    Base interface for assistant service implementations.
    Services include: Explanation, Trace visualization.

    See SERVICE-800 for base specification.
    """

    async def explain(self, result: Any) -> Explanation:
        """Explain a result.

        Args:
            result: Result to explain

        Returns:
            Explanation
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def visualize_trace(self, trace_id: str) -> dict[str, Any]:
        """Visualize a trace.

        Args:
            trace_id: Trace to visualize

        Returns:
            Visualization data
        """
        raise NotImplementedError("Will be implemented in Phase 11")


class IExplanationEngineService(IAssistantService):
    """Explanation Engine Service interface.

    See SERVICE-810 for full specification.
    """

    async def generate_explanation(
        self,
        result: Any,
        format: str = "text",
    ) -> str:
        """Generate explanation.

        Args:
            result: Result to explain
            format: Output format

        Returns:
            Explanation
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def get_evidence(self, result: Any) -> list[str]:
        """Get evidence for result.

        Args:
            result: Result to get evidence for

        Returns:
            Evidence list
        """
        raise NotImplementedError("Will be implemented in Phase 11")


class ITraceVisualizationService(IAssistantService):
    """Trace Visualization Service interface.

    See SERVICE-820 for full specification.
    """

    async def visualize(
        self,
        trace: Trace,
        format: str = "json",
    ) -> dict[str, Any]:
        """Visualize trace.

        Args:
            trace: Trace to visualize
            format: Output format

        Returns:
            Visualization
        """
        raise NotImplementedError("Will be implemented in Phase 11")

    async def create_timeline(self, trace: Trace) -> list[dict[str, Any]]:
        """Create timeline from trace.

        Args:
            trace: Trace to process

        Returns:
            Timeline events
        """
        raise NotImplementedError("Will be implemented in Phase 11")
