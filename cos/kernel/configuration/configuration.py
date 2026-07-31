"""Configuration - Configuration management for COS."""

from __future__ import annotations

from typing import Any


class IConfiguration:
    """Configuration manager for accessing and updating system settings.

    The configuration manager is responsible for:
    - Loading configuration from various sources
    - Providing type-safe configuration access
    - Managing configuration updates
    - Supporting configuration validation
    """

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (dot-separated for nested values)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def validate(self) -> list[str]:
        """Validate the current configuration.

        Returns:
            List of validation errors (empty if valid)
        """
        raise NotImplementedError("Will be implemented in Phase 2")

    def reload(self) -> None:
        """Reload configuration from sources."""
        raise NotImplementedError("Will be implemented in Phase 2")
