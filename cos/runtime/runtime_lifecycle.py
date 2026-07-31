"""Runtime Lifecycle Implementation.

This module provides the Runtime Lifecycle manager for coordinating runtime startup and shutdown.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from cos.runtime.configuration_manager import ConfigurationManager, get_configuration_manager
from cos.runtime.dependency_injection import DependencyInjection, get_dependency_injection
from cos.runtime.event_bus import EventBus, get_event_bus
from cos.runtime.scheduler import get_scheduler, Scheduler
from cos.runtime.service_registry import get_service_registry, ServiceRegistry


class RuntimeStatus(str, Enum):
    """Runtime status values."""

    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"


class RuntimeLifecycle:
    """Runtime Lifecycle manages runtime startup and shutdown.

    The Runtime Lifecycle is responsible for:
    - Initializing runtime
    - Starting services
    - Coordinating shutdown

    See RUNTIME-010 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the runtime lifecycle."""
        self._status = RuntimeStatus.CREATED
        self._registry: ServiceRegistry | None = None
        self._di: DependencyInjection | None = None
        self._event_bus: EventBus | None = None
        self._scheduler: Scheduler | None = None
        self._config: ConfigurationManager | None = None
        self._extensions: dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize the runtime."""
        if self._status != RuntimeStatus.CREATED:
            raise RuntimeError(f"Cannot initialize from status: {self._status}")

        self._registry = get_service_registry()
        self._di = get_dependency_injection()
        self._event_bus = get_event_bus()
        self._scheduler = get_scheduler()
        self._config = get_configuration_manager()

        self._config.load_dict({
            "runtime": {
                "status": "initialized",
                "version": "1.0.0",
            }
        })

        self._status = RuntimeStatus.INITIALIZED

    async def start(self) -> None:
        """Start the runtime."""
        if self._status not in (RuntimeStatus.INITIALIZED, RuntimeStatus.PAUSED):
            raise RuntimeError(f"Cannot start from status: {self._status}")

        self._status = RuntimeStatus.RUNNING

    async def stop(self) -> None:
        """Stop the runtime."""
        if self._status != RuntimeStatus.RUNNING:
            raise RuntimeError(f"Cannot stop from status: {self._status}")

        self._status = RuntimeStatus.STOPPING

    async def shutdown(self) -> None:
        """Shutdown the runtime."""
        await self.stop()

        if self._scheduler:
            await self._scheduler.pause()

        if self._event_bus:
            await self._event_bus.clear()

        self._status = RuntimeStatus.STOPPED

    async def get_status(self) -> dict[str, Any]:
        """Get runtime status.

        Returns:
            Status information
        """
        return {
            "status": self._status.value,
            "services": {
                "registry": self._registry is not None,
                "di": self._di is not None,
                "event_bus": self._event_bus is not None,
                "scheduler": self._scheduler is not None,
                "config": self._config is not None,
            },
            "extensions": list(self._extensions.keys()),
        }

    async def get_registry(self) -> ServiceRegistry:
        """Get the service registry.

        Returns:
            Service registry
        """
        if not self._registry:
            raise RuntimeError("Runtime not initialized")
        return self._registry

    async def get_di(self) -> DependencyInjection:
        """Get dependency injection.

        Returns:
            Dependency injection
        """
        if not self._di:
            raise RuntimeError("Runtime not initialized")
        return self._di

    async def get_event_bus(self) -> EventBus:
        """Get event bus.

        Returns:
            Event bus
        """
        if not self._event_bus:
            raise RuntimeError("Runtime not initialized")
        return self._event_bus

    async def get_scheduler(self) -> Scheduler:
        """Get scheduler.

        Returns:
            Scheduler
        """
        if not self._scheduler:
            raise RuntimeError("Runtime not initialized")
        return self._scheduler

    async def get_config(self) -> ConfigurationManager:
        """Get configuration manager.

        Returns:
            Configuration manager
        """
        if not self._config:
            raise RuntimeError("Runtime not initialized")
        return self._config

    async def register_extension(self, name: str, extension: Any) -> None:
        """Register a runtime extension.

        Args:
            name: Extension name
            extension: Extension instance
        """
        self._extensions[name] = extension

    async def get_extension(self, name: str) -> Any | None:
        """Get a runtime extension.

        Args:
            name: Extension name

        Returns:
            Extension or None
        """
        return self._extensions.get(name)

    async def is_running(self) -> bool:
        """Check if runtime is running.

        Returns:
            True if running
        """
        return self._status == RuntimeStatus.RUNNING

    async def pause(self) -> None:
        """Pause the runtime."""
        if self._status != RuntimeStatus.RUNNING:
            raise RuntimeError(f"Cannot pause from status: {self._status}")

        if self._scheduler:
            await self._scheduler.pause()

        self._status = RuntimeStatus.PAUSED

    async def resume(self) -> None:
        """Resume the runtime."""
        if self._status != RuntimeStatus.PAUSED:
            raise RuntimeError(f"Cannot resume from status: {self._status}")

        if self._scheduler:
            await self._scheduler.resume()

        self._status = RuntimeStatus.RUNNING


# Module-level singleton instance
_runtime: RuntimeLifecycle | None = None


def get_runtime_lifecycle() -> RuntimeLifecycle:
    """Get the global runtime lifecycle instance.

    Returns:
        RuntimeLifecycle instance
    """
    global _runtime
    if _runtime is None:
        _runtime = RuntimeLifecycle()
    return _runtime


# Re-export interface for type hints
IRuntimeLifecycle = RuntimeLifecycle
