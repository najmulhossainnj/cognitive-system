"""Cognitive Pipeline Implementation.

This module provides the cognitive execution pipeline that orchestrates
all cognitive capabilities to solve problems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from cos.broker.cognitive_broker import CognitiveBroker


class ExecutionStatus(str, Enum):
    """Pipeline execution status."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PipelineStage:
    """Represents a stage in the cognitive pipeline."""

    name: str
    handler: str
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineStep:
    """Represents a step in the pipeline."""

    id: str
    stage: str
    action: str
    input: dict[str, Any]
    output: dict[str, Any] | None = None
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None


@dataclass
class PipelineExecution:
    """Represents a pipeline execution."""

    id: str
    request: dict[str, Any]
    stages: list[PipelineStage]
    steps: list[PipelineStep] = field(default_factory=list)
    status: ExecutionStatus = ExecutionStatus.PENDING
    result: dict[str, Any] | None = None
    trace: list[dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None


class CognitivePipeline:
    """Cognitive Pipeline for cognitive execution.

    The pipeline orchestrates all cognitive capabilities to solve problems.
    """

    def __init__(self, broker: CognitiveBroker) -> None:
        """Initialize the cognitive pipeline.

        Args:
            broker: Cognitive broker instance
        """
        self._broker = broker
        self._executions: dict[str, PipelineExecution] = {}
        self._default_stages = [
            PipelineStage(name="parse", handler="reasoning"),
            PipelineStage(name="reason", handler="reasoning"),
            PipelineStage(name="plan", handler="planning"),
            PipelineStage(name="decide", handler="decision"),
            PipelineStage(name="learn", handler="learning"),
            PipelineStage(name="reflect", handler="meta"),
            PipelineStage(name="respond", handler="assistant"),
        ]

    async def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        """Execute the pipeline.

        Args:
            request: Request to process

        Returns:
            Pipeline result
        """
        execution_id = str(uuid4())

        stages = self._default_stages.copy()
        if "stages" in request:
            stages = [PipelineStage(**s) for s in request["stages"]]

        execution = PipelineExecution(
            id=execution_id,
            request=request,
            stages=stages,
        )
        self._executions[execution_id] = execution

        try:
            execution.status = ExecutionStatus.RUNNING
            execution.started_at = datetime.now()

            for stage in stages:
                step = PipelineStep(
                    id=str(uuid4()),
                    stage=stage.name,
                    action=stage.handler,
                    input=request,
                )
                execution.steps.append(step)

                try:
                    step.status = ExecutionStatus.RUNNING
                    step.started_at = datetime.now()

                    output = await self._execute_stage(stage, request)

                    step.output = output
                    step.status = ExecutionStatus.COMPLETED
                    step.completed_at = datetime.now()

                    request = output
                    execution.trace.append({
                        "stage": stage.name,
                        "output": output,
                    })

                except Exception as e:
                    step.status = ExecutionStatus.FAILED
                    step.error = str(e)
                    execution.status = ExecutionStatus.FAILED
                    execution.result = {"error": str(e)}
                    break

            if execution.status == ExecutionStatus.RUNNING:
                execution.status = ExecutionStatus.COMPLETED
                execution.result = request

            execution.completed_at = datetime.now()

        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.result = {"error": str(e)}

        return {
            "execution_id": execution_id,
            "status": execution.status.value,
            "result": execution.result,
            "trace": execution.trace,
        }

    async def _execute_stage(
        self,
        stage: PipelineStage,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute a single stage.

        Args:
            stage: Stage to execute
            input_data: Input data

        Returns:
            Stage output
        """
        handler = stage.handler
        stage_input = input_data.get("data", input_data)

        if handler == "reasoning":
            result = await self._broker.reasoning.solve(stage_input)
        elif handler == "planning":
            result = await self._broker.planning.plan(stage_input)
        elif handler == "decision":
            alternatives = stage_input.get("alternatives", [])
            result = await self._broker.decision.decide({"alternatives": alternatives})
        elif handler == "learning":
            if "experience" in stage_input:
                result = await self._broker.learning.learn(stage_input["experience"])
            else:
                result = await self._broker.learning.get_insights()
        elif handler == "meta":
            result = await self._broker.meta.monitor()
        elif handler == "assistant":
            if "query" in stage_input:
                result = await self._broker.assistant.respond(stage_input["query"])
            else:
                result = {"status": "ok"}
        else:
            result = {"status": "ok", "stage": stage.name}

        return result

    async def pause(self, execution_id: str) -> None:
        """Pause execution.

        Args:
            execution_id: Execution to pause
        """
        execution = self._executions.get(execution_id)
        if execution and execution.status == ExecutionStatus.RUNNING:
            execution.status = ExecutionStatus.PAUSED

    async def resume(self, execution_id: str) -> None:
        """Resume execution.

        Args:
            execution_id: Execution to resume
        """
        execution = self._executions.get(execution_id)
        if execution and execution.status == ExecutionStatus.PAUSED:
            execution.status = ExecutionStatus.RUNNING

    async def cancel(self, execution_id: str) -> None:
        """Cancel execution.

        Args:
            execution_id: Execution to cancel
        """
        execution = self._executions.get(execution_id)
        if execution and execution.status in (ExecutionStatus.RUNNING, ExecutionStatus.PAUSED):
            execution.status = ExecutionStatus.CANCELLED

    async def get_trace(self, execution_id: str) -> list[dict[str, Any]]:
        """Get execution trace.

        Args:
            execution_id: Execution ID

        Returns:
            Execution trace
        """
        execution = self._executions.get(execution_id)
        return execution.trace if execution else []

    async def explain(self, execution_id: str) -> str:
        """Explain execution.

        Args:
            execution_id: Execution ID

        Returns:
            Explanation
        """
        execution = self._executions.get(execution_id)
        if not execution:
            return "Execution not found."

        steps_summary = [f"Stage: {step.stage} ({step.status.value})" for step in execution.steps]
        return "Cognitive pipeline execution:\n" + "\n".join(steps_summary)

    async def get_confidence(self, execution_id: str) -> float:
        """Get execution confidence.

        Args:
            execution_id: Execution ID

        Returns:
            Confidence estimate
        """
        execution = self._executions.get(execution_id)
        if not execution:
            return 0.0

        completed_steps = sum(1 for s in execution.steps if s.status == ExecutionStatus.COMPLETED)
        total_steps = len(execution.stages)

        if total_steps == 0:
            return 0.0

        base_confidence = completed_steps / total_steps

        if execution.status == ExecutionStatus.FAILED:
            base_confidence *= 0.5

        execution.confidence = base_confidence
        return base_confidence

    async def get_status(self, execution_id: str) -> dict[str, Any]:
        """Get execution status.

        Args:
            execution_id: Execution ID

        Returns:
            Status information
        """
        execution = self._executions.get(execution_id)
        if not execution:
            return {"status": "not_found"}

        completed = sum(1 for s in execution.steps if s.status == ExecutionStatus.COMPLETED)
        return {
            "execution_id": execution.id,
            "status": execution.status.value,
            "stages_total": len(execution.stages),
            "stages_completed": completed,
            "created_at": execution.created_at.isoformat(),
            "started_at": execution.started_at.isoformat() if execution.started_at else None,
            "completed_at": (
                execution.completed_at.isoformat() if execution.completed_at else None
            ),
        }

    async def get_metrics(self, execution_id: str) -> dict[str, Any]:
        """Get execution metrics.

        Args:
            execution_id: Execution ID

        Returns:
            Metrics
        """
        execution = self._executions.get(execution_id)
        if not execution:
            return {}

        duration = None
        if execution.started_at and execution.completed_at:
            duration = (execution.completed_at - execution.started_at).total_seconds()
        elif execution.started_at:
            duration = (datetime.now() - execution.started_at).total_seconds()

        completed = sum(1 for s in execution.steps if s.status == ExecutionStatus.COMPLETED)
        failed = sum(1 for s in execution.steps if s.status == ExecutionStatus.FAILED)
        return {
            "execution_id": execution.id,
            "total_stages": len(execution.stages),
            "completed_stages": completed,
            "failed_stages": failed,
            "duration_seconds": duration,
            "confidence": execution.confidence,
        }


class RequestLifecycle:
    """Request Lifecycle manager.

    Manages the lifecycle of requests through the system.
    """

    def __init__(self, pipeline: CognitivePipeline) -> None:
        """Initialize request lifecycle.

        Args:
            pipeline: Cognitive pipeline
        """
        self._pipeline = pipeline
        self._requests: dict[str, dict[str, Any]] = {}

    async def submit(self, request: dict[str, Any]) -> str:
        """Submit a request.

        Args:
            request: Request to submit

        Returns:
            Request ID
        """
        request_id = str(uuid4())
        self._requests[request_id] = {
            "id": request_id,
            "request": request,
            "status": "submitted",
            "submitted_at": datetime.now().isoformat(),
        }

        result = await self._pipeline.execute(request)

        self._requests[request_id]["status"] = result.get("status", "completed")
        self._requests[request_id]["result"] = result
        self._requests[request_id]["execution_id"] = result.get("execution_id")

        return request_id

    async def get_status(self, request_id: str) -> dict[str, Any]:
        """Get request status.

        Args:
            request_id: Request ID

        Returns:
            Status
        """
        request = self._requests.get(request_id)
        if not request:
            return {"status": "not_found"}

        return {
            "request_id": request_id,
            "status": request["status"],
            "submitted_at": request["submitted_at"],
        }

    async def cancel(self, request_id: str) -> bool:
        """Cancel a request.

        Args:
            request_id: Request to cancel

        Returns:
            True if cancelled
        """
        request = self._requests.get(request_id)
        if not request:
            return False

        execution_id = request.get("execution_id")
        if execution_id:
            await self._pipeline.cancel(execution_id)
            request["status"] = "cancelled"
            return True

        return False

    async def get_result(self, request_id: str) -> dict[str, Any] | None:
        """Get request result.

        Args:
            request_id: Request ID

        Returns:
            Result or None
        """
        request = self._requests.get(request_id)
        if not request:
            return None

        return request.get("result")
