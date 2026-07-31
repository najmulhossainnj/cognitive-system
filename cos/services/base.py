"""Base Service Interface.

This module defines the base interface for all services.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class IService:
    """Base interface for all COS services.

    All services must implement this interface and conform to the
    service lifecycle defined in SERVICE-001.
    """

    async def initialize(self) -> None:
        """Initialize the service."""
        raise NotImplementedError("Will be implemented in Phase 2")

    async def start(self) -> None:
        """Start the service."""
        raise NotImplementedError("Will be implemented in Phase 2")

    async def stop(self) -> None:
        """Stop the service."""
        raise NotImplementedError("Will be implemented in Phase 2")

    async def pause(self) -> None:
        """Pause the service."""
        raise NotImplementedError("Will be implemented in Phase 2")

    async def resume(self) -> None:
        """Resume the service."""
        raise NotImplementedError("Will be implemented in Phase 2")

    async def dispose(self) -> None:
        """Dispose the service."""
        raise NotImplementedError("Will be implemented in Phase 2")

    async def health_check(self) -> dict[str, Any]:
        """Check service health.

        Returns:
            Health status
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def get_status(self) -> str:
        """Get service status.

        Returns:
            Current status
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def get_capabilities(self) -> list[str]:
        """Get service capabilities.

        Returns:
            List of capabilities
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def get_metadata(self) -> dict[str, Any]:
        """Get service metadata.

        Returns:
            Service metadata
        """
        raise NotImplementedError("Will be implemented in Phase 2")
