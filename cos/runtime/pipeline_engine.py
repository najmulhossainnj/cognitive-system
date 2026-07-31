"""Pipeline Engine Implementation.

This module provides the Pipeline Engine for workflow orchestration.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class PipelineStatus(str, Enum):
    """Pipeline status values."""

    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Pipeline:
    """Represents a pipeline."""

    id: str
    stages: list[dict[str, Any]]
    status: PipelineStatus = PipelineStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: Any = None
    error: str | None = None


@dataclass
class PipelineStage:
    """Represents a pipeline stage."""

    name: str
    handler: Any
    input_key: str = "input"
    output_key: str = "output"


class PipelineEngine:
    """Pipeline Engine provides workflow orchestration.

    The Pipeline Engine is responsible for:
    - Executing pipelines
    - Coordinating stages
    - Managing state
    - Handling errors

    See RUNTIME-005 for full specification.
    """

    def __init__(self) -> None:
        """Initialize the pipeline engine."""
        self._pipelines: dict[str, Pipeline] = {}
        self._executing: set[str] = set()
        self._results: dict[str, dict[str, Any]] = {}

    async def execute(
        self,
        pipeline_id: str,
        input_data: Any,
    ) -> Any:
        """Execute a pipeline.

        Args:
            pipeline_id: Pipeline to execute
            input_data: Input data

        Returns:
            Pipeline result
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")

        pipeline.status = PipelineStatus.RUNNING
        pipeline.started_at = datetime.now()
        self._executing.add(pipeline_id)

        current_data = input_data
        self._results[pipeline_id] = {}

        try:
            for i, stage_def in enumerate(pipeline.stages):
                handler = stage_def.get("handler")
                if not handler:
                    continue

                input_key = stage_def.get("input_key", "input")
                output_key = stage_def.get("output_key", f"stage_{i}_output")

                stage_input = current_data
                if input_key in self._results[pipeline_id]:
                    stage_input = self._results[pipeline_id][input_key]

                if asyncio.iscoroutinefunction(handler):
                    result = await handler(stage_input)
                elif callable(handler):
                    result = handler(stage_input)
                    if asyncio.iscoroutine(result):
                        result = await result
                else:
                    result = stage_input

                self._results[pipeline_id][output_key] = result
                current_data = result

            pipeline.result = current_data
            pipeline.status = PipelineStatus.COMPLETED
            pipeline.completed_at = datetime.now()
            return current_data

        except Exception as e:
            pipeline.error = str(e)
            pipeline.status = PipelineStatus.FAILED
            pipeline.completed_at = datetime.now()
            raise

        finally:
            self._executing.discard(pipeline_id)

    async def start(self, pipeline_id: str) -> None:
        """Start a pipeline.

        Args:
            pipeline_id: Pipeline to start
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")

        pipeline.status = PipelineStatus.RUNNING
        pipeline.started_at = datetime.now()

    async def pause(self, pipeline_id: str) -> None:
        """Pause a pipeline.

        Args:
            pipeline_id: Pipeline to pause
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")

        pipeline.status = PipelineStatus.PAUSED

    async def resume(self, pipeline_id: str) -> None:
        """Resume a pipeline.

        Args:
            pipeline_id: Pipeline to resume
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")

        pipeline.status = PipelineStatus.RUNNING

    async def cancel(self, pipeline_id: str) -> None:
        """Cancel a pipeline.

        Args:
            pipeline_id: Pipeline to cancel
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")

        pipeline.status = PipelineStatus.CANCELLED
        pipeline.completed_at = datetime.now()
        self._executing.discard(pipeline_id)

    async def status(self, pipeline_id: str) -> dict[str, Any]:
        """Get pipeline status.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            Status information
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"status": "not_found"}

        return {
            "id": pipeline.id,
            "status": pipeline.status.value,
            "created_at": pipeline.created_at.isoformat(),
            "started_at": pipeline.started_at.isoformat() if pipeline.started_at else None,
            "completed_at": pipeline.completed_at.isoformat() if pipeline.completed_at else None,
            "error": pipeline.error,
        }

    async def history(self, pipeline_id: str) -> list[dict[str, Any]]:
        """Get pipeline execution history.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            Execution history
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return []

        return [
            {
                "timestamp": pipeline.created_at.isoformat(),
                "status": pipeline.status.value,
                "result": str(pipeline.result)[:100] if pipeline.result else None,
                "error": pipeline.error,
            }
        ]

    async def monitor(self, pipeline_id: str) -> dict[str, Any]:
        """Monitor pipeline execution.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            Monitoring data
        """
        return await self.status(pipeline_id)

    async def validate(self, pipeline_id: str) -> bool:
        """Validate a pipeline.

        Args:
            pipeline_id: Pipeline to validate

        Returns:
            True if valid
        """
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return False

        if not pipeline.stages:
            return False

        return True

    async def create_pipeline(
        self,
        stages: list[dict[str, Any]],
    ) -> str:
        """Create a new pipeline.

        Args:
            stages: Pipeline stages

        Returns:
            Pipeline ID
        """
        pipeline_id = str(uuid4())
        pipeline = Pipeline(id=pipeline_id, stages=stages)
        self._pipelines[pipeline_id] = pipeline
        return pipeline_id

    def get_pipeline(self, pipeline_id: str) -> Pipeline | None:
        """Get a pipeline by ID.

        Args:
            pipeline_id: Pipeline ID

        Returns:
            Pipeline or None
        """
        return self._pipelines.get(pipeline_id)


# Module-level singleton instance
_pipeline_engine: PipelineEngine | None = None


def get_pipeline_engine() -> PipelineEngine:
    """Get the global pipeline engine instance.

    Returns:
        PipelineEngine instance
    """
    global _pipeline_engine
    if _pipeline_engine is None:
        _pipeline_engine = PipelineEngine()
    return _pipeline_engine


# Re-export interface for type hints
IPipelineEngine = PipelineEngine
