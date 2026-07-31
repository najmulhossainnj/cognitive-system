"""World Model Service Interfaces.

This module defines interfaces for world model services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.services.base import IService

if TYPE_CHECKING:
    from cos.shared.models import Constraint, Entity, Hypothesis, Pattern, Relationship


class IWorldModelService(IService):
    """World Model Service interface.

    Provides semantic representation of the environment.

    See SERVICE-300 for full specification.
    """

    async def query(self, criteria: dict[str, Any]) -> list[Entity]:
        """Query the world model.

        Args:
            criteria: Query criteria

        Returns:
            Matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def find(self, entity_type: str) -> list[Entity]:
        """Find entities by type.

        Args:
            entity_type: Entity type to find

        Returns:
            Matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def match(self, pattern: Pattern) -> list[Entity]:
        """Match entities against pattern.

        Args:
            pattern: Pattern to match

        Returns:
            Matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def validate(self, hypothesis: Hypothesis) -> dict[str, Any]:
        """Validate a hypothesis.

        Args:
            hypothesis: Hypothesis to validate

        Returns:
            Validation result
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def relationships(self, entity_id: str) -> list[Relationship]:
        """Get relationships for an entity.

        Args:
            entity_id: Entity ID

        Returns:
            Relationships
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def neighbors(self, entity_id: str) -> list[Entity]:
        """Get neighboring entities.

        Args:
            entity_id: Entity ID

        Returns:
            Neighboring entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def constraints(self, entity_id: str) -> list[Constraint]:
        """Get constraints for an entity.

        Args:
            entity_id: Entity ID

        Returns:
            Constraints
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def explain(self, entity_id: str) -> str:
        """Explain an entity.

        Args:
            entity_id: Entity ID

        Returns:
            Explanation
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def snapshot(self) -> str:
        """Create world model snapshot.

        Returns:
            Snapshot ID
        """
        raise NotImplementedError("Will be implemented in Phase 5")


class IKnowledgeGraphService(IService):
    """Knowledge Graph Service interface.

    See SERVICE-310 for full specification.
    """

    async def add_entity(self, entity: Entity) -> str:
        """Add an entity.

        Args:
            entity: Entity to add

        Returns:
            Entity ID
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def add_relationship(self, relationship: Relationship) -> str:
        """Add a relationship.

        Args:
            relationship: Relationship to add

        Returns:
            Relationship ID
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def traverse(
        self,
        start_id: str,
        path_pattern: dict[str, Any],
    ) -> list[Entity]:
        """Traverse the graph.

        Args:
            start_id: Starting entity
            path_pattern: Path pattern

        Returns:
            Traversed entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")


class ISemanticQueryService(IService):
    """Semantic Query Service interface.

    See SERVICE-320 for full specification.
    """

    async def semantic_search(self, query: str) -> list[Entity]:
        """Perform semantic search.

        Args:
            query: Search query

        Returns:
            Matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def find_similar(self, entity_id: str) -> list[Entity]:
        """Find similar entities.

        Args:
            entity_id: Entity to compare

        Returns:
            Similar entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")


class IConstraintValidationService(IService):
    """Constraint Validation Service interface.

    See SERVICE-330 for full specification.
    """

    async def validate_constraint(self, constraint: Constraint) -> bool:
        """Validate a constraint.

        Args:
            constraint: Constraint to validate

        Returns:
            True if valid
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def find_violations(self) -> list[dict[str, Any]]:
        """Find constraint violations.

        Returns:
            List of violations
        """
        raise NotImplementedError("Will be implemented in Phase 5")


class IPatternMatchingService(IService):
    """Pattern Matching Service interface.

    See SERVICE-340 for full specification.
    """

    async def match_pattern(self, pattern: Pattern) -> list[Entity]:
        """Match a pattern.

        Args:
            pattern: Pattern to match

        Returns:
            Matching entities
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def detect_symmetry(self) -> list[Pattern]:
        """Detect symmetry patterns.

        Returns:
            Detected patterns
        """
        raise NotImplementedError("Will be implemented in Phase 5")

    async def find_repetitions(self) -> list[Pattern]:
        """Find repetition patterns.

        Returns:
            Detected patterns
        """
        raise NotImplementedError("Will be implemented in Phase 5")
