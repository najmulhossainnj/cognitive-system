"""World Model Capability Interface.

This module defines the public interface for the World Model Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import Constraint, Entity, Hypothesis, Pattern, Relationship


class IWorldModelCapability:
    """World Model Capability provides semantic representation of the environment.

    The World Model Capability is responsible for:
    - Maintaining semantic state
    - Maintaining object relationships
    - Representing constraints
    - Exposing graph queries
    - Validating hypotheses
    - Detecting inconsistencies

    See COS-CORE-120 for full specification.
    """

    async def query(self, criteria: dict[str, Any]) -> list[Entity]:
        """Query the world model.

        Args:
            criteria: Query criteria

        Returns:
            List of matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def match(self, pattern: Pattern) -> list[Entity]:
        """Match entities against a pattern.

        Args:
            pattern: Pattern to match

        Returns:
            List of matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def validate(self, hypothesis: Hypothesis) -> dict[str, Any]:
        """Validate a hypothesis.

        Args:
            hypothesis: The hypothesis to validate

        Returns:
            Validation result with explanation
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def traverse(
        self,
        graph_query: dict[str, Any],
    ) -> list[Relationship]:
        """Traverse the graph.

        Args:
            graph_query: Graph traversal query

        Returns:
            List of traversed relationships
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def neighbors(self, entity: Entity) -> list[Entity]:
        """Get neighboring entities.

        Args:
            entity: The source entity

        Returns:
            List of neighboring entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def constraints(self, entity: Entity) -> list[Constraint]:
        """Get constraints for an entity.

        Args:
            entity: The entity to get constraints for

        Returns:
            List of constraints
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def infer_relationships(
        self,
        entity: Entity,
    ) -> list[Relationship]:
        """Infer relationships for an entity.

        Args:
            entity: The source entity

        Returns:
            List of inferred relationships
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def check_consistency(self) -> dict[str, Any]:
        """Check world model consistency.

        Returns:
            Consistency check results
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def abstract(self, region: dict[str, Any]) -> Entity:
        """Abstract a region.

        Args:
            region: Region to abstract

        Returns:
            Abstracted entity
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def find_equivalent(self, entity: Entity) -> list[Entity]:
        """Find equivalent entities.

        Args:
            entity: The source entity

        Returns:
            List of equivalent entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def detect_patterns(self) -> list[Pattern]:
        """Detect patterns in the world model.

        Returns:
            List of detected patterns
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def find_candidates(self, goal: dict[str, Any]) -> list[Entity]:
        """Find candidate entities for a goal.

        Args:
            goal: The goal to find candidates for

        Returns:
            List of candidate entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")
