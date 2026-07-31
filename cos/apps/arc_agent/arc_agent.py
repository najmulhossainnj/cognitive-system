"""ARC Agent - Application for solving ARC-AGI-2 tasks.

The ARC Agent bridges the ARC-AGI-2 benchmark dataset and the
Cognitive Operating System by converting tasks into standardized
COS requests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cos.apps.arc_agent.arc_solver import ARCSolver
from cos.apps.arc_agent.grid_interpreter import GridInterpreter
from cos.apps.arc_agent.pattern_discovery import PatternDiscovery


@dataclass
class ARCTask:
    """Represents an ARC-AGI-2 task."""

    train: list[dict[str, Any]] = field(default_factory=list)
    test: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ARCSolution:
    """Represents an ARC task solution."""

    task_id: str
    input_grid: list[list[int]]
    output_grid: list[list[int]]
    confidence: float = 0.0
    reasoning_trace: list[str] = field(default_factory=list)


class ARCAgent:
    """ARC Agent Application (APP-140).

    Converts ARC-AGI-2 benchmark tasks into standardized COS requests
    and coordinates cognitive processing to solve them.

    Pipeline:
        1. Load ARC Task
        2. Create Standard COS Request
        3. Initialize Working Memory
        4. Perception and Grid Interpretation
        5. Knowledge Graph Construction
        6. Pattern Discovery
        7. Reasoning Pipeline
        8. Planning
        9. Constraint Validation
        10. Decision Engine
        11. Reflection
        12. Learning
        13. Solve Test Input
    """

    def __init__(self) -> None:
        """Initialize the ARC Agent."""
        self._grid_interpreter = GridInterpreter()
        self._pattern_discovery = PatternDiscovery()
        self._solver = ARCSolver()
        self._task_history: list[ARCTask] = []

    def load_task(self, task_data: dict[str, Any]) -> ARCTask:
        """Load an ARC task from JSON data.

        Args:
            task_data: JSON representation of the task

        Returns:
            Parsed ARCTask
        """
        task = ARCTask(
            train=task_data.get("train", []),
            test=task_data.get("test", []),
            metadata=task_data.get("metadata", {}),
        )
        self._task_history.append(task)
        return task

    async def solve(self, task: ARCTask) -> ARCSolution:
        """Solve an ARC task using the cognitive pipeline.

        Args:
            task: The ARC task to solve

        Returns:
            ARCSolution with predicted output
        """
        solution = ARCSolution(
            task_id=self._generate_task_id(),
            input_grid=[],
            output_grid=[],
        )

        # Step 1-2: Parse task into symbolic representation
        training_pairs = []
        for i, example in enumerate(task.train):
            interpreted = await self._grid_interpreter.interpret(example)
            training_pairs.append(interpreted)
            solution.reasoning_trace.append(f"Training example {i+1} interpreted")

        # Step 3-5: Initialize working memory with perceived grids
        perceived_grids = []
        for pair in training_pairs:
            perceived_grids.append({
                "input": pair["input_symbolic"],
                "output": pair["output_symbolic"],
            })
            solution.reasoning_trace.append(f"Grid {pair['input_symbolic'].id} perceived")

        # Step 6: Pattern Discovery - find candidate transformations
        patterns = await self._pattern_discovery.discover(training_pairs)
        solution.reasoning_trace.append(f"{len(patterns)} candidate patterns discovered")

        # Step 7-10: Use the solver to find and validate the correct transformation
        test_input = task.test[0]["input"] if task.test else []
        solution = await self._solver.solve(
            training_pairs=training_pairs,
            test_input=test_input,
            patterns=patterns,
            solution=solution,
        )

        return solution

    async def solve_batch(self, tasks: list[dict[str, Any]]) -> list[ARCSolution]:
        """Solve multiple ARC tasks.

        Args:
            tasks: List of ARC task JSON data

        Returns:
            List of ARCSolutions
        """
        solutions = []
        for task_data in tasks:
            task = self.load_task(task_data)
            solution = await self.solve(task)
            solutions.append(solution)
        return solutions

    def _generate_task_id(self) -> str:
        """Generate a unique task ID.

        Returns:
            Task ID
        """
        return f"task_{len(self._task_history)}"

    def get_history(self) -> list[ARCTask]:
        """Get the history of solved tasks.

        Returns:
            List of ARCTask
        """
        return self._task_history
