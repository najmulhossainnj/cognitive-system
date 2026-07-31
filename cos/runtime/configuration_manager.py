"""Configuration Manager Implementation.

This module provides the Configuration Manager for system configuration.
"""

from __future__ import annotations

import json
import os
from typing import Any


class ConfigurationManager:
    """Configuration Manager manages system configuration.

    The Configuration Manager is responsible for:
    - Loading configuration
    - Providing type-safe access
    - Managing updates

    See RUNTIME-009 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the configuration manager."""
        self._config: dict[str, Any] = {}
        self._defaults: dict[str, Any] = {}
        self._validation_rules: dict[str, list[type]] = {}
        self._readonly_keys: set[str] = set()

    def _get_nested(self, key: str) -> tuple[dict[str, Any], str]:
        """Get the parent dict and key for a nested key.

        Args:
            key: Dot-separated key

        Returns:
            Tuple of (parent_dict, final_key)
        """
        parts = key.split(".")
        if len(parts) == 1:
            return self._config, key

        current = self._config
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        return current, parts[-1]

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            default: Default value

        Returns:
            Configuration value
        """
        try:
            parent, final_key = self._get_nested(key)
            return parent.get(final_key, default)
        except (AttributeError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        if key in self._readonly_keys:
            raise PermissionError(f"Cannot modify readonly key: {key}")

        if key in self._validation_rules:
            expected_types = self._validation_rules[key]
            if not any(isinstance(value, t) for t in expected_types):
                raise TypeError(
                    f"Invalid type for {key}: expected {expected_types}, got {type(value)}"
                )

        parent, final_key = self._get_nested(key)
        parent[final_key] = value

    def get_section(self, section: str) -> dict[str, Any]:
        """Get a configuration section.

        Args:
            section: Section name

        Returns:
            Section configuration
        """
        section_data = self._config.get(section, {})
        if isinstance(section_data, dict):
            return section_data.copy()
        return {}

    def validate(self) -> list[str]:
        """Validate configuration.

        Returns:
            List of validation errors
        """
        errors = []

        for key, expected_types in self._validation_rules.items():
            value = self.get(key)
            if value is None:
                continue

            if not any(isinstance(value, t) for t in expected_types):
                errors.append(
                    f"Invalid type for {key}: expected {expected_types}, got {type(value)}"
                )

        return errors

    def reload(self) -> None:
        """Reload configuration from sources."""
        env_prefix = "COS_"
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower().replace("_", ".")
                try:
                    parsed = json.loads(value)
                    self.set(config_key, parsed)
                except json.JSONDecodeError:
                    self.set(config_key, value)

    def save(self) -> None:
        """Save configuration (no-op for in-memory config)."""
        pass

    def get_all(self) -> dict[str, Any]:
        """Get all configuration.

        Returns:
            Full configuration
        """
        return self._config.copy()

    def has_key(self, key: str) -> bool:
        """Check if key exists.

        Args:
            key: Configuration key

        Returns:
            True if exists
        """
        parent, final_key = self._get_nested(key)
        return final_key in parent

    def set_default(self, key: str, value: Any) -> None:
        """Set a default value for a key.

        Args:
            key: Configuration key
            value: Default value
        """
        self._defaults[key] = value
        if not self.has_key(key):
            self.set(key, value)

    def set_validation(self, key: str, types: list[type]) -> None:
        """Set validation rules for a key.

        Args:
            key: Configuration key
            types: Allowed types
        """
        self._validation_rules[key] = types

    def set_readonly(self, key: str) -> None:
        """Mark a key as readonly.

        Args:
            key: Configuration key
        """
        self._readonly_keys.add(key)

    def load_dict(self, config: dict[str, Any], prefix: str = "") -> None:
        """Load configuration from a dictionary.

        Args:
            config: Configuration dictionary
            prefix: Key prefix for nested values
        """
        for key, value in config.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                self.load_dict(value, full_key)
            else:
                self.set(full_key, value)

    def load_json(self, json_str: str) -> None:
        """Load configuration from JSON string.

        Args:
            json_str: JSON configuration string
        """
        config = json.loads(json_str)
        if isinstance(config, dict):
            self.load_dict(config)

    def to_json(self) -> str:
        """Export configuration as JSON.

        Returns:
            JSON string
        """
        return json.dumps(self._config, indent=2)


# Module-level singleton instance
_config_manager: ConfigurationManager | None = None


def get_configuration_manager() -> ConfigurationManager:
    """Get the global configuration manager instance.

    Returns:
        ConfigurationManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    return _config_manager


# Re-export interface for type hints
IConfigurationManager = ConfigurationManager
