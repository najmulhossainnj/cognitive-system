"""Kernel Memory - Low-level memory management for COS."""

from __future__ import annotations


class IKernelMemory:
    """Kernel-level memory management.

    This is the low-level memory interface used by the kernel.
    The cognitive layer uses higher-level memory services.
    """

    async def allocate(self, size: int) -> bytes:
        """Allocate memory.

        Args:
            size: Size in bytes

        Returns:
            Allocated memory buffer
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    async def deallocate(self, buffer: bytes) -> None:
        """Deallocate memory.

        Args:
            buffer: Memory buffer to deallocate
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def get_stats(self) -> dict[str, int]:
        """Get memory statistics.

        Returns:
            Dictionary of memory statistics
        """
        raise NotImplementedError("Will be implemented in Phase 2")
