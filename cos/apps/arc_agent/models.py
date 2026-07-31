"""ARC Agent Models - Standard COS Request/Response formats.

This module defines the standardized COS request and response formats
for ARC-AGI-2 tasks, following the architectural principles where
applications prepare requests and the Runtime executes them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ARCExample(BaseModel):
    """Single ARC example (input/output pair)."""

    input: list[list[int]] = Field(default_factory=list)
    output: list[list[int]] | None = None


class ARCOptions(BaseModel):
    """Options for ARC task execution."""

    validate: bool = True
    max_attempts: int = 3
    confidence_threshold: float = 0.5
    use_memory: bool = True
    explain: bool = False


class ARCInputData(BaseModel):
    """Input data for an ARC task."""

    train: list[ARCExample] = Field(default_factory=list)
    test: list[ARCExample] = Field(default_factory=list)
    task_id: str | None = None


class ARCRequest(BaseModel):
    """Standard COS Request format for ARC tasks.

    Applications create this request format, and the Runtime executes
    it through the Cognitive Pipeline.
    """

    request_id: str = Field(default_factory=lambda: f"arc-{datetime.now().timestamp()}")
    request_type: str = "arc_task"
    task_data: ARCInputData
    options: ARCOptions = Field(default_factory=ARCOptions)
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class ARCResponse(BaseModel):
    """Standard COS Response format for ARC tasks.

    The Runtime returns this format, and applications format it
    for their specific needs.
    """

    response_id: str
    request_id: str
    status: str
    result: ARCResult
    trace: list[ARCStep] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)


class ARCResult(BaseModel):
    """Result of an ARC task execution."""

    output_grids: list[list[list[int]]] = Field(default_factory=list)
    primary_output: list[list[int]] | None = None
    pattern_type: str | None = None
    learned_from_memory: bool = False
    execution_pipeline: list[str] = Field(default_factory=list)


class ARCStep(BaseModel):
    """Single step in the ARC execution trace."""

    step: int
    stage: str
    action: str
    input_summary: dict[str, Any] | None = None
    output_summary: dict[str, Any] | None = None
    confidence: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)


# Legacy compatibility aliases
@dataclass
class ARCTask:
    """Legacy: Represents an ARC-AGI-2 task.

    Deprecated: Use ARCInputData instead.
    """

    train: list[dict[str, Any]] = field(default_factory=list)
    test: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ARCSolution:
    """Legacy: Represents an ARC task solution.

    Deprecated: Use ARCResponse instead.
    """

    task_id: str
    input_grid: list[list[int]]
    output_grid: list[list[int]]
    confidence: float = 0.0
    reasoning_trace: list[str] = field(default_factory=list)
    learned_from_memory: bool = False
