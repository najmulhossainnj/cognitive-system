"""Planning Capability Interface.

This module defines the public interface for the Planning Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Goal, Plan, ResourceEstimate, Task


class IPlanningCapability:
    """Planning Capability generates executable strategies for achieving goals.

    The Planning Capability is responsible for:
    - Generating plans
    - Decomposing goals
    - Generating alternative strategies
    - Estimating execution cost
    - Identifying dependencies
    - Evaluating feasibility

    See COS-CORE-130 for full specification.
    """

    async def plan(self, goal: Goal) -> list[Plan]:
        """Create plans for a goal.

        Args:
            goal: The goal to plan for

        Returns:
            List of candidate plans
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def decompose(self, goal: Goal) -> list[Goal]:
        """Decompose a goal into subgoals.

        Args:
            goal: The goal to decompose

        Returns:
            List of subgoals
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def generate(self, goal: Goal) -> list[Plan]:
        """Generate plans for a goal.

        Args:
            goal: The goal to generate plans for

        Returns:
            List of generated plans
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def evaluate(self, plan: Plan) -> dict[str, Any]:
        """Evaluate a plan.

        Args:
            plan: The plan to evaluate

        Returns:
            Evaluation results
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def alternatives(self, goal: Goal) -> list[Plan]:
        """Get alternative plans for a goal.

        Args:
            goal: The goal to get alternatives for

        Returns:
            List of alternative plans
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def estimate(self, plan: Plan) -> ResourceEstimate:
        """Estimate resources required for a plan.

        Args:
            plan: The plan to estimate

        Returns:
            Resource estimate
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def dependencies(self, plan: Plan) -> list[tuple[Task, list[Task]]]:
        """Analyze task dependencies in a plan.

        Args:
            plan: The plan to analyze

        Returns:
            List of task dependencies
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def feasible(self, plan: Plan) -> bool:
        """Check if a plan is feasible.

        Args:
            plan: The plan to check

        Returns:
            True if plan is feasible
        """
        raise NotImplementedError("Will be implemented in Phase 7")
