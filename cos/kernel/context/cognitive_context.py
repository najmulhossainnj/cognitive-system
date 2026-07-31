"""Cognitive Context - Primary execution environment for COS."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from cos.execution.context import CognitiveContext as ExecutionContext
from cos.runtime import (
    get_configuration_manager,
    get_event_bus,
    get_scheduler,
)

if TYPE_CHECKING:
    pass


class KernelNamespace:
    """Kernel namespace for accessing operating system infrastructure."""

    def __init__(self, context: CognitiveContext) -> None:
        """Initialize kernel namespace.

        Args:
            context: Parent cognitive context
        """
        self._context = context

    @property
    def scheduler(self) -> Any:
        """Access the task scheduler."""
        return get_scheduler()

    @property
    def events(self) -> Any:
        """Access the event bus."""
        return get_event_bus()

    @property
    def configuration(self) -> Any:
        """Access configuration management."""
        return get_configuration_manager()

    @property
    def attention(self) -> Any:
        """Access attention mechanism."""
        return self._context._attention


class CognitionNamespace:
    """Cognition namespace for accessing cognitive capabilities through the broker."""

    def __init__(self, context: CognitiveContext) -> None:
        """Initialize cognition namespace.

        Args:
            context: Parent cognitive context
        """
        self._context = context

    @property
    def reasoning(self) -> Any:
        """Access reasoning capability."""
        return self._context._execution_context.cognition.reasoning

    @property
    def memory(self) -> Any:
        """Access memory capability."""
        return self._context._execution_context.cognition.memory

    @property
    def world(self) -> Any:
        """Access world model capability."""
        return self._context._execution_context.cognition.world

    @property
    def planning(self) -> Any:
        """Access planning capability."""
        return self._context._execution_context.cognition.planning

    @property
    def decision(self) -> Any:
        """Access decision capability."""
        return self._context._execution_context.cognition.decision

    @property
    def learning(self) -> Any:
        """Access learning capability."""
        return self._context._execution_context.cognition.learning

    @property
    def meta(self) -> Any:
        """Access meta-cognition capability."""
        return self._context._execution_context.cognition.meta

    @property
    def assistant(self) -> Any:
        """Access assistant capability."""
        return self._context._execution_context.cognition.assistant


class CognitiveContext:
    """Primary execution environment for the Cognitive Operating System.

    Every module receives a CognitiveContext which provides access to all
    operating system and cognitive capabilities.

    The context contains two primary namespaces:
    - kernel: OS infrastructure (scheduler, events, telemetry, configuration)
    - cognition: Reusable cognitive capabilities

    Example:
        >>> context = CognitiveContext.create()
        >>> context.cognition.reasoning.solve(task)
        >>> context.kernel.events.publish(event)
    """

    def __init__(
        self,
        execution_context: ExecutionContext | None = None,
    ) -> None:
        """Initialize the cognitive context.

        Args:
            execution_context: The execution context instance
        """
        from cos.kernel.attention.attention import Attention

        self._execution_context = execution_context or ExecutionContext()
        self._attention = Attention()
        self._initialized = False

    @classmethod
    def create(cls) -> CognitiveContext:
        """Create a new cognitive context with default configuration.

        Returns:
            A new CognitiveContext instance
        """
        context = cls()
        return context

    @property
    def kernel(self) -> KernelNamespace:
        """Access kernel infrastructure."""
        return KernelNamespace(self)

    @property
    def cognition(self) -> CognitionNamespace:
        """Access cognitive capabilities through the broker."""
        return CognitionNamespace(self)

    async def initialize(self) -> None:
        """Initialize the context."""
        if not self._initialized:
            await self._execution_context.initialize()
            self._initialized = True

    def shutdown(self) -> None:
        """Shutdown the context and release resources."""
        import asyncio
        _task = asyncio.create_task(self._execution_context.destroy_context())
        self._initialized = False


# Re-export
ICognitiveContext = CognitiveContext
