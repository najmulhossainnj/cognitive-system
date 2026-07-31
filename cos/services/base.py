"""Base Service Implementation.

This module provides the base service class for all COS services.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any


class ServiceStatus(str, Enum):
    """Service status values."""

    CREATED = "created"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    RESUMING = "resuming"
    STOPPING = "stopping"
    STOPPED = "stopped"
    DISPOSING = "disposing"
    DISPOSED = "disposed"
    ERROR = "error"


class ServiceBase:
    """Base class for all COS services.

    All services must inherit from this class and implement the
    required lifecycle methods.
    """

    def __init__(self, service_id: str | None = None) -> None:
        """Initialize the service.

        Args:
            service_id: Optional service identifier
        """
        self._service_id = service_id or self.__class__.__name__
        self._status = ServiceStatus.CREATED
        self._capabilities: list[str] = []
        self._metadata: dict[str, Any] = {}
        self._initialized_at: datetime | None = None
        self._started_at: datetime | None = None
        self._error: str | None = None

    async def initialize(self) -> None:
        """Initialize the service."""
        self._status = ServiceStatus.INITIALIZING
        try:
            await self._on_initialize()
            self._status = ServiceStatus.INITIALIZED
            self._initialized_at = datetime.now()
        except Exception as e:
            self._status = ServiceStatus.ERROR
            self._error = str(e)
            raise

    async def start(self) -> None:
        """Start the service."""
        if self._status != ServiceStatus.INITIALIZED:
            raise RuntimeError(f"Cannot start from status: {self._status}")
        self._status = ServiceStatus.STARTING
        try:
            await self._on_start()
            self._status = ServiceStatus.RUNNING
            self._started_at = datetime.now()
        except Exception as e:
            self._status = ServiceStatus.ERROR
            self._error = str(e)
            raise

    async def stop(self) -> None:
        """Stop the service."""
        self._status = ServiceStatus.STOPPING
        try:
            await self._on_stop()
            self._status = ServiceStatus.STOPPED
        except Exception as e:
            self._status = ServiceStatus.ERROR
            self._error = str(e)
            raise

    async def pause(self) -> None:
        """Pause the service."""
        if self._status != ServiceStatus.RUNNING:
            raise RuntimeError(f"Cannot pause from status: {self._status}")
        self._status = ServiceStatus.PAUSING
        try:
            await self._on_pause()
            self._status = ServiceStatus.PAUSED
        except Exception as e:
            self._status = ServiceStatus.ERROR
            self._error = str(e)
            raise

    async def resume(self) -> None:
        """Resume the service."""
        if self._status != ServiceStatus.PAUSED:
            raise RuntimeError(f"Cannot resume from status: {self._status}")
        self._status = ServiceStatus.RESUMING
        try:
            await self._on_resume()
            self._status = ServiceStatus.RUNNING
        except Exception as e:
            self._status = ServiceStatus.ERROR
            self._error = str(e)
            raise

    async def dispose(self) -> None:
        """Dispose the service."""
        self._status = ServiceStatus.DISPOSING
        try:
            await self._on_dispose()
            self._status = ServiceStatus.DISPOSED
        except Exception as e:
            self._status = ServiceStatus.ERROR
            self._error = str(e)
            raise

    async def health_check(self) -> dict[str, Any]:
        """Check service health.

        Returns:
            Health status
        """
        return {
            "service_id": self._service_id,
            "status": self._status.value,
            "healthy": self._status in (ServiceStatus.RUNNING, ServiceStatus.PAUSED),
            "uptime_seconds": (
                (datetime.now() - self._started_at).total_seconds()
                if self._started_at
                else None
            ),
            "error": self._error,
        }

    async def get_status(self) -> str:
        """Get service status.

        Returns:
            Current status
        """
        return self._status.value

    def get_capabilities(self) -> list[str]:
        """Get service capabilities.

        Returns:
            List of capabilities
        """
        return self._capabilities.copy()

    def get_metadata(self) -> dict[str, Any]:
        """Get service metadata.

        Returns:
            Service metadata
        """
        return {
            "service_id": self._service_id,
            "class": self.__class__.__name__,
            "capabilities": self._capabilities,
            **self._metadata,
        }

    def _add_capability(self, capability: str) -> None:
        """Add a capability.

        Args:
            capability: Capability to add
        """
        if capability not in self._capabilities:
            self._capabilities.append(capability)

    def _set_metadata(self, key: str, value: Any) -> None:
        """Set metadata.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self._metadata[key] = value

    async def _on_initialize(self) -> None:
        """Override to implement initialization logic."""
        pass

    async def _on_start(self) -> None:
        """Override to implement start logic."""
        pass

    async def _on_stop(self) -> None:
        """Override to implement stop logic."""
        pass

    async def _on_pause(self) -> None:
        """Override to implement pause logic."""
        pass

    async def _on_resume(self) -> None:
        """Override to implement resume logic."""
        pass

    async def _on_dispose(self) -> None:
        """Override to implement dispose logic."""
        pass


# Re-export interface for type hints
IService = ServiceBase
