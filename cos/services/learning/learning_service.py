"""Learning Services Implementation.

This module provides learning services for experience-based improvement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Experience:
    """Represents a learning experience."""

    id: str
    situation: dict[str, Any]
    action: dict[str, Any]
    outcome: dict[str, Any]
    reward: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class LearningService:
    """Learning Service for experience-based improvement.

    Provides general learning capabilities.
    """

    def __init__(self) -> None:
        """Initialize the learning service."""
        self._experiences: list[Experience] = []
        self._models: dict[str, Any] = {}

    async def learn(self, experience: Any) -> dict[str, Any]:
        """Learn from an experience.

        Args:
            experience: Experience to learn from

        Returns:
            Learning result
        """
        exp_dict = experience.model_dump() if hasattr(experience, "model_dump") else (
            experience if isinstance(experience, dict) else {}
        )

        exp_id = exp_dict.get("id", str(datetime.now().timestamp()))
        exp = Experience(
            id=exp_id,
            situation=exp_dict.get("situation", {}),
            action=exp_dict.get("action", {}),
            outcome=exp_dict.get("outcome", {}),
            reward=exp_dict.get("reward", 0.0),
        )
        self._experiences.append(exp)

        return {
            "experience_id": exp_id,
            "learned": True,
            "total_experiences": len(self._experiences),
        }

    async def recall(self, situation: dict[str, Any]) -> list[Experience]:
        """Recall similar experiences.

        Args:
            situation: Situation to recall for

        Returns:
            Similar experiences
        """
        similar = []

        for exp in reversed(self._experiences):
            if self._similar_situations(situation, exp.situation):
                similar.append(exp)
                if len(similar) >= 5:
                    break

        return similar

    def _similar_situations(self, s1: dict[str, Any], s2: dict[str, Any]) -> bool:
        """Check if situations are similar."""
        common_keys = set(s1.keys()) & set(s2.keys())
        if not common_keys:
            return False

        matches = sum(1 for k in common_keys if s1.get(k) == s2.get(k))
        return matches >= len(common_keys) * 0.5

    async def get_insights(self) -> list[str]:
        """Get learned insights.

        Returns:
            List of insights
        """
        if not self._experiences:
            return []

        avg_reward = sum(e.reward for e in self._experiences) / len(self._experiences)
        return [
            f"Average reward: {avg_reward:.2f}",
            f"Total experiences: {len(self._experiences)}",
        ]


class ExperienceLearningService:
    """Experience Learning Service.

    Focuses on learning from past experiences.
    """

    def __init__(self) -> None:
        """Initialize the experience learner."""
        self._experiences: list[Experience] = []

    async def record(
        self,
        situation: dict[str, Any],
        action: dict[str, Any],
        outcome: dict[str, Any],
    ) -> str:
        """Record an experience.

        Args:
            situation: Observed situation
            action: Action taken
            outcome: Resulting outcome

        Returns:
            Experience ID
        """
        exp_id = str(datetime.now().timestamp())
        exp = Experience(
            id=exp_id,
            situation=situation,
            action=action,
            outcome=outcome,
        )
        self._experiences.append(exp)
        return exp_id

    async def retrieve_similar(self, situation: dict[str, Any], limit: int = 5) -> list[Experience]:
        """Retrieve similar experiences.

        Args:
            situation: Situation to match
            limit: Maximum results

        Returns:
            Similar experiences
        """
        results = []
        for exp in reversed(self._experiences):
            if self._matches_situation(situation, exp.situation):
                results.append(exp)
                if len(results) >= limit:
                    break
        return results

    def _matches_situation(self, s1: dict[str, Any], s2: dict[str, Any]) -> bool:
        """Check if situations match."""
        return any(s1.get(k) == s2.get(k) for k in s1 if k in s2)


class HeuristicLearningService:
    """Heuristic Learning Service.

    Focuses on learning and refining heuristics.
    """

    def __init__(self) -> None:
        """Initialize the heuristic learner."""
        self._heuristics: dict[str, float] = {}

    async def update_heuristic(self, heuristic: str, feedback: float) -> None:
        """Update a heuristic based on feedback.

        Args:
            heuristic: Heuristic identifier
            feedback: Feedback value
        """
        current = self._heuristics.get(heuristic, 0.5)
        learning_rate = 0.1
        self._heuristics[heuristic] = current + learning_rate * (feedback - current)

    async def get_heuristic(self, heuristic: str) -> float:
        """Get heuristic value.

        Args:
            heuristic: Heuristic identifier

        Returns:
            Heuristic value
        """
        return self._heuristics.get(heuristic, 0.5)


class PolicyLearningService:
    """Policy Learning Service.

    Focuses on policy improvement.
    """

    def __init__(self) -> None:
        """Initialize the policy learner."""
        self._policies: dict[str, dict[str, float]] = {}

    async def update_policy(self, state: str, action: str, value: float) -> None:
        """Update policy value.

        Args:
            state: State identifier
            action: Action identifier
            value: Value to update
        """
        if state not in self._policies:
            self._policies[state] = {}
        self._policies[state][action] = value

    async def get_best_action(self, state: str) -> str | None:
        """Get best action for state.

        Args:
            state: State identifier

        Returns:
            Best action or None
        """
        state_policy = self._policies.get(state, {})
        if not state_policy:
            return None

        return max(state_policy, key=state_policy.get)


# Re-export interfaces
ILearningService = LearningService
IExperienceLearningService = ExperienceLearningService
IHeuristicLearningService = HeuristicLearningService
IPolicyLearningService = PolicyLearningService
