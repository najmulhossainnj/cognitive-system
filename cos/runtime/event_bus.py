"""Event Bus Implementation.

This module provides the Event Bus for pub/sub event handling.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class Event:
    """Represents an event in the system."""

    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = ""
    payload: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""


@dataclass
class Subscription:
    """Represents an event subscription."""

    id: str
    event_type: str
    handler: Callable[[Any], None]
    created_at: datetime = field(default_factory=datetime.now)


class EventBus:
    """Event Bus provides event publication and subscription.

    The Event Bus is responsible for:
    - Publishing events
    - Managing subscriptions
    - Supporting event replay

    See RUNTIME-003 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the event bus."""
        self._subscriptions: dict[str, Subscription] = {}
        self._type_index: dict[str, list[str]] = {}
        self._event_history: list[Event] = []
        self._max_history: int = 1000

    async def publish(self, event: Event | Any) -> str:
        """Publish an event.

        Args:
            event: Event to publish (can be Event object or any payload)

        Returns:
            Event ID
        """
        if not isinstance(event, Event):
            event = Event(type=getattr(event, "__class__", type(event)).__name__, payload=event)

        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

        subscriptions = self._type_index.get(event.type, [])
        for sub_id in subscriptions:
            subscription = self._subscriptions.get(sub_id)
            if subscription:
                try:
                    handler = subscription.handler
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception:
                    pass

        wildcard_subs = self._type_index.get("*", [])
        for sub_id in wildcard_subs:
            subscription = self._subscriptions.get(sub_id)
            if subscription and subscription.event_type == "*":
                try:
                    handler = subscription.handler
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event)
                    else:
                        handler(event)
                except Exception:
                    pass

        return event.id

    def subscribe(
        self,
        event_type: str,
        handler: Callable[[Any], None],
    ) -> str:
        """Subscribe to events.

        Args:
            event_type: Type of events to subscribe to
            handler: Handler function

        Returns:
            Subscription ID
        """
        sub_id = str(uuid4())
        subscription = Subscription(
            id=sub_id,
            event_type=event_type,
            handler=handler,
        )
        self._subscriptions[sub_id] = subscription

        if event_type not in self._type_index:
            self._type_index[event_type] = []
        self._type_index[event_type].append(sub_id)

        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events.

        Args:
            subscription_id: Subscription to remove

        Returns:
            True if unsubscribed
        """
        subscription = self._subscriptions.pop(subscription_id, None)
        if subscription:
            event_type = subscription.event_type
            if event_type in self._type_index:
                try:
                    self._type_index[event_type].remove(subscription_id)
                except ValueError:
                    pass
            return True
        return False

    def replay(
        self,
        event_type: str | None = None,
        from_event_id: str | None = None,
    ) -> list[Event]:
        """Replay events.

        Args:
            event_type: Filter by event type
            from_event_id: Start replay from this event ID

        Returns:
            List of events
        """
        events = self._event_history.copy()

        if from_event_id:
            start_idx = 0
            for i, e in enumerate(events):
                if e.id == from_event_id:
                    start_idx = i + 1
                    break
            events = events[start_idx:]

        if event_type:
            events = [e for e in events if e.type == event_type]

        return events

    async def clear(self) -> None:
        """Clear all events and subscriptions."""
        self._event_history.clear()
        self._subscriptions.clear()
        self._type_index.clear()

    def get_subscriptions(self, event_type: str) -> list[str]:
        """Get subscriptions for an event type.

        Args:
            event_type: Event type

        Returns:
            List of subscription IDs
        """
        return self._type_index.get(event_type, []).copy()

    def get_all_subscriptions(self) -> dict[str, list[str]]:
        """Get all subscriptions grouped by event type.

        Returns:
            Dictionary of event types to subscription IDs
        """
        return {k: v.copy() for k, v in self._type_index.items()}

    def set_max_history(self, max_size: int) -> None:
        """Set maximum history size.

        Args:
            max_size: Maximum number of events to keep
        """
        self._max_history = max_size
        while len(self._event_history) > self._max_history:
            self._event_history.pop(0)


# Module-level singleton instance
_event_bus: EventBus | None = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance.

    Returns:
        EventBus instance
    """
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


# Re-export interface for type hints
IEventBus = EventBus
