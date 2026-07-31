"""ARC Agent - Application for solving ARC-AGI-2 tasks.

The ARC Agent bridges the ARC-AGI-2 benchmark dataset and the
Cognitive Operating System by converting tasks into standardized
COS requests. It integrates with COS memory services for
automatic experience-based learning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from cos.apps.arc_agent.arc_solver import ARCSolver
from cos.apps.arc_agent.grid_interpreter import GridInterpreter
from cos.apps.arc_agent.pattern_discovery import PatternDiscovery
from cos.services.memory.memory_service import (
    EpisodicMemoryService,
    SemanticMemoryService,
    WorkingMemoryService,
)


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
    learned_from_memory: bool = False


class ARCAgent:
    """ARC Agent Application (APP-140).

    Converts ARC-AGI-2 benchmark tasks into standardized COS requests
    and coordinates cognitive processing to solve them.

    Integrates with COS memory services for automatic learning:
    - WorkingMemory: Current task state
    - SemanticMemory: Learned patterns (persistent)
    - EpisodicMemory: Solving experiences

    Pipeline:
        1. Load ARC Task
        2. Check Semantic Memory for similar patterns
        3. Initialize Working Memory
        4. Perception and Grid Interpretation
        5. Pattern Discovery (combined with memory)
        6. Reasoning Pipeline
        7. Planning
        8. Constraint Validation
        9. Decision Engine
        10. Reflection
        11. Learn: Store patterns in Semantic/Episodic Memory
        12. Solve Test Input
    """

    def __init__(
        self,
        working_memory: WorkingMemoryService | None = None,
        semantic_memory: SemanticMemoryService | None = None,
        episodic_memory: EpisodicMemoryService | None = None,
    ) -> None:
        """Initialize the ARC Agent with memory services.

        Args:
            working_memory: Working memory for active tasks
            semantic_memory: Semantic memory for learned patterns
            episodic_memory: Episodic memory for experiences
        """
        self._grid_interpreter = GridInterpreter()
        self._pattern_discovery = PatternDiscovery()
        self._solver = ARCSolver()

        # Memory services for automatic learning
        self._working_memory = working_memory or WorkingMemoryService()
        self._semantic_memory = semantic_memory or SemanticMemoryService()
        self._episodic_memory = episodic_memory or EpisodicMemoryService()

        self._task_history: list[ARCTask] = []
        self._workspace_id: str | None = None

    async def _initialize_workspace(self) -> None:
        """Initialize working memory workspace."""
        if self._workspace_id is None:
            self._workspace_id = await self._working_memory.create_workspace()

    async def _learn_from_solution(self, task: ARCTask, solution: ARCSolution) -> None:
        """Learn from solving experience - stores in Semantic and Episodic memory.

        This enables automatic learning from experience without explicit training.
        """
        if solution.confidence < 0.5:
            return

        # Store learned pattern in Semantic Memory
        pattern_concept = {
            "id": f"arc_pattern_{solution.task_id}",
            "category": "arc_transformation",
            "pattern_type": self._extract_pattern_type(solution),
            "confidence": solution.confidence,
            "training_count": len(task.train),
            "input_summary": self._summarize_grid(task.train[0]["input"] if task.train else []),
            "output_summary": self._summarize_grid(solution.output_grid),
            "tags": ["arc", "transformation", "learned"],
            "importance": solution.confidence,
            "learned_at": datetime.now().isoformat(),
        }
        await self._semantic_memory.store_concept(pattern_concept)

        # Record episode in Episodic Memory
        episode = {
            "id": f"arc_episode_{solution.task_id}",
            "task_id": solution.task_id,
            "type": "arc_solving",
            "success": solution.confidence >= 0.8,
            "confidence": solution.confidence,
            "training_examples": len(task.train),
            "reasoning_steps": len(solution.reasoning_trace),
            "pattern_used": pattern_concept["pattern_type"],
            "timestamp": datetime.now().isoformat(),
            "importance": solution.confidence,
        }
        await self._episodic_memory.record_episode(episode)

        solution.reasoning_trace.append("Learned patterns stored in semantic memory")
        solution.reasoning_trace.append("Experience recorded in episodic memory")

    def _extract_pattern_type(self, solution: ARCSolution) -> str:
        """Extract the pattern type from solution trace."""
        for trace in solution.reasoning_trace:
            if "Selected:" in trace:
                return trace.replace("Selected:", "").strip()
        return "unknown"

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

    async def _check_memory_for_patterns(
        self,
        task: ARCTask,
    ) -> list[dict[str, Any]]:
        """Check semantic memory for relevant learned patterns.

        This enables the agent to leverage past experience automatically.
        """
        # Create query based on current task characteristics
        query = {
            "category": "arc_transformation",
            "tags": ["arc", "learned"],
        }

        learned_patterns = await self._semantic_memory.search_concepts(query)

        # Filter patterns that might be relevant
        current_summary = self._summarize_grid(task.train[0]["input"] if task.train else [])
        relevant_patterns = []

        for pattern in learned_patterns:
            # Check if pattern has similar characteristics
            pattern_summary = pattern.get("input_summary", {})
            if self._patterns_are_similar(current_summary, pattern_summary):
                relevant_patterns.append(pattern)

        return relevant_patterns

    def _patterns_are_similar(
        self,
        summary1: dict[str, Any],
        summary2: dict[str, Any],
    ) -> bool:
        """Check if two pattern summaries are similar."""
        if summary1.get("width") != summary2.get("width"):
            return False
        if summary1.get("height") != summary2.get("height"):
            return False
        return True

    async def _get_past_experiences(self, limit: int = 5) -> list[dict[str, Any]]:
        """Get past solving experiences from episodic memory."""
        episodes = await self._episodic_memory.retrieve_episodes({
            "limit": limit,
            "type": "arc_solving",
        })
        return episodes

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
        """Solve an ARC task using the cognitive pipeline with automatic learning.

        The agent automatically:
        1. Checks semantic memory for similar past patterns
        2. Uses working memory for current task state
        3. Learns from successful solutions

        Args:
            task: The ARC task to solve

        Returns:
            ARCSolution with predicted output
        """
        # Initialize working memory
        await self._initialize_workspace()

        solution = ARCSolution(
            task_id=self._generate_task_id(),
            input_grid=[],
            output_grid=[],
        )

        # Step 1: Check semantic memory for learned patterns (experience)
        learned_patterns = await self._check_memory_for_patterns(task)
        if learned_patterns:
            solution.learned_from_memory = True
            solution.reasoning_trace.append(
                f"Found {len(learned_patterns)} learned patterns from memory"
            )

        # Store current task in working memory
        await self._working_memory.store_fact(self._workspace_id, {
            "type": "arc_task",
            "task_id": solution.task_id,
            "training_count": len(task.train),
            "test_count": len(task.test),
        })
        await self._working_memory.update_context(self._workspace_id, {
            "current_task": solution.task_id,
            "memory_aided": solution.learned_from_memory,
        })

        # Step 2: Parse task into symbolic representation
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

        # Step 11: Learn from this solution (automatic experience)
        await self._learn_from_solution(task, solution)

        return solution

    async def solve_batch(self, tasks: list[dict[str, Any]]) -> list[ARCSolution]:
        """Solve multiple ARC tasks.

        Each task is solved with automatic learning enabled.
        The system learns from each task, improving future performance.

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

    async def get_learned_patterns(self) -> list[dict[str, Any]]:
        """Get all learned patterns from semantic memory.

        Returns:
            List of learned patterns
        """
        return await self._semantic_memory.search_concepts({
            "category": "arc_transformation",
        })

    async def get_solving_experiences(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get past solving experiences from episodic memory.

        Args:
            limit: Maximum number of experiences to return

        Returns:
            List of past experiences
        """
        return await self._episodic_memory.retrieve_episodes({
            "limit": limit,
        })

    async def get_memory_stats(self) -> dict[str, Any]:
        """Get statistics about learned knowledge.

        Returns:
            Memory statistics
        """
        patterns = await self.get_learned_patterns()
        experiences = await self.get_solving_experiences(limit=100)

        successful = [e for e in experiences if e.get("success")]
        avg_confidence = (
            sum(e.get("confidence", 0) for e in experiences) / len(experiences)
            if experiences else 0
        )

        return {
            "learned_patterns": len(patterns),
            "total_experiences": len(experiences),
            "successful_solutions": len(successful),
            "average_confidence": round(avg_confidence, 2),
            "success_rate": round(len(successful) / len(experiences), 2) if experiences else 0,
        }

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
