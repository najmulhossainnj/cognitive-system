"""Event Bus - Event publication and subscription for COS."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class IEventBus:
    """Event bus for publishing and subscribing to system events.

    The event bus is responsible for:
    - Publishing events to subscribers
    - Managing event subscriptions
    - Ensuring event delivery
    - Supporting event replay for debugging
    """

    async def publish(self, event: object) -> None:
        """Publish an event to all subscribers.

        Args:
            event: The event to publish
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def subscribe(
        self,
        event_type: type[object],
        handler: Callable[[object], Any],
    ) -> str:
        """Subscribe to events of a specific type.

        Args:
            event_type: The type of events to subscribe to
            handler: Callback function to handle events

        Returns:
            Subscription ID for later unsubscription
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events.

        Args:
            subscription_id: The subscription ID to remove

        Returns:
            True if unsubscribed, False if not found
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def replay(self, from_event_id: str | None = None) -> list[object]:
        """Replay events for debugging.

        Args:
            from_event_id: Start replay from this event ID

        Returns:
            List of events for replay
        """
        raise NotImplementedError("Will be implemented in Phase 2")
