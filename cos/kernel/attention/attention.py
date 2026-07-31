"""Attention - Focus management for COS."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AttentionItem:
    """Represents an item in attention."""

    id: str
    content: Any
    priority: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0


class Attention:
    """Attention mechanism for managing cognitive focus.

    The attention mechanism is responsible for:
    - Tracking active context items
    - Managing attention windows
    - Prioritizing information
    - Handling context switching
    """

    def __init__(self, max_items: int = 7) -> None:
        """Initialize attention.

        Args:
            max_items: Maximum items in attention window
        """
        self._max_items = max_items
        self._items: dict[str, AttentionItem] = {}

    async def focus(self, item_id: str, content: Any, priority: float = 0.5) -> None:
        """Focus attention on an item.

        Args:
            item_id: Unique identifier for the item
            content: The content to focus on
            priority: Priority level (0.0 to 1.0)
        """
        item = AttentionItem(
            id=item_id,
            content=content,
            priority=priority,
        )
        self._items[item_id] = item
        await self._maintain_window()

    async def unfocus(self, item_id: str) -> None:
        """Remove item from attention.

        Args:
            item_id: The item to unfocus
        """
        if item_id in self._items:
            del self._items[item_id]

    def get_focused(self) -> list[AttentionItem]:
        """Get currently focused items.

        Returns:
            List of focused items sorted by priority
        """
        items = list(self._items.values())
        items.sort(key=lambda x: (x.priority, x.last_accessed), reverse=True)
        return items

    async def update_priority(self, item_id: str, priority: float) -> None:
        """Update the priority of a focused item.

        Args:
            item_id: Item identifier
            priority: New priority (0.0 to 1.0)
        """
        if item_id in self._items:
            self._items[item_id].priority = priority

    async def refresh(self, item_id: str) -> None:
        """Refresh an item's last accessed time.

        Args:
            item_id: Item identifier
        """
        if item_id in self._items:
            self._items[item_id].last_accessed = datetime.now()
            self._items[item_id].access_count += 1

    async def clear(self) -> None:
        """Clear all focused items."""
        self._items.clear()

    async def _maintain_window(self) -> None:
        """Maintain the attention window size."""
        if len(self._items) > self._max_items:
            items = list(self._items.values())
            items.sort(key=lambda x: (x.priority, x.last_accessed), reverse=True)

            items_to_remove = items[self._max_items:]
            for item in items_to_remove:
                del self._items[item.id]

    def get_count(self) -> int:
        """Get the number of focused items.

        Returns:
            Number of items in attention
        """
        return len(self._items)


# Re-export interface
IAttention = Attention
