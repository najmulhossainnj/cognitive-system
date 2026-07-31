"""ARC Agent Application (APP-140).

The ARC Agent converts ARC-AGI-2 benchmark tasks into standardized
COS requests for cognitive processing.

Architecture:
    The ARC Agent is a thin application that:
    1. Loads ARC JSON data
    2. Validates requests
    3. Converts to standardized COS Request format
    4. Submits to Runtime via Cognitive Pipeline
    5. Formats the Response

See COS-IMPLEMENTATION-001 for architectural guidance.
"""

from cos.apps.arc_agent.arc_agent import ARCAgent
from cos.apps.arc_agent.arc_pipeline import (
    ARCCognitivePipeline,
    ARCRequestBuilder,
    ARCResponseFormatter,
    ARCPipelineConfig,
)
from cos.apps.arc_agent.grid_interpreter import GridInterpreter
from cos.apps.arc_agent.models import (
    ARCRequest,
    ARCResponse,
    ARCInputData,
    ARCExample,
    ARCOptions,
    ARCResult,
    ARCStep,
)
from cos.apps.arc_agent.pattern_discovery import PatternDiscovery
from cos.apps.arc_agent.arc_solver import ARCSolver

__all__ = [
    "ARCAgent",
    "ARCCognitivePipeline",
    "ARCExample",
    "ARCInputData",
    "ARCOptions",
    "ARCPipelineConfig",
    "ARCRequest",
    "ARCRequestBuilder",
    "ARCResponse",
    "ARCResponseFormatter",
    "ARCResult",
    "ARCSolver",
    "ARCStep",
    "GridInterpreter",
    "PatternDiscovery",
]
