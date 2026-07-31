"""Decision Service Interfaces.

This module defines interfaces for decision services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Decision, Plan, Policy


class IDecisionService(IService):
    """Decision Service interface.

    Base interface for decision service implementations.
    Services include: Utility, Policy, Risk decision engines.

    See SERVICE-500 for base specification.
    """

    async def select_plan(self, plans: list[Plan]) -> Decision:
        """Select the best plan.

        Args:
            plans: Candidate plans

        Returns:
            Selected decision
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def evaluate_plan(self, plan: Plan) -> dict[str, Any]:
        """Evaluate a plan.

        Args:
            plan: Plan to evaluate

        Returns:
            Evaluation results
        """
        raise NotImplementedError("Will be implemented in Phase 8")


class IUtilityDecisionService(IDecisionService):
    """Utility Decision Service interface.

    See SERVICE-510 for full specification.
    """

    async def calculate_utility(self, plan: Plan) -> float:
        """Calculate plan utility.

        Args:
            plan: Plan to evaluate

        Returns:
            Utility score
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def compare_utilities(
        self,
        plan_a: Plan,
        plan_b: Plan,
    ) -> Plan:
        """Compare utilities of two plans.

        Args:
            plan_a: First plan
            plan_b: Second plan

        Returns:
            Plan with higher utility
        """
        raise NotImplementedError("Will be implemented in Phase 8")


class IPolicyEngineService(IDecisionService):
    """Policy Engine Service interface.

    See SERVICE-520 for full specification.
    """

    async def evaluate_policy(
        self,
        plan: Plan,
        policy: Policy,
    ) -> bool:
        """Evaluate a plan against policy.

        Args:
            plan: Plan to evaluate
            policy: Policy to check

        Returns:
            True if compliant
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def add_policy(self, policy: Policy) -> None:
        """Add a policy.

        Args:
            policy: Policy to add
        """
        raise NotImplementedError("Will be implemented in Phase 8")


class IRiskAssessmentService(IDecisionService):
    """Risk Assessment Service interface.

    See SERVICE-530 for full specification.
    """

    async def assess_risk(self, plan: Plan) -> float:
        """Assess plan risk.

        Args:
            plan: Plan to assess

        Returns:
            Risk score
        """
        raise NotImplementedError("Will be implemented in Phase 8")

    async def identify_risks(self, plan: Plan) -> list[dict[str, Any]]:
        """Identify plan risks.

        Args:
            plan: Plan to check

        Returns:
            Identified risks
        """
        raise NotImplementedError("Will be implemented in Phase 8")
