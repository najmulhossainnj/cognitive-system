"""Dependency Injection Implementation.

This module provides the Dependency Injection subsystem for implementation-independent
dependency resolution.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class Lifetime(str, Enum):
    """Service lifetime strategies."""

    SINGLETON = "singleton"
    SCOPED = "scoped"
    TRANSIENT = "transient"


@dataclass
class Binding:
    """Represents a dependency binding."""

    interface: str
    implementation: Any
    lifetime: Lifetime = Lifetime.SINGLETON
    instance: Any | None = None


class DependencyInjection:
    """Dependency Injection provides implementation-independent dependency resolution.

    The DI subsystem is responsible for:
    - Resolving published interfaces
    - Injecting service dependencies
    - Managing service lifetimes
    - Validating dependency graphs

    See RUNTIME-002 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the dependency injection container."""
        self._bindings: dict[str, Binding] = {}
        self._scopes: dict[str, dict[str, Any]] = {}
        self._current_scope: str | None = None
        self._factories: dict[str, Callable[[], Any]] = {}

    def _get_instance(self, binding: Binding) -> Any:
        """Get or create an instance based on lifetime."""
        if binding.lifetime == Lifetime.SINGLETON:
            if binding.instance is None:
                binding.instance = self._create_instance(binding)
            return binding.instance

        if binding.lifetime == Lifetime.SCOPED:
            if self._current_scope and self._current_scope in self._scopes:
                scope_instances = self._scopes[self._current_scope]
                if binding.interface not in scope_instances:
                    scope_instances[binding.interface] = self._create_instance(binding)
                return scope_instances[binding.interface]

            if binding.instance is None:
                binding.instance = self._create_instance(binding)
            return binding.instance

        return self._create_instance(binding)

    def _create_instance(self, binding: Binding) -> Any:
        """Create a new instance."""
        impl = binding.implementation
        if callable(impl) and not isinstance(impl, type):
            return impl()
        if isinstance(impl, type):
            return impl()
        return impl

    async def bind(
        self,
        interface: str,
        implementation: Any,
        lifetime: str = "singleton",
    ) -> None:
        """Bind an interface to an implementation.

        Args:
            interface: Interface to bind
            implementation: Implementation class or instance
            lifetime: Lifetime strategy (singleton, scoped, transient)
        """
        lifetime_enum = Lifetime(lifetime.lower())
        self._bindings[interface] = Binding(
            interface=interface,
            implementation=implementation,
            lifetime=lifetime_enum,
        )

    async def unbind(self, interface: str) -> bool:
        """Unbind an interface.

        Args:
            interface: Interface to unbind

        Returns:
            True if unbound
        """
        if interface in self._bindings:
            del self._bindings[interface]
            return True
        return False

    async def resolve(self, interface: str) -> Any:
        """Resolve an interface to an implementation.

        Args:
            interface: Interface to resolve

        Returns:
            Resolved implementation
        """
        binding = self._bindings.get(interface)
        if not binding:
            raise ValueError(f"No binding found for interface: {interface}")
        return self._get_instance(binding)

    async def inject(self, target: Any) -> None:
        """Inject dependencies into a target.

        Args:
            target: Target object to inject into
        """
        if not hasattr(target, "__init__"):
            return

        annotations = getattr(target, "__annotations__", {})
        for attr_name, attr_type in annotations.items():
            if attr_name.startswith("_"):
                continue

            type_str = self._get_type_string(attr_type)
            if type_str in self._bindings:
                instance = await self.resolve(type_str)
                setattr(target, attr_name, instance)

    def _get_type_string(self, attr_type: Any) -> str:
        """Get string representation of type."""
        if isinstance(attr_type, str):
            return attr_type
        if hasattr(attr_type, "__name__"):
            return attr_type.__name__
        if hasattr(attr_type, "__origin__"):
            origin = getattr(attr_type, "__origin__")
            if hasattr(origin, "__name__"):
                return origin.__name__
        return str(attr_type)

    async def factory(self, interface: str) -> Callable[[], Any]:
        """Create a factory for an interface.

        Args:
            interface: Interface for factory

        Returns:
            Factory function
        """
        async def create() -> Any:
            binding = self._bindings.get(interface)
            if not binding:
                raise ValueError(f"No binding found for interface: {interface}")
            return self._create_instance(binding)

        self._factories[interface] = create
        return create

    async def scope(self, scope_name: str) -> Scope:
        """Create or get a scope.

        Args:
            scope_name: Name of the scope

        Returns:
            Scope object
        """
        if scope_name not in self._scopes:
            self._scopes[scope_name] = {}
        return Scope(self, scope_name)

    async def create(self, interface: str) -> Any:
        """Create a new instance.

        Args:
            interface: Interface to create

        Returns:
            New instance (always transient)
        """
        binding = self._bindings.get(interface)
        if not binding:
            raise ValueError(f"No binding found for interface: {interface}")
        return self._create_instance(binding)

    async def validate(self) -> list[str]:
        """Validate dependency graph.

        Returns:
            List of validation errors
        """
        errors = []

        for interface, binding in self._bindings.items():
            if binding.lifetime == Lifetime.SCOPED:
                if self._current_scope is None:
                    errors.append(
                        f"Scoped binding '{interface}' requires active scope"
                    )

        if self._check_circular_dependencies():
            errors.append("Circular dependency detected")

        return errors

    def _check_circular_dependencies(self) -> bool:
        """Check for circular dependencies."""
        visited: set[str] = set()
        path: set[str] = set()

        def visit(interface: str) -> bool:
            if interface in path:
                return True
            if interface in visited:
                return False

            path.add(interface)
            binding = self._bindings.get(interface)
            if binding and isinstance(binding.implementation, type):
                for base in getattr(binding.implementation, "__bases__", []):
                    if visit(base.__name__):
                        return True

            path.remove(interface)
            visited.add(interface)
            return False

        for interface in self._bindings:
            if visit(interface):
                return True

        return False

    async def replace(
        self,
        interface: str,
        implementation: Any,
    ) -> None:
        """Replace an implementation.

        Args:
            interface: Interface to replace
            implementation: New implementation
        """
        binding = self._bindings.get(interface)
        if binding:
            binding.implementation = implementation
            binding.instance = None
        else:
            await self.bind(interface, implementation)

    async def status(self) -> dict[str, Any]:
        """Get DI status.

        Returns:
            Status information
        """
        return {
            "total_bindings": len(self._bindings),
            "active_scope": self._current_scope,
            "scopes": list(self._scopes.keys()),
            "bindings": {
                interface: {
                    "lifetime": binding.lifetime.value,
                    "has_instance": binding.instance is not None,
                }
                for interface, binding in self._bindings.items()
            },
        }


class Scope:
    """Represents a dependency injection scope."""

    def __init__(self, di: DependencyInjection, name: str) -> None:
        """Initialize the scope.

        Args:
            di: Parent DI container
            name: Scope name
        """
        self._di = di
        self._name = name
        self._previous_scope: str | None = None

    async def __aenter__(self) -> Scope:
        """Enter the scope."""
        self._previous_scope = self._di._current_scope
        self._di._current_scope = self._name
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the scope."""
        self._di._current_scope = self._previous_scope


# Module-level singleton instance
_di: DependencyInjection | None = None


def get_dependency_injection() -> DependencyInjection:
    """Get the global dependency injection instance.

    Returns:
        DependencyInjection instance
    """
    global _di
    if _di is None:
        _di = DependencyInjection()
    return _di


# Re-export interface for type hints
IDependencyInjection = DependencyInjection
