"""Plugin SDK for creating cognitive plugins."""

from __future__ import annotations

from typing import Any


class PluginSDK:
    """SDK for creating cognitive plugins.

    Provides a framework for building plugins that extend the
    cognitive system's capabilities.
    """

    def __init__(self, name: str) -> None:
        """Initialize the plugin SDK.

        Args:
            name: Plugin name
        """
        self._name = name
        self._enabled = True
        self._dependencies: list[str] = []

    @property
    def name(self) -> str:
        """Get the plugin name."""
        return self._name

    @property
    def enabled(self) -> bool:
        """Check if the plugin is enabled."""
        return self._enabled

    def add_dependency(self, plugin_name: str) -> None:
        """Add a dependency.

        Args:
            plugin_name: Name of the dependency
        """
        if plugin_name not in self._dependencies:
            self._dependencies.append(plugin_name)

    async def on_load(self) -> None:
        """Called when the plugin is loaded."""
        pass

    async def on_enable(self) -> None:
        """Called when the plugin is enabled."""
        self._enabled = True

    async def on_disable(self) -> None:
        """Called when the plugin is disabled."""
        self._enabled = False

    async def on_unload(self) -> None:
        """Called when the plugin is unloaded."""
        pass


def create_plugin(name: str) -> PluginSDK:
    """Create a new plugin.

    Args:
        name: Plugin name

    Returns:
        Plugin instance
    """
    return PluginSDK(name)


__all__ = ["PluginSDK", "create_plugin"]
