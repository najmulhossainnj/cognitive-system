"""Memory Capability Interface.

This module defines the public interface for the Memory Capability.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.shared.models import MemoryItem, Query, RetrievalCriteria


class IMemoryCapability:
    """Memory Capability provides unified interface for knowledge storage and retrieval.

    The Memory Capability is responsible for:
    - Storing knowledge
    - Retrieving knowledge
    - Organizing knowledge
    - Consolidating experiences
    - Managing memory lifecycle

    See COS-CORE-110 for full specification.
    """

    async def store(self, item: MemoryItem) -> None:
        """Store an item in memory.

        Args:
            item: The memory item to store
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def retrieve(self, criteria: RetrievalCriteria) -> list[MemoryItem]:
        """Retrieve items matching criteria.

        Args:
            criteria: Retrieval criteria

        Returns:
            List of matching memory items
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def search(self, query: Query) -> list[MemoryItem]:
        """Search memory with a query.

        Args:
            query: Search query

        Returns:
            List of matching items
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def remember(self, entity: dict[str, Any]) -> MemoryItem | None:
        """Remember an entity.

        Args:
            entity: Entity information

        Returns:
            The remembered memory item
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def forget(self, entity: dict[str, Any]) -> bool:
        """Forget an entity.

        Args:
            entity: Entity to forget

        Returns:
            True if forgotten successfully
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def update(self, entity: dict[str, Any]) -> MemoryItem:
        """Update a memory entity.

        Args:
            entity: Updated entity information

        Returns:
            The updated memory item
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    async def consolidate(self) -> None:
        """Consolidate memory for improved organization."""
        raise NotImplementedError("Will be implemented in Phase 4")

    def working(self) -> IMemoryCapability:
        """Access working memory.

        Returns:
            Working memory interface
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    def episodic(self) -> IMemoryCapability:
        """Access episodic memory.

        Returns:
            Episodic memory interface
        """
        raise NotImplementedError("Will be implemented in Phase 4")

    def semantic(self) -> IMemoryCapability:
        """Access semantic memory.

        Returns:
            Semantic memory interface
        """
        raise NotImplementedError("Will be implemented in Phase 4")
