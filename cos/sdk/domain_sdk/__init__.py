"""Domain SDK for accessing cognitive capabilities."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cos.kernel.context.cognitive_context import CognitiveContext


class DomainSDK:
    """SDK for accessing cognitive capabilities through the context.

    This SDK provides a high-level interface to the cognitive system's
    domain-specific capabilities.
    """

    def __init__(self, context: CognitiveContext) -> None:
        """Initialize the domain SDK.

        Args:
            context: The cognitive context
        """
        self._context = context

    @property
    def reasoning(self) -> Any:
        """Access reasoning capabilities."""
        return self._context.cognition.reasoning

    @property
    def memory(self) -> Any:
        """Access memory capabilities."""
        return self._context.cognition.memory

    @property
    def world(self) -> Any:
        """Access world model capabilities."""
        return self._context.cognition.world

    @property
    def planning(self) -> Any:
        """Access planning capabilities."""
        return self._context.cognition.planning

    @property
    def decision(self) -> Any:
        """Access decision capabilities."""
        return self._context.cognition.decision

    @property
    def learning(self) -> Any:
        """Access learning capabilities."""
        return self._context.cognition.learning

    @property
    def meta(self) -> Any:
        """Access meta-cognition capabilities."""
        return self._context.cognition.meta

    @property
    def assistant(self) -> Any:
        """Access assistant capabilities."""
        return self._context.cognition.assistant

    async def solve(self, problem: Any) -> dict[str, Any]:
        """Solve a problem using reasoning.

        Args:
            problem: Problem to solve

        Returns:
            Solution
        """
        return await self.reasoning.solve(problem)

    async def remember(self, item: dict[str, Any]) -> None:
        """Store an item in memory.

        Args:
            item: Item to store
        """
        await self.memory.store(item)

    async def recall(self, query: Any) -> list[dict[str, Any]]:
        """Recall items from memory.

        Args:
            query: Query to recall

        Returns:
            Retrieved items
        """
        return await self.memory.query(query)


__all__ = ["DomainSDK"]
