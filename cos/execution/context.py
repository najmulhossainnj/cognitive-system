"""Cognitive Context Implementation.

This module provides the Cognitive Context that manages execution state
and provides access to all cognitive capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from cos.broker.cognitive_broker import CognitiveBroker
from cos.execution.pipeline import CognitivePipeline, RequestLifecycle


class Cognition:
    """Cognition provides access to all cognitive capabilities.

    This interface provides a unified view of all cognitive services.
    """

    def __init__(self, broker: CognitiveBroker) -> None:
        """Initialize cognition.

        Args:
            broker: Cognitive broker
        """
        self._broker = broker

    @property
    def reasoning(self) -> Any:
        """Get reasoning capability.

        Returns:
            Reasoning capability
        """
        return self._broker.reasoning

    @property
    def memory(self) -> Any:
        """Get memory capability.

        Returns:
            Memory capability
        """
        return self._broker.memory

    @property
    def world(self) -> Any:
        """Get world model capability.

        Returns:
            World model capability
        """
        return self._broker.world

    @property
    def planning(self) -> Any:
        """Get planning capability.

        Returns:
            Planning capability
        """
        return self._broker.planning

    @property
    def decision(self) -> Any:
        """Get decision capability.

        Returns:
            Decision capability
        """
        return self._broker.decision

    @property
    def learning(self) -> Any:
        """Get learning capability.

        Returns:
            Learning capability
        """
        return self._broker.learning

    @property
    def meta(self) -> Any:
        """Get meta-cognition capability.

        Returns:
            Meta-cognition capability
        """
        return self._broker.meta

    @property
    def assistant(self) -> Any:
        """Get assistant capability.

        Returns:
            Assistant capability
        """
        return self._broker.assistant


@dataclass
class ContextState:
    """Represents the state of a cognitive context."""

    session_id: str
    execution_id: str
    created_at: datetime = field(default_factory=datetime.now)
    data: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)


class CognitiveContext:
    """Cognitive Context provides access to all cognitive capabilities.

    This is the primary interface through which applications access
    cognitive functionality.

    Example:
        >>> context = CognitiveContext()
        >>> await context.initialize()
        >>> result = await context.cognition.reasoning.solve(problem)
        >>> await context.destroy()
    """

    def __init__(self) -> None:
        """Initialize the cognitive context."""
        self._session_id = str(uuid4())
        self._execution_id = str(uuid4())
        self._initialized = False

        self._broker: CognitiveBroker | None = None
        self._pipeline: CognitivePipeline | None = None
        self._lifecycle: RequestLifecycle | None = None
        self._cognition: Cognition | None = None
        self._state: ContextState | None = None

    @property
    def cognition(self) -> Cognition:
        """Get cognitive capabilities.

        Returns:
            Cognition interface
        """
        if not self._initialized:
            raise RuntimeError("Context not initialized. Call initialize() first.")
        return self._cognition

    @property
    def session_id(self) -> str:
        """Get session ID.

        Returns:
            Current session ID
        """
        return self._session_id

    @property
    def execution_id(self) -> str:
        """Get execution ID.

        Returns:
            Current execution ID
        """
        return self._execution_id

    async def initialize(self) -> None:
        """Initialize the cognitive context."""
        if self._initialized:
            return

        self._broker = CognitiveBroker(context=self)
        await self._broker.initialize()

        self._pipeline = CognitivePipeline(self._broker)
        self._lifecycle = RequestLifecycle(self._pipeline)
        self._cognition = Cognition(self._broker)

        self._state = ContextState(
            session_id=self._session_id,
            execution_id=self._execution_id,
        )

        self._initialized = True

    async def create_context(self) -> CognitiveContext:
        """Create a new cognitive context.

        Returns:
            New context
        """
        new_context = CognitiveContext()
        await new_context.initialize()
        return new_context

    async def destroy_context(self) -> None:
        """Destroy this context."""
        if self._broker:
            await self._broker.shutdown()
        self._initialized = False
        self._broker = None
        self._pipeline = None
        self._lifecycle = None
        self._cognition = None
        self._state = None

    async def get_state(self) -> dict[str, Any]:
        """Get context state.

        Returns:
            Current state
        """
        if not self._state:
            return {"status": "not_initialized"}

        return {
            "session_id": self._state.session_id,
            "execution_id": self._state.execution_id,
            "created_at": self._state.created_at.isoformat(),
            "data_keys": list(self._state.data.keys()),
            "history_size": len(self._state.history),
        }

    async def set_data(self, key: str, value: Any) -> None:
        """Set context data.

        Args:
            key: Data key
            value: Data value
        """
        if self._state:
            self._state.data[key] = value

    async def get_data(self, key: str) -> Any | None:
        """Get context data.

        Args:
            key: Data key

        Returns:
            Data value or None
        """
        if self._state:
            return self._state.data.get(key)
        return None

    async def clear_data(self) -> None:
        """Clear context data."""
        if self._state:
            self._state.data.clear()

    async def submit_request(self, request: dict[str, Any]) -> str:
        """Submit a request to the pipeline.

        Args:
            request: Request to submit

        Returns:
            Request ID
        """
        if not self._lifecycle:
            raise RuntimeError("Context not initialized.")
        return await self._lifecycle.submit(request)

    async def get_request_status(self, request_id: str) -> dict[str, Any]:
        """Get request status.

        Args:
            request_id: Request ID

        Returns:
            Status
        """
        if not self._lifecycle:
            raise RuntimeError("Context not initialized.")
        return await self._lifecycle.get_status(request_id)

    async def get_request_result(self, request_id: str) -> dict[str, Any] | None:
        """Get request result.

        Args:
            request_id: Request ID

        Returns:
            Result or None
        """
        if not self._lifecycle:
            raise RuntimeError("Context not initialized.")
        return await self._lifecycle.get_result(request_id)

    async def cancel_request(self, request_id: str) -> bool:
        """Cancel a request.

        Args:
            request_id: Request to cancel

        Returns:
            True if cancelled
        """
        if not self._lifecycle:
            raise RuntimeError("Context not initialized.")
        return await self._lifecycle.cancel(request_id)


# Re-export interfaces
ICognitiveContext = CognitiveContext
ICognition = Cognition
