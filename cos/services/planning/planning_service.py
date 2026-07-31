"""Planning Service Interfaces.

This module defines interfaces for planning services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Goal, Plan, ResourceEstimate, Task


class IPlanningService(IService):
    """Planning Service interface.

    Base interface for all planning service implementations.
    Services include: HTN, Graph, Constraint planners.

    See SERVICE-400 for base specification.
    """

    async def create_plan(self, goal: Goal) -> list[Plan]:
        """Create a plan for a goal.

        Args:
            goal: Goal to plan for

        Returns:
            Candidate plans
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def decompose_goal(self, goal: Goal) -> list[Goal]:
        """Decompose a goal.

        Args:
            goal: Goal to decompose

        Returns:
            Subgoals
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def estimate_cost(self, plan: Plan) -> ResourceEstimate:
        """Estimate plan cost.

        Args:
            plan: Plan to estimate

        Returns:
            Cost estimate
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def analyze_dependencies(self, plan: Plan) -> list[tuple[Task, list[Task]]]:
        """Analyze task dependencies.

        Args:
            plan: Plan to analyze

        Returns:
            Task dependencies
        """
        raise NotImplementedError("Will be implemented in Phase 7")


class IHTNPlanningService(IPlanningService):
    """HTN Planning Service interface.

    See SERVICE-410 for full specification.
    """

    async def apply_method(self, task: Task, methods: list[dict[str, Any]]) -> list[Task]:
        """Apply HTN method.

        Args:
            task: Task to decompose
            methods: Available methods

        Returns:
            Decomposed tasks
        """
        raise NotImplementedError("Will be implemented in Phase 7")


class IGraphPlanningService(IPlanningService):
    """Graph Planning Service interface.

    See SERVICE-420 for full specification.
    """

    async def build_state_graph(self, initial_state: dict[str, Any]) -> Any:
        """Build state graph.

        Args:
            initial_state: Initial state

        Returns:
            State graph
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def find_path(
        self,
        start_state: dict[str, Any],
        goal_state: dict[str, Any],
    ) -> list[Task]:
        """Find path in state graph.

        Args:
            start_state: Start state
            goal_state: Goal state

        Returns:
            Path as tasks
        """
        raise NotImplementedError("Will be implemented in Phase 7")


class IConstraintPlanningService(IPlanningService):
    """Constraint Planning Service interface.

    See SERVICE-430 for full specification.
    """

    async def validate_constraints(self, plan: Plan) -> bool:
        """Validate plan constraints.

        Args:
            plan: Plan to validate

        Returns:
            True if valid
        """
        raise NotImplementedError("Will be implemented in Phase 7")

    async def find_constraint_conflicts(self, plan: Plan) -> list[dict[str, Any]]:
        """Find constraint conflicts.

        Args:
            plan: Plan to check

        Returns:
            Conflicts
        """
        raise NotImplementedError("Will be implemented in Phase 7")
