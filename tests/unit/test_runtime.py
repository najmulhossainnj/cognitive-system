"""Unit tests for runtime components."""

from __future__ import annotations

import pytest


class TestServiceRegistry:
    """Tests for ServiceRegistry."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry."""
        from cos.runtime import ServiceRegistry
        return ServiceRegistry()

    @pytest.mark.asyncio
    async def test_register_service(self, registry):
        """Test registering a service."""
        service = object()
        await registry.register("test-service", "test-capability", service)
        assert await registry.lookup("test-service") is service

    @pytest.mark.asyncio
    async def test_unregister_service(self, registry):
        """Test unregistering a service."""
        service = object()
        await registry.register("test-service", "test-capability", service)
        result = await registry.unregister("test-service")
        assert result is True
        assert await registry.lookup("test-service") is None

    @pytest.mark.asyncio
    async def test_discover_capability(self, registry):
        """Test discovering services by capability."""
        await registry.register("service-1", "reasoning", object())
        await registry.register("service-2", "reasoning", object())
        await registry.register("service-3", "memory", object())

        reasoning_services = await registry.discover("reasoning")
        assert len(reasoning_services) == 2
        assert "service-1" in reasoning_services
        assert "service-2" in reasoning_services

        memory_services = await registry.discover("memory")
        assert len(memory_services) == 1
        assert "service-3" in memory_services

    @pytest.mark.asyncio
    async def test_service_metadata(self, registry):
        """Test getting service metadata."""
        await registry.register(
            "test-service",
            "test-capability",
            object(),
            interfaces=["IInterface1"],
            version="2.0.0",
        )
        metadata = await registry.metadata("test-service")
        assert metadata["service_id"] == "test-service"
        assert metadata["capability"] == "test-capability"
        assert metadata["version"] == "2.0.0"
        assert "IInterface1" in metadata["interfaces"]

    @pytest.mark.asyncio
    async def test_health_status(self, registry):
        """Test health status tracking."""
        await registry.register("test-service", "test-capability", object())
        assert await registry.health("test-service") == "registered"

        await registry.set_health("test-service", "healthy")
        assert await registry.health("test-service") == "healthy"


class TestDependencyInjection:
    """Tests for DependencyInjection."""

    @pytest.fixture
    def di(self):
        """Create a fresh DI container."""
        from cos.runtime import DependencyInjection
        return DependencyInjection()

    @pytest.mark.asyncio
    async def test_bind_interface(self, di):
        """Test binding an interface."""
        impl = object()
        await di.bind("ITest", impl)
        resolved = await di.resolve("ITest")
        assert resolved is impl

    @pytest.mark.asyncio
    async def test_singleton_lifetime(self, di):
        """Test singleton lifetime."""
        class Singleton:
            instance_count = 0

            def __init__(self):
                Singleton.instance_count += 1

        await di.bind("ITest", Singleton)
        await di.resolve("ITest")
        await di.resolve("ITest")
        assert Singleton.instance_count == 1

    @pytest.mark.asyncio
    async def test_transient_lifetime(self, di):
        """Test transient lifetime."""
        call_count = 0

        def factory():
            nonlocal call_count
            call_count += 1
            return object()

        await di.bind("ITest", factory, lifetime="transient")
        await di.resolve("ITest")
        await di.resolve("ITest")
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_replace_binding(self, di):
        """Test replacing a binding."""
        impl1 = object()
        impl2 = object()
        await di.bind("ITest", impl1)
        await di.replace("ITest", impl2)
        resolved = await di.resolve("ITest")
        assert resolved is impl2


class TestEventBus:
    """Tests for EventBus."""

    @pytest.fixture
    def bus(self):
        """Create a fresh event bus."""
        from cos.runtime import EventBus
        return EventBus()

    @pytest.mark.asyncio
    async def test_publish_event(self, bus):
        """Test publishing an event."""
        from cos.runtime import Event
        event = Event(type="test", payload={"data": "value"})
        event_id = await bus.publish(event)
        assert event_id is not None

    @pytest.mark.asyncio
    async def test_subscribe_and_receive(self, bus):
        """Test subscribing and receiving events."""
        from cos.runtime import Event
        received = []

        def handler(event):
            received.append(event)

        bus.subscribe("test", handler)
        await bus.publish(Event(type="test", payload={"data": "value"}))

        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_unsubscribe(self, bus):
        """Test unsubscribing."""
        def handler(event):
            pass

        sub_id = bus.subscribe("test", handler)
        bus.unsubscribe(sub_id)
        assert len(bus.get_subscriptions("test")) == 0

    @pytest.mark.asyncio
    async def test_event_replay(self, bus):
        """Test event replay."""
        from cos.runtime import Event
        bus.subscribe("test", lambda e: None)
        await bus.publish(Event(type="test", payload={"id": 1}))
        await bus.publish(Event(type="test", payload={"id": 2}))

        events = bus.replay("test")
        assert len(events) == 2


class TestScheduler:
    """Tests for Scheduler."""

    @pytest.fixture
    def scheduler(self):
        """Create a fresh scheduler."""
        from cos.runtime import Scheduler
        return Scheduler()

    @pytest.mark.asyncio
    async def test_schedule_task(self, scheduler):
        """Test scheduling a task."""
        async def task():
            return 42

        task_id = await scheduler.schedule(task(), priority=1)
        assert task_id is not None

    @pytest.mark.asyncio
    async def test_priority_ordering(self, scheduler):
        """Test tasks are ordered by priority."""
        results = []

        async def low():
            results.append("low")

        async def high():
            results.append("high")

        await scheduler.schedule(low(), priority=1)
        await scheduler.schedule(high(), priority=10)

        await asyncio.sleep(0.1)

        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_cancel_task(self, scheduler):
        """Test cancelling a task."""
        # Create a long-running task
        task_started = asyncio.Event()
        task_can_continue = asyncio.Event()

        async def long_task():
            task_started.set()
            await task_can_continue.wait()
            return "done"

        task_id = await scheduler.schedule(long_task(), priority=1)

        # Wait for task to start
        await task_started.wait()

        # Now cancel
        result = await scheduler.cancel(task_id)
        assert result is True

        # Clean up
        task_can_continue.set()


class TestConfigurationManager:
    """Tests for ConfigurationManager."""

    @pytest.fixture
    def config(self):
        """Create a fresh config manager."""
        from cos.runtime import ConfigurationManager
        return ConfigurationManager()

    def test_get_set(self, config):
        """Test getting and setting values."""
        config.set("key", "value")
        assert config.get("key") == "value"

    def test_nested_keys(self, config):
        """Test nested key access."""
        config.set("parent.child.grandchild", "value")
        assert config.get("parent.child.grandchild") == "value"

    def test_default_value(self, config):
        """Test default value for missing keys."""
        assert config.get("missing", "default") == "default"

    def test_has_key(self, config):
        """Test checking key existence."""
        config.set("key", "value")
        assert config.has_key("key") is True
        assert config.has_key("missing") is False

    def test_load_dict(self, config):
        """Test loading from dictionary."""
        config.load_dict({"key1": "value1", "nested": {"key2": "value2"}})
        assert config.get("key1") == "value1"
        assert config.get("nested.key2") == "value2"


class TestRuntimeLifecycle:
    """Tests for RuntimeLifecycle."""

    @pytest.fixture
    def runtime(self):
        """Create a fresh runtime."""
        from cos.runtime import RuntimeLifecycle
        return RuntimeLifecycle()

    @pytest.mark.asyncio
    async def test_initialize(self, runtime):
        """Test initializing the runtime."""
        await runtime.initialize()
        status = await runtime.get_status()
        assert status["status"] == "initialized"

    @pytest.mark.asyncio
    async def test_start_stop(self, runtime):
        """Test starting and stopping the runtime."""
        await runtime.initialize()
        await runtime.start()
        assert await runtime.is_running() is True

        await runtime.stop()
        status = await runtime.get_status()
        assert status["status"] == "stopping"

    @pytest.mark.asyncio
    async def test_shutdown(self, runtime):
        """Test full shutdown."""
        await runtime.initialize()
        await runtime.start()
        await runtime.shutdown()
        status = await runtime.get_status()
        assert status["status"] == "stopped"

    @pytest.mark.asyncio
    async def test_get_components(self, runtime):
        """Test getting runtime components."""
        await runtime.initialize()
        registry = await runtime.get_registry()
        assert registry is not None
        di = await runtime.get_di()
        assert di is not None


# Import asyncio for tests
import asyncio
