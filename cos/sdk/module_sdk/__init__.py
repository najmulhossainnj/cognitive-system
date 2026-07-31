"""Module SDK for creating cognitive modules."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ModuleSDK:
    """SDK for creating cognitive modules.

    Provides a framework for building reusable cognitive modules that
    can be integrated into the cognitive system.
    """

    def __init__(self, context: Any) -> None:
        """Initialize the module SDK.

        Args:
            context: The cognitive context
        """
        self._context = context
        self._name: str = "UnnamedModule"
        self._version: str = "0.0.0"

    def define(self, name: str, version: str = "0.0.0") -> "ModuleSDK":
        """Define the module metadata.

        Args:
            name: Module name
            version: Module version

        Returns:
            Self for chaining
        """
        self._name = name
        self._version = version
        return self

    @property
    def name(self) -> str:
        """Get the module name."""
        return self._name

    @property
    def version(self) -> str:
        """Get the module version."""
        return self._version

    async def on_initialize(self) -> None:
        """Called when the module is initialized."""
        pass

    async def on_start(self) -> None:
        """Called when the module starts."""
        pass

    async def on_stop(self) -> None:
        """Called when the module stops."""
        pass

    async def process(self, input_data: Any) -> Any:
        """Process input data.

        Args:
            input_data: Input to process

        Returns:
            Processing result
        """
        return input_data


__all__ = ["ModuleSDK"]
