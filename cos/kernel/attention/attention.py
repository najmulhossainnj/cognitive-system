"""Attention - Focus management for COS."""

from __future__ import annotations


class IAttention:
    """Attention mechanism for managing cognitive focus.

    The attention mechanism is responsible for:
    - Tracking active context items
    - Managing attention windows
    - Prioritizing information
    - Handling context switching
    """

    async def focus(self, item: object) -> None:
        """Focus attention on an item.

        Args:
            item: The item to focus on
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def unfocus(self, item: object) -> None:
        """Remove item from attention.

        Args:
            item: The item to unfocus
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def get_focused(self) -> list[object]:
        """Get currently focused items.

        Returns:
            List of focused items
        """
        raise NotImplementedError("Will be implemented in Phase 2")
