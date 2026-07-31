"""Reasoning Service Interface.

This module defines the interface for reasoning services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Problem, Solution


class IReasoningService(IService):
    """Reasoning Service interface.

    This is the base interface for all reasoning service implementations.
    Services include: Rule, Symbolic, LLM, Neuro-Symbolic, Probabilistic, Hybrid.

    See SERVICE-100 through SERVICE-130 for specific implementations.
    """

    async def solve(self, problem: Problem) -> Solution:
        """Solve a problem.

        Args:
            problem: The problem to solve

        Returns:
            Solution
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def infer(self, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Perform inference.

        Args:
            facts: Facts to reason about

        Returns:
            Inferred conclusions
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def prove(self, goal: dict[str, Any]) -> dict[str, Any]:
        """Prove a goal.

        Args:
            goal: Goal to prove

        Returns:
            Proof result
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def explain(self, result: Solution) -> str:
        """Explain a result.

        Args:
            result: Result to explain

        Returns:
            Explanation
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def trace(self, result: Solution) -> list[dict[str, Any]]:
        """Get reasoning trace.

        Args:
            result: Result to trace

        Returns:
            Reasoning trace
        """
        raise NotImplementedError("Will be implemented in Phase 6")
