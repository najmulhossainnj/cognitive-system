"""Resource Manager Implementation.

This module provides the Resource Manager for system resource allocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ResourceLimit:
    """Represents a resource limit."""

    resource_type: str
    limit: int
    allocated: int = 0


@dataclass
class ResourceAllocation:
    """Represents a resource allocation."""

    id: str
    resource_type: str
    amount: int
    allocated_at: datetime = field(default_factory=datetime.now)
    released: bool = False


class ResourceManager:
    """Resource Manager manages system resources.

    The Resource Manager is responsible for:
    - Tracking resource usage
    - Allocating resources
    - Enforcing limits

    See RUNTIME-007 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the resource manager."""
        self._limits: dict[str, ResourceLimit] = {}
        self._allocations: dict[str, ResourceAllocation] = {}
        self._allocation_counter: int = 0

    async def allocate(self, resource_type: str, amount: int) -> bool:
        """Allocate resources.

        Args:
            resource_type: Type of resource
            amount: Amount to allocate

        Returns:
            True if allocated
        """
        limit = self._limits.get(resource_type)
        if limit:
            if limit.allocated + amount > limit.limit:
                return False

        allocation_id = f"alloc_{self._allocation_counter}"
        self._allocation_counter += 1

        allocation = ResourceAllocation(
            id=allocation_id,
            resource_type=resource_type,
            amount=amount,
        )
        self._allocations[allocation_id] = allocation

        if resource_type in self._limits:
            self._limits[resource_type].allocated += amount
        else:
            self._limits[resource_type] = ResourceLimit(
                resource_type=resource_type,
                limit=-1,
                allocated=amount,
            )

        return True

    async def release(self, resource_type: str, amount: int) -> None:
        """Release resources.

        Args:
            resource_type: Type of resource
            amount: Amount to release
        """
        for allocation in self._allocations.values():
            if allocation.resource_type == resource_type and not allocation.released:
                if allocation.amount <= amount:
                    amount -= allocation.amount
                    allocation.released = True
                    if resource_type in self._limits:
                        self._limits[resource_type].allocated -= allocation.amount
                else:
                    allocation.amount -= amount
                    if resource_type in self._limits:
                        self._limits[resource_type].allocated -= amount
                    break

        if amount > 0 and resource_type in self._limits:
            current = self._limits[resource_type].allocated
            self._limits[resource_type].allocated = max(0, current - amount)

    async def get_usage(self) -> dict[str, Any]:
        """Get resource usage.

        Returns:
            Resource usage information
        """
        return {
            resource_type: {
                "limit": limit.limit if limit.limit > 0 else "unlimited",
                "allocated": limit.allocated,
                "available": limit.limit - limit.allocated if limit.limit > 0 else "unlimited",
            }
            for resource_type, limit in self._limits.items()
        }

    async def get_available(self, resource_type: str) -> int:
        """Get available resources.

        Args:
            resource_type: Type of resource

        Returns:
            Available amount
        """
        limit = self._limits.get(resource_type)
        if not limit:
            return -1

        if limit.limit < 0:
            return -1

        return max(0, limit.limit - limit.allocated)

    async def set_limit(self, resource_type: str, limit: int) -> None:
        """Set resource limit.

        Args:
            resource_type: Type of resource
            limit: Limit to set
        """
        if resource_type in self._limits:
            self._limits[resource_type].limit = limit
        else:
            self._limits[resource_type] = ResourceLimit(
                resource_type=resource_type,
                limit=limit,
            )

    async def check_available(self, resource_type: str, amount: int) -> bool:
        """Check if resources are available.

        Args:
            resource_type: Type of resource
            amount: Amount needed

        Returns:
            True if available
        """
        available = await self.get_available(resource_type)
        if available < 0:
            return True
        return available >= amount

    def get_allocation(self, allocation_id: str) -> ResourceAllocation | None:
        """Get an allocation by ID.

        Args:
            allocation_id: Allocation ID

        Returns:
            Allocation or None
        """
        return self._allocations.get(allocation_id)

    def get_allocations_by_type(self, resource_type: str) -> list[ResourceAllocation]:
        """Get allocations by resource type.

        Args:
            resource_type: Resource type

        Returns:
            List of allocations
        """
        return [
            a for a in self._allocations.values()
            if a.resource_type == resource_type and not a.released
        ]


# Module-level singleton instance
_resource_manager: ResourceManager | None = None


def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance.

    Returns:
        ResourceManager instance
    """
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager


# Re-export interface for type hints
IResourceManager = ResourceManager
