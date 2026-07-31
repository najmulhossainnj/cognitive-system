"""Testing SDK for cognitive system testing utilities."""

from __future__ import annotations

from typing import Any
import asyncio


class MockContext:
    """Mock cognitive context for testing."""

    def __init__(self) -> None:
        """Initialize mock context."""
        self._data: dict[str, Any] = {}

    async def set_data(self, key: str, value: Any) -> None:
        """Set context data."""
        self._data[key] = value

    async def get_data(self, key: str) -> Any | None:
        """Get context data."""
        return self._data.get(key)


class TestRunner:
    """Test runner for cognitive system tests."""

    def __init__(self) -> None:
        """Initialize test runner."""
        self._tests_passed = 0
        self._tests_failed = 0

    def assert_equal(self, actual: Any, expected: Any, message: str = "") -> None:
        """Assert two values are equal.

        Args:
            actual: Actual value
            expected: Expected value
            message: Optional message
        """
        if actual != expected:
            self._tests_failed += 1
            raise AssertionError(f"{message}: {actual} != {expected}")
        self._tests_passed += 1

    def assert_true(self, value: Any, message: str = "") -> None:
        """Assert a value is true.

        Args:
            value: Value to check
            message: Optional message
        """
        if not value:
            self._tests_failed += 1
            raise AssertionError(f"{message}: expected truthy value")
        self._tests_passed += 1

    def get_summary(self) -> dict[str, int]:
        """Get test summary."""
        return {
            "passed": self._tests_passed,
            "failed": self._tests_failed,
        }


async def run_async_test(coro: Any) -> bool:
    """Run an async test.

    Args:
        coro: Async test coroutine

    Returns:
        True if test passed
    """
    try:
        await coro()
        return True
    except Exception:
        return False


__all__ = ["MockContext", "TestRunner", "run_async_test"]
