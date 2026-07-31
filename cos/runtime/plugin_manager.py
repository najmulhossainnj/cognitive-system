"""Plugin Manager Implementation.

This module provides the Plugin Manager for runtime plugin management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class PluginStatus(str, Enum):
    """Plugin status values."""

    LOADED = "loaded"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"


@dataclass
class Plugin:
    """Represents a plugin."""

    id: str
    name: str
    path: str
    instance: Any | None = None
    status: PluginStatus = PluginStatus.LOADED
    loaded_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class PluginManager:
    """Plugin Manager manages runtime plugins.

    The Plugin Manager is responsible for:
    - Loading plugins
    - Managing plugin lifecycle
    - Unloading plugins

    See RUNTIME-008 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the plugin manager."""
        self._plugins: dict[str, Plugin] = {}
        self._loaders: dict[str, Any] = {}

    def register_loader(self, extension: str, loader: Any) -> None:
        """Register a plugin loader for a file extension.

        Args:
            extension: File extension (e.g., ".py")
            loader: Loader function
        """
        self._loaders[extension] = loader

    async def load_plugin(self, plugin_path: str) -> str:
        """Load a plugin.

        Args:
            plugin_path: Path to plugin

        Returns:
            Plugin ID
        """
        import importlib.util
        import sys

        plugin_id = str(uuid4())
        plugin_name = plugin_path.split("/")[-1].split("\\")[-1]

        if plugin_name.endswith(".py"):
            plugin_name = plugin_name[:-3]

        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[plugin_name] = module
                spec.loader.exec_module(module)

                instance = getattr(module, "create_plugin", lambda: None)()

                plugin = Plugin(
                    id=plugin_id,
                    name=plugin_name,
                    path=plugin_path,
                    instance=instance,
                    status=PluginStatus.LOADED,
                )
                self._plugins[plugin_id] = plugin
                return plugin_id
            else:
                raise ValueError(f"Could not load plugin from {plugin_path}")

        except Exception as e:
            plugin = Plugin(
                id=plugin_id,
                name=plugin_name,
                path=plugin_path,
                status=PluginStatus.ERROR,
                error=str(e),
            )
            self._plugins[plugin_id] = plugin
            raise

    async def unload_plugin(self, plugin_id: str) -> bool:
        """Unload a plugin.

        Args:
            plugin_id: Plugin to unload

        Returns:
            True if unloaded
        """
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            return False

        if plugin.status == PluginStatus.ENABLED:
            await self.disable_plugin(plugin_id)

        del self._plugins[plugin_id]
        return True

    async def get_plugin(self, plugin_id: str) -> Any | None:
        """Get a plugin instance.

        Args:
            plugin_id: Plugin ID

        Returns:
            Plugin instance or None
        """
        plugin = self._plugins.get(plugin_id)
        return plugin.instance if plugin else None

    async def list_plugins(self) -> list[dict[str, Any]]:
        """List loaded plugins.

        Returns:
            List of plugin information
        """
        return [
            {
                "id": p.id,
                "name": p.name,
                "status": p.status.value,
                "loaded_at": p.loaded_at.isoformat(),
                "error": p.error,
            }
            for p in self._plugins.values()
        ]

    async def enable_plugin(self, plugin_id: str) -> None:
        """Enable a plugin.

        Args:
            plugin_id: Plugin to enable
        """
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin not found: {plugin_id}")

        if plugin.status == PluginStatus.ERROR:
            raise RuntimeError(f"Cannot enable errored plugin: {plugin.error}")

        plugin.status = PluginStatus.ENABLED

        if plugin.instance and hasattr(plugin.instance, "on_enable"):
            enable_fn = plugin.instance.on_enable
            if callable(enable_fn):
                await enable_fn()

    async def disable_plugin(self, plugin_id: str) -> None:
        """Disable a plugin.

        Args:
            plugin_id: Plugin to disable
        """
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin not found: {plugin_id}")

        if plugin.instance and hasattr(plugin.instance, "on_disable"):
            disable_fn = plugin.instance.on_disable
            if callable(disable_fn):
                await disable_fn()

        plugin.status = PluginStatus.DISABLED

    async def get_plugin_status(self, plugin_id: str) -> str:
        """Get plugin status.

        Args:
            plugin_id: Plugin ID

        Returns:
            Plugin status
        """
        plugin = self._plugins.get(plugin_id)
        return plugin.status.value if plugin else "not_found"


# Module-level singleton instance
_plugin_manager: PluginManager | None = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance.

    Returns:
        PluginManager instance
    """
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


# Re-export interface for type hints
IPluginManager = PluginManager
