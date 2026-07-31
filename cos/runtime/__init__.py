"""Runtime module for the Cognitive Operating System.

This module provides the runtime kernel infrastructure including:
- Service Registry
- Dependency Injection
- Event Bus
- Scheduler
- Configuration Manager
- Pipeline Engine
- Task Manager
- Resource Manager
- Plugin Manager
- Runtime Lifecycle
"""

from cos.runtime.service_registry import (
    ServiceRegistry,
    IServiceRegistry,
    ServiceMetadata,
    get_service_registry,
)
from cos.runtime.dependency_injection import (
    DependencyInjection,
    IDependencyInjection,
    Lifetime,
    Binding,
    Scope,
    get_dependency_injection,
)
from cos.runtime.event_bus import (
    EventBus,
    IEventBus,
    Event,
    Subscription,
    get_event_bus,
)
from cos.runtime.scheduler import (
    Scheduler,
    IScheduler,
    Task,
    TaskStatus,
    ScheduledTask,
    get_scheduler,
)
from cos.runtime.pipeline_engine import (
    PipelineEngine,
    IPipelineEngine,
    Pipeline,
    PipelineStatus,
    get_pipeline_engine,
)
from cos.runtime.task_manager import (
    TaskManager,
    ITaskManager,
    ManagedTask,
    TaskState,
    get_task_manager,
)
from cos.runtime.resource_manager import (
    ResourceManager,
    IResourceManager,
    ResourceLimit,
    ResourceAllocation,
    get_resource_manager,
)
from cos.runtime.plugin_manager import (
    PluginManager,
    IPluginManager,
    Plugin,
    PluginStatus,
    get_plugin_manager,
)
from cos.runtime.configuration_manager import (
    ConfigurationManager,
    IConfigurationManager,
    get_configuration_manager,
)
from cos.runtime.runtime_lifecycle import (
    RuntimeLifecycle,
    IRuntimeLifecycle,
    RuntimeStatus,
    get_runtime_lifecycle,
)

__all__ = [
    # Service Registry
    "ServiceRegistry",
    "IServiceRegistry",
    "ServiceMetadata",
    "get_service_registry",
    # Dependency Injection
    "DependencyInjection",
    "IDependencyInjection",
    "Lifetime",
    "Binding",
    "Scope",
    "get_dependency_injection",
    # Event Bus
    "EventBus",
    "IEventBus",
    "Event",
    "Subscription",
    "get_event_bus",
    # Scheduler
    "Scheduler",
    "IScheduler",
    "Task",
    "TaskStatus",
    "ScheduledTask",
    "get_scheduler",
    # Pipeline Engine
    "PipelineEngine",
    "IPipelineEngine",
    "Pipeline",
    "PipelineStatus",
    "get_pipeline_engine",
    # Task Manager
    "TaskManager",
    "ITaskManager",
    "ManagedTask",
    "TaskState",
    "get_task_manager",
    # Resource Manager
    "ResourceManager",
    "IResourceManager",
    "ResourceLimit",
    "ResourceAllocation",
    "get_resource_manager",
    # Plugin Manager
    "PluginManager",
    "IPluginManager",
    "Plugin",
    "PluginStatus",
    "get_plugin_manager",
    # Configuration
    "ConfigurationManager",
    "IConfigurationManager",
    "get_configuration_manager",
    # Lifecycle
    "RuntimeLifecycle",
    "IRuntimeLifecycle",
    "RuntimeStatus",
    "get_runtime_lifecycle",
]
