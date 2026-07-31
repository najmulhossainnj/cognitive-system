"""Meta-Cognition Capability Interface.

This module defines the public interface for the Meta-Cognition Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import CognitiveState, Confidence, ReflectionReport


class IMetaCognitionCapability:
    """Meta-Cognition Capability enables self-observation and regulation.

    The Meta-Cognition Capability is responsible for:
    - Monitoring cognitive execution
    - Estimating confidence
    - Identifying failures
    - Evaluating strategies
    - Recommending improvements
    - Assessing execution quality

    See COS-CORE-160 for full specification.
    """

    async def monitor(self) -> dict[str, Any]:
        """Monitor cognitive execution.

        Returns:
            Current monitoring state
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def reflect(self, state: CognitiveState) -> ReflectionReport:
        """Perform reflection on cognitive state.

        Args:
            state: The cognitive state to reflect on

        Returns:
            Reflection report
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def evaluate(self, state: CognitiveState) -> dict[str, Any]:
        """Evaluate cognitive performance.

        Args:
            state: The state to evaluate

        Returns:
            Evaluation results
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def diagnose(self) -> dict[str, Any]:
        """Diagnose cognitive issues.

        Returns:
            Diagnostic results
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def confidence(self) -> Confidence:
        """Estimate cognitive confidence.

        Returns:
            Confidence estimate
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def recommend(self) -> list[dict[str, Any]]:
        """Generate improvement recommendations.

        Returns:
            List of recommendations
        """
        raise NotImplementedError("Will be implemented in Phase 10")

    async def report(self) -> dict[str, Any]:
        """Generate meta-cognition report.

        Returns:
            Meta-cognition report
        """
        raise NotImplementedError("Will be implemented in Phase 10")
