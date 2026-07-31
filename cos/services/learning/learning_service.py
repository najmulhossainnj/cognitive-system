"""Learning Service Interfaces.

This module defines interfaces for learning services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Dataset, Experience, LearningMetrics


class ILearningService(IService):
    """Learning Service interface.

    Base interface for learning service implementations.
    Services include: Experience, Heuristic, Policy learning.

    See SERVICE-600 for base specification.
    """

    async def record_experience(self, experience: Experience) -> None:
        """Record an experience.

        Args:
            experience: Experience to record
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def analyze_history(
        self,
        experiences: list[Experience],
    ) -> dict[str, Any]:
        """Analyze experience history.

        Args:
            experiences: Past experiences

        Returns:
            Analysis results
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def learn(self, dataset: Dataset) -> dict[str, Any]:
        """Learn from dataset.

        Args:
            dataset: Dataset to learn from

        Returns:
            Learning results
        """
        raise NotImplementedError("Will be implemented in Phase 9")

    async def get_metrics(self) -> LearningMetrics:
        """Get learning metrics.

        Returns:
            Learning metrics
        """
        raise NotImplementedError("Will be implemented in Phase 9")


class IExperienceLearningService(ILearningService):
    """Experience Learning Service interface.

    See SERVICE-610 for full specification.
    """

    async def extract_patterns(
        self,
        experiences: list[Experience],
    ) -> list[dict[str, Any]]:
        """Extract patterns from experiences.

        Args:
            experiences: Experiences to analyze

        Returns:
            Extracted patterns
        """
        raise NotImplementedError("Will be implemented in Phase 9")


class IHeuristicLearningService(ILearningService):
    """Heuristic Learning Service interface.

    See SERVICE-620 for full specification.
    """

    async def refine_heuristics(
        self,
        experiences: list[Experience],
    ) -> list[dict[str, Any]]:
        """Refine heuristics.

        Args:
            experiences: Experiences to learn from

        Returns:
            Refined heuristics
        """
        raise NotImplementedError("Will be implemented in Phase 9")


class IPolicyLearningService(ILearningService):
    """Policy Learning Service interface.

    See SERVICE-630 for full specification.
    """

    async def improve_policy(
        self,
        experiences: list[Experience],
        policy_id: str,
    ) -> dict[str, Any]:
        """Improve a policy.

        Args:
            experiences: Learning experiences
            policy_id: Policy to improve

        Returns:
            Improved policy
        """
        raise NotImplementedError("Will be implemented in Phase 9")
