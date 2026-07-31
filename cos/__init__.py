"""Cognitive Operating System (COS)

A reusable cognitive architecture for domain-independent reasoning.

Architecture:
    Applications
         |
         v
    Cognitive Context
         |
         v
    Cognitive Broker
         |
         v
    Cognitive Services
         |
         v
    Cognitive Kernel

Modules:
    kernel: Deterministic runtime infrastructure
    broker: Unified cognitive facade
    services: Cognitive capability implementations
    applications: Domain-specific applications
    sdk: Software development kits
    shared: Common data models and utilities

Usage:
    >>> from cos import CognitiveContext
    >>> context = CognitiveContext.create()
    >>> result = context.cognition.reasoning.solve(task)
"""

__version__ = "0.1.0"
__author__ = "COS Team"

from cos.kernel.context.cognitive_context import CognitiveContext
from cos.broker.cognitive_broker import CognitiveBroker

__all__ = [
    "CognitiveBroker",
    "CognitiveContext",
    "__version__",
]
