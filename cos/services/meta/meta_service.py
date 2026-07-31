"""Meta-Cognition Service Interfaces.

This module defines interfaces for meta-cognition services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import CognitiveState, Confidence, ReflectionReport


class IMetaCognitionService(IService):
    """Meta-Cognition Service interface.

    Base interface for meta-cognition service implementations.
    Services include: Reflection, Confidence estimation.

    See SERVICE-700 for base specification.
    """

    async def reflect(self, state: CognitiveState) -> ReflectionReport:
        """Perform reflection.

        Args:
            state: Cognitive state

        Returns:
            Reflection report
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def monitor(self) -> dict[str, Any]:
        """Monitor cognitive performance.

        Returns:
            Monitoring data
        """
        raise NotImplementedError("Will be implemented in Phase 10")


class IReflectionService(IMetaCognitionService):
    """Reflection Service interface.

    See SERVICE-710 for full specification.
    """

    async def analyze_reasoning(self, reasoning_trace: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze reasoning trace.

        Args:
            reasoning_trace: Reasoning to analyze

        Returns:
            Analysis
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def generate_insights(self, state: CognitiveState) -> list[str]:
        """Generate insights.

        Args:
            state: Cognitive state

        Returns:
            Generated insights
        """
        raise NotImplementedError("Will be implemented in Phase 10")


class IConfidenceEstimationService(IMetaCognitionService):
    """Confidence Estimation Service interface.

    See SERVICE-720 for full specification.
    """

    async def estimate_confidence(
        self,
        state: CognitiveState,
    ) -> Confidence:
        """Estimate confidence.

        Args:
            state: Cognitive state

        Returns:
            Confidence estimate
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def get_confidence_factors(self, state: CognitiveState) -> list[str]:
        """Get confidence factors.

        Args:
            state: Cognitive state

        Returns:
            Factors affecting confidence
        """
        raise NotImplementedError("Will be implemented in Phase 10")
