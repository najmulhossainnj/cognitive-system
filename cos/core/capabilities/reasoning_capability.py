"""Reasoning Capability Interface.

This module defines the public interface for the Reasoning Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Confidence, Observation, Problem, Solution


class IReasoningCapability:
    """Reasoning Capability provides the primary problem-solving interface.

    The Reasoning Capability is responsible for:
    - Solving problems
    - Generating hypotheses
    - Evaluating alternatives
    - Verifying candidate solutions
    - Coordinating reasoning strategies
    - Producing explanations
    - Estimating confidence

    See COS-CORE-100 for full specification.
    """

    async def solve(self, problem: Problem) -> Solution:
        """Solve a reasoning problem.

        Args:
            problem: The problem to solve

        Returns:
            A solution with explanation and confidence
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def analyze(self, observation: Observation) -> dict[str, Any]:
        """Analyze an observation.

        Args:
            observation: The observation to analyze

        Returns:
            Analysis results
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def infer(self, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Perform inference on facts.

        Args:
            facts: List of facts to reason about

        Returns:
            Inferred conclusions
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def verify(self, candidate: Solution) -> bool:
        """Verify a candidate solution.

        Args:
            candidate: The candidate solution to verify

        Returns:
            True if solution is valid
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def compare(
        self,
        options: list[Solution],
    ) -> list[tuple[Solution, float]]:
        """Compare solution options.

        Args:
            options: List of candidate solutions

        Returns:
            Ranked solutions with scores
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def synthesize(
        self,
        parts: list[dict[str, Any]],
    ) -> Solution:
        """Synthesize a solution from parts.

        Args:
            parts: Components to synthesize

        Returns:
            Synthesized solution
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def evaluate(self, solution: Solution) -> Confidence:
        """Evaluate a solution.

        Args:
            solution: The solution to evaluate

        Returns:
            Confidence score and rationale
        """
        raise NotImplementedError("Will be implemented in Phase 6")

    async def explain(self, result: Solution) -> str:
        """Generate explanation for a result.

        Args:
            result: The result to explain

        Returns:
            Human-readable explanation
        """
        raise NotImplementedError("Will be implemented in Phase 6")
