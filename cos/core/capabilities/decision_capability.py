"""Decision Capability Interface.

This module defines the public interface for the Decision Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Decision, Plan, Preference


class IDecisionCapability:
    """Decision Capability selects optimal course of action from alternatives.

    The Decision Capability is responsible for:
    - Evaluating alternatives
    - Selecting plans
    - Resolving conflicts
    - Assessing risk
    - Applying policies
    - Estimating utility

    See COS-CORE-140 for full specification.
    """

    async def select(self, plans: list[Plan]) -> Decision:
        """Select the best plan from alternatives.

        Args:
            plans: List of candidate plans

        Returns:
            Selected decision with rationale
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def evaluate(self, plan: Plan) -> dict[str, Any]:
        """Evaluate a plan.

        Args:
            plan: The plan to evaluate

        Returns:
            Evaluation results
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def compare(
        self,
        plan_a: Plan,
        plan_b: Plan,
    ) -> dict[str, Any]:
        """Compare two plans.

        Args:
            plan_a: First plan
            plan_b: Second plan

        Returns:
            Comparison results
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def utility(self, plan: Plan) -> float:
        """Calculate utility of a plan.

        Args:
            plan: The plan to evaluate

        Returns:
            Utility score
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def risk(self, plan: Plan) -> float:
        """Assess risk of a plan.

        Args:
            plan: The plan to assess

        Returns:
            Risk score
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def validate(self, plan: Plan) -> bool:
        """Validate a plan against policies.

        Args:
            plan: The plan to validate

        Returns:
            True if valid
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def justify(self, decision: Decision) -> str:
        """Generate justification for a decision.

        Args:
            decision: The decision to justify

        Returns:
            Human-readable justification
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def preferences(self) -> list[Preference]:
        """Get current preferences.

        Returns:
            List of preferences
        """
        raise NotImplementedError("Will be implemented in Phase 8")
