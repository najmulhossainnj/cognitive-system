"""ARC Cognitive Pipeline - Runtime-executable pipeline for ARC tasks.

This module implements the ARC Cognitive Pipeline that executes within the
Runtime, following the architectural principle where applications submit
requests to the Runtime and the Runtime executes pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from cos.apps.arc_agent.arc_solver import ARCSolver
from cos.apps.arc_agent.grid_interpreter import GridInterpreter
from cos.apps.arc_agent.models import (
    ARCExample,
    ARCInputData,
    ARCOptions,
    ARCRequest,
    ARCResponse,
    ARCResult,
    ARCStep,
)
from cos.apps.arc_agent.pattern_discovery import PatternDiscovery
from cos.broker.cognitive_broker import CognitiveBroker
from cos.apps.arc_agent.arc_agent_legacy import ARCSolution


@dataclass
class ARCPipelineConfig:
    """Configuration for ARC Pipeline execution."""

    use_reasoning: bool = True
    use_planning: bool = True
    use_decision: bool = True
    use_learning: bool = True
    use_memory: bool = True
    use_world_model: bool = True
    use_meta_cognition: bool = True
    confidence_threshold: float = 0.5


class ARCCognitivePipeline:
    """ARC Cognitive Pipeline for Runtime execution.

    This pipeline executes ARC tasks through the Cognitive Operating System,
    using the CognitiveBroker to access cognitive services.

    Pipeline Stages:
        1. Parse - Interpret grid data into symbolic representation
        2. Reason - Apply reasoning to find patterns
        3. Plan - Generate transformation plan
        4. Decide - Select best transformation
        5. Learn - Store learned patterns
        6. Reflect - Self-evaluate confidence
        7. Respond - Generate output

    Example:
        >>> pipeline = ARCCognitivePipeline(broker)
        >>> request = ARCRequest(task_data=ARCInputData(...))
        >>> response = await pipeline.execute(request)
    """

    def __init__(
        self,
        broker: CognitiveBroker,
        config: ARCPipelineConfig | None = None,
    ) -> None:
        """Initialize the ARC Cognitive Pipeline.

        Args:
            broker: Cognitive Broker for accessing cognitive services
            config: Pipeline configuration
        """
        self._broker = broker
        self._config = config or ARCPipelineConfig()
        self._grid_interpreter = GridInterpreter()
        self._pattern_discovery = PatternDiscovery()
        self._solver = ARCSolver()

    async def execute(self, request: ARCRequest) -> ARCResponse:
        """Execute the ARC Cognitive Pipeline.

        Args:
            request: Standard ARC request from the application

        Returns:
            Standard ARC response from the Runtime
        """
        trace: list[ARCStep] = []
        step_num = 0

        # Initialize variables for later use
        patterns = []
        solution = None
        selected_pattern = "unknown"
        test_input = request.task_data.test[0].input if request.task_data.test else []

        # Stage 1: Parse - Interpret grid data
        step_num += 1
        step = ARCStep(
            step=step_num,
            stage="parse",
            action="interpret_grid",
            timestamp=datetime.now(),
        )
        training_pairs = []
        for example in request.task_data.train:
            interpreted = await self._grid_interpreter.interpret(example.model_dump())
            training_pairs.append(interpreted)
        step.input_summary = {"examples": len(training_pairs)}
        step.output_summary = {"symbols_created": len(training_pairs) * 2}
        step.confidence = 0.8
        trace.append(step)

        # Stage 2: Reason - Find patterns using cognitive services
        if self._config.use_reasoning:
            step_num += 1
            step = ARCStep(
                step=step_num,
                stage="reason",
                action="discover_patterns",
                timestamp=datetime.now(),
            )

            # Use Reasoning Service
            reasoning_result = await self._broker.reasoning.solve({
                "type": "induction",
                "observations": [str(p) for p in training_pairs],
            })

            # Discover patterns
            patterns = await self._pattern_discovery.discover(training_pairs)
            step.input_summary = {"training_pairs": len(training_pairs)}
            step.output_summary = {"patterns_found": len(patterns)}
            step.confidence = reasoning_result.get("confidence", 0.7)
            trace.append(step)

        # Stage 3: Plan - Generate transformation plan
        if self._config.use_planning:
            step_num += 1
            step = ARCStep(
                step=step_num,
                stage="plan",
                action="generate_plan",
                timestamp=datetime.now(),
            )

            planning_result = await self._broker.planning.plan({
                "goal": "transform_grid",
                "depth": 2,
            })

            step.input_summary = {"patterns": len(patterns)}
            step.output_summary = {"plan_generated": planning_result.get("status") == "generated"}
            step.confidence = 0.75
            trace.append(step)

        # Stage 4: Decide - Select best transformation
        if self._config.use_decision:
            step_num += 1
            step = ARCStep(
                step=step_num,
                stage="decide",
                action="select_transformation",
                timestamp=datetime.now(),
            )

            # Create solution object
            solution = ARCSolution(
                task_id=request.request_id,
                input_grid=test_input,
                output_grid=[],
            )

            solution = await self._solver.solve(
                training_pairs=training_pairs,
                test_input=test_input,
                patterns=patterns,
                solution=solution,
            )

            # Extract selected pattern from trace
            for trace_item in solution.reasoning_trace:
                if "Selected:" in trace_item:
                    selected_pattern = trace_item.replace("Selected:", "").strip()

            step.input_summary = {"candidates": len(patterns)}
            step.output_summary = {
                "selected": selected_pattern,
                "confidence": solution.confidence,
            }
            step.confidence = solution.confidence
            trace.append(step)

        # Stage 5: Learn - Store learned patterns
        if self._config.use_learning and self._config.use_memory and solution:
            step_num += 1
            step = ARCStep(
                step=step_num,
                stage="learn",
                action="store_pattern",
                timestamp=datetime.now(),
            )

            if solution.confidence >= self._config.confidence_threshold:
                # Store in Semantic Memory
                await self._broker.memory.store({
                    "category": "arc_transformation",
                    "pattern_type": selected_pattern,
                    "confidence": solution.confidence,
                    "input_summary": self._summarize_grid(test_input),
                    "tags": ["arc", "learned"],
                }, memory_type="semantic")

                # Record in Episodic Memory
                await self._broker.memory.store({
                    "type": "arc_solving",
                    "task_id": request.task_data.task_id,
                    "success": solution.confidence >= 0.8,
                    "confidence": solution.confidence,
                }, memory_type="episodic")

            step.input_summary = {"confidence": solution.confidence if solution else 0.0}
            step.output_summary = {"learned": solution.confidence >= self._config.confidence_threshold if solution else False}
            step.confidence = 0.85
            trace.append(step)

        # Stage 6: Reflect - Self-evaluate
        if self._config.use_meta_cognition and solution:
            step_num += 1
            step = ARCStep(
                step=step_num,
                stage="reflect",
                action="evaluate_confidence",
                timestamp=datetime.now(),
            )

            # Use Meta-Cognition
            await self._broker.meta.observe({
                "pipeline": "arc",
                "confidence": solution.confidence,
                "patterns_used": selected_pattern,
            })

            reflection = await self._broker.meta.reflect({
                "content": f"ARC task confidence: {solution.confidence}",
            })

            step.input_summary = {"raw_confidence": solution.confidence}
            step.output_summary = {"reflection": reflection[:100] if reflection else ""}
            step.confidence = solution.confidence
            trace.append(step)

        # Stage 7: Respond - Generate output
        step_num += 1
        step = ARCStep(
            step=step_num,
            stage="respond",
            action="generate_output",
            timestamp=datetime.now(),
        )

        # Provide default values if solution is None
        output_grid = solution.output_grid if solution and solution.output_grid else test_input
        final_confidence = solution.confidence if solution else 0.0
        learned_from_memory = solution.learned_from_memory if solution else False

        result = ARCResult(
            output_grids=[output_grid],
            primary_output=output_grid,
            pattern_type=selected_pattern,
            learned_from_memory=learned_from_memory,
            execution_pipeline=[s.stage for s in trace],
        )

        step.input_summary = {"input_grid": test_input}
        step.output_summary = {"output_grid": result.primary_output}
        step.confidence = final_confidence
        trace.append(step)

        # Build response
        response = ARCResponse(
            response_id=f"arc-response-{datetime.now().timestamp()}",
            request_id=request.request_id,
            status="completed" if final_confidence > 0 else "failed",
            result=result,
            trace=trace,
            metadata={
                "task_id": request.task_data.task_id,
                "pipeline_config": self._config.__dict__,
            },
            confidence=final_confidence,
        )

        return response

    def _summarize_grid(self, grid: list[list[int]]) -> dict[str, Any]:
        """Create a summary of a grid."""
        if not grid:
            return {"width": 0, "height": 0, "colors": []}

        height = len(grid)
        width = len(grid[0]) if grid[0] else 0
        colors = list({cell for row in grid for cell in row})

        return {
            "width": width,
            "height": height,
            "colors": sorted(colors),
        }


class ARCRequestBuilder:
    """Builds standardized ARC requests for the Runtime.

    This is the application's responsibility - to prepare requests
    in the standard COS format.
    """

    @staticmethod
    def from_json(task_data: dict[str, Any]) -> ARCRequest:
        """Build request from JSON data.

        Args:
            task_data: JSON representation of ARC task

        Returns:
            Standard ARC request
        """
        train_examples = [
            ARCExample(input=e.get("input", []), output=e.get("output"))
            for e in task_data.get("train", [])
        ]
        test_examples = [
            ARCExample(input=e.get("input", []))
            for e in task_data.get("test", [])
        ]

        input_data = ARCInputData(
            train=train_examples,
            test=test_examples,
            task_id=task_data.get("id"),
        )

        options = ARCOptions(
            validate=task_data.get("options", {}).get("validate", True),
            max_attempts=task_data.get("options", {}).get("max_attempts", 3),
            confidence_threshold=task_data.get("options", {}).get("confidence_threshold", 0.5),
            use_memory=task_data.get("options", {}).get("use_memory", True),
        )

        return ARCRequest(
            task_data=input_data,
            options=options,
            metadata=task_data.get("metadata", {}),
        )


class ARCResponseFormatter:
    """Formats ARC responses for application-specific needs.

    The Runtime returns standard responses, and applications
    format them for their specific use cases.
    """

    @staticmethod
    def to_solution(response: ARCResponse) -> dict[str, Any]:
        """Format response as legacy solution dict.

        Args:
            response: Standard ARC response

        Returns:
            Legacy solution format
        """
        return {
            "task_id": response.metadata.get("task_id"),
            "input_grid": [],  # Not stored in response
            "output_grid": response.result.primary_output,
            "confidence": response.confidence,
            "reasoning_trace": [f"{s.stage}: {s.action}" for s in response.trace],
            "learned_from_memory": response.result.learned_from_memory,
        }

    @staticmethod
    def to_simple_dict(response: ARCResponse) -> dict[str, Any]:
        """Format response as simple dict.

        Args:
            response: Standard ARC response

        Returns:
            Simple dict with essential info
        """
        return {
            "output": response.result.primary_output,
            "confidence": response.confidence,
            "pattern": response.result.pattern_type,
            "steps": len(response.trace),
        }
