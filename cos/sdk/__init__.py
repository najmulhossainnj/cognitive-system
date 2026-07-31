"""SDK module for the Cognitive Operating System.

This module provides SDKs for building cognitive applications:
- DomainSDK: Access to cognitive capabilities
- MemorySDK: Memory operations
- ModuleSDK: Creating cognitive modules
- PluginSDK: Creating plugins
- TestingSDK: Testing utilities
"""

from cos.sdk.domain_sdk import DomainSDK
from cos.sdk.memory_sdk import MemorySDK
from cos.sdk.module_sdk import ModuleSDK
from cos.sdk.plugin_sdk import PluginSDK, create_plugin
from cos.sdk.testing_sdk import MockContext, TestRunner, run_async_test

__all__ = [
    "DomainSDK",
    "MemorySDK",
    "ModuleSDK",
    "PluginSDK",
    "create_plugin",
    "MockContext",
    "TestRunner",
    "run_async_test",
]
