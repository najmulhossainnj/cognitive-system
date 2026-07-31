"""Service Registry Implementation.

This module provides the Service Registry for centralized service registration
and discovery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ServiceMetadata:
    """Service metadata container."""

    service_id: str
    capability: str
    interfaces: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    health: str = "unknown"
    registered_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class ServiceRegistry:
    """Service Registry provides centralized registration and discovery.

    The Service Registry is responsible for:
    - Registering runtime services
    - Maintaining capability mappings
    - Supporting service discovery
    - Monitoring health

    See RUNTIME-001 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the service registry."""
        self._services: dict[str, Any] = {}
        self._metadata: dict[str, ServiceMetadata] = {}
        self._capability_index: dict[str, list[str]] = {}

    async def register(
        self,
        service_id: str,
        capability: str,
        implementation: Any,
        interfaces: list[str] | None = None,
        version: str = "1.0.0",
    ) -> None:
        """Register a service.

        Args:
            service_id: Unique service identifier
            capability: Capability provided by the service
            implementation: Service implementation
            interfaces: List of implemented interfaces
            version: Service version
        """
        self._services[service_id] = implementation
        self._metadata[service_id] = ServiceMetadata(
            service_id=service_id,
            capability=capability,
            interfaces=interfaces or [],
            version=version,
            health="registered",
        )

        if capability not in self._capability_index:
            self._capability_index[capability] = []
        self._capability_index[capability].append(service_id)

    async def unregister(self, service_id: str) -> bool:
        """Unregister a service.

        Args:
            service_id: Service to unregister

        Returns:
            True if unregistered
        """
        if service_id not in self._services:
            return False

        metadata = self._metadata.get(service_id)
        if metadata:
            capability = metadata.capability
            if capability in self._capability_index:
                self._capability_index[capability].remove(service_id)

        del self._services[service_id]
        del self._metadata[service_id]
        return True

    async def discover(self, capability: str) -> list[str]:
        """Discover services providing a capability.

        Args:
            capability: Capability to discover

        Returns:
            List of service IDs
        """
        return self._capability_index.get(capability, []).copy()

    async def lookup(self, service_id: str) -> Any | None:
        """Look up a service by ID.

        Args:
            service_id: Service to look up

        Returns:
            Service implementation or None
        """
        return self._services.get(service_id)

    async def interfaces(self, service_id: str) -> list[str]:
        """Get interfaces for a service.

        Args:
            service_id: Service ID

        Returns:
            List of interface names
        """
        metadata = self._metadata.get(service_id)
        return metadata.interfaces.copy() if metadata else []

    async def capabilities(self, service_id: str) -> list[str]:
        """Get capabilities for a service.

        Args:
            service_id: Service ID

        Returns:
            List of capabilities
        """
        metadata = self._metadata.get(service_id)
        return [metadata.capability] if metadata else []

    async def metadata(self, service_id: str) -> dict[str, Any]:
        """Get metadata for a service.

        Args:
            service_id: Service ID

        Returns:
            Service metadata
        """
        meta = self._metadata.get(service_id)
        if not meta:
            return {}
        return {
            "service_id": meta.service_id,
            "capability": meta.capability,
            "interfaces": meta.interfaces,
            "version": meta.version,
            "health": meta.health,
            "registered_at": meta.registered_at.isoformat(),
            "custom": meta.metadata,
        }

    async def health(self, service_id: str) -> str:
        """Get health status of a service.

        Args:
            service_id: Service ID

        Returns:
            Health status
        """
        metadata = self._metadata.get(service_id)
        return metadata.health if metadata else "unknown"

    async def set_health(self, service_id: str, health: str) -> None:
        """Set health status of a service.

        Args:
            service_id: Service ID
            health: Health status
        """
        metadata = self._metadata.get(service_id)
        if metadata:
            metadata.health = health

    async def status(self) -> dict[str, Any]:
        """Get registry status.

        Returns:
            Registry status
        """
        return {
            "total_services": len(self._services),
            "capabilities": list(self._capability_index.keys()),
            "services": [
                {"id": sid, "capability": m.capability, "health": m.health}
                for sid, m in self._metadata.items()
            ],
        }

    async def versions(self, service_id: str) -> dict[str, str]:
        """Get version information for a service.

        Args:
            service_id: Service ID

        Returns:
            Version information
        """
        metadata = self._metadata.get(service_id)
        if not metadata:
            return {}
        return {
            "service_version": metadata.version,
            "registered_at": metadata.registered_at.isoformat(),
        }


# Module-level singleton instance
_registry: ServiceRegistry | None = None


def get_service_registry() -> ServiceRegistry:
    """Get the global service registry instance.

    Returns:
        ServiceRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = ServiceRegistry()
    return _registry


# Re-export interface for type hints
IServiceRegistry = ServiceRegistry
