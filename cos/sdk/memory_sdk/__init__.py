"""Memory SDK for memory operations."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class MemorySDK:
    """SDK for memory operations.

    Provides a simplified interface to the cognitive system's memory capabilities.
    """

    def __init__(self, memory_capability: Any) -> None:
        """Initialize the memory SDK.

        Args:
            memory_capability: The memory capability instance
        """
        self._memory = memory_capability

    async def store(self, item: dict[str, Any], memory_type: str = "semantic") -> None:
        """Store an item in memory.

        Args:
            item: Item to store
            memory_type: Type of memory (working, semantic, episodic)
        """
        await self._memory.store(item, memory_type)

    async def query(
        self,
        query: Any,
        memory_type: str = "semantic",
    ) -> list[dict[str, Any]]:
        """Query memory.

        Args:
            query: Search query
            memory_type: Type of memory to query

        Returns:
            Query results
        """
        return await self._memory.query(query, memory_type)

    async def remember(self, item: dict[str, Any]) -> None:
        """Store in semantic memory (convenience method).

        Args:
            item: Item to remember
        """
        await self._memory.store(item, "semantic")

    async def forget(self, item_id: str) -> None:
        """Remove an item from memory.

        Args:
            item_id: ID of item to forget
        """
        pass


__all__ = ["MemorySDK"]
