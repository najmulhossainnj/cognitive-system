"""ARC Agent Application (APP-140).

The ARC Agent converts ARC-AGI-2 benchmark tasks into standardized
COS requests for cognitive processing.
"""

from cos.apps.arc_agent.arc_agent import ARCAgent
from cos.apps.arc_agent.grid_interpreter import GridInterpreter
from cos.apps.arc_agent.pattern_discovery import PatternDiscovery
from cos.apps.arc_agent.arc_solver import ARCSolver

__all__ = [
    "ARCAgent",
    "ARCSolver",
    "GridInterpreter",
    "PatternDiscovery",
]
