"""Learning Capability Interface.

This module defines the public interface for the Learning Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Dataset, Experience, LearningMetrics


class ILearningCapability:
    """Learning Capability enables improvement through experience.

    The Learning Capability is responsible for:
    - Acquiring experience
    - Analyzing outcomes
    - Refining heuristics
    - Improving policies
    - Consolidating knowledge
    - Measuring effectiveness

    See COS-CORE-150 for full specification.
    """

    async def record(self, experience: Experience) -> None:
        """Record an experience.

        Args:
            experience: The experience to record
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def analyze(self, history: list[Experience]) -> dict[str, Any]:
        """Analyze experience history.

        Args:
            history: List of past experiences

        Returns:
            Analysis results
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def learn(self, dataset: Dataset) -> dict[str, Any]:
        """Learn from a dataset.

        Args:
            dataset: The dataset to learn from

        Returns:
            Learning results
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def refine(self, model: dict[str, Any]) -> dict[str, Any]:
        """Refine a model based on experience.

        Args:
            model: The model to refine

        Returns:
            Refined model
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def recommend(self) -> list[dict[str, Any]]:
        """Get improvement recommendations.

        Returns:
            List of recommendations
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def evaluate(self) -> LearningMetrics:
        """Evaluate learning effectiveness.

        Returns:
            Learning metrics
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def consolidate(self) -> None:
        """Consolidate learned knowledge."""
        raise NotImplementedError("Will be implemented in Phase 9")

    async def metrics(self) -> dict[str, Any]:
        """Get learning metrics.

        Returns:
            Current learning metrics
        """
        raise NotImplementedError("Will be implemented in Phase 9")
