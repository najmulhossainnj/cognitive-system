"""Applications module for the Cognitive Operating System.

This module contains application-specific agents built on top of COS:
- ARCAgent (APP-140): Solves ARC-AGI-2 benchmark tasks
"""

from cos.apps.arc_agent import (
    ARCAgent,
    GridInterpreter,
    PatternDiscovery,
    ARCSolver,
)

__all__ = [
    "ARCAgent",
    "ARCSolver",
    "GridInterpreter",
    "PatternDiscovery",
]
