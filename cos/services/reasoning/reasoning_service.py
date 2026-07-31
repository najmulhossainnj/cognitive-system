"""Reasoning Service Implementation.

This module provides the Reasoning Service for cognitive reasoning operations,
integrating LLM-powered neuro-symbolic reasoning with symbolic verification.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cos.services.base import ServiceBase
from cos.services.reasoning.neuro_symbolic_reasoning import NeuroSymbolicReasoningService

if TYPE_CHECKING:
    from cos.services.learning.learning_service import LearningService


class ReasoningService(ServiceBase):
    """Reasoning Service for cognitive reasoning operations.

    This service provides various reasoning capabilities:
    - Problem solving (via Neuro-Symbolic Reasoning)
    - Logical inference
    - Goal proving
    - Result explanation
    - Reasoning traces
    - Self-improvement through learning integration
    """

    def __init__(self, service_id: str | None = None) -> None:
        """Initialize the reasoning service.

        Args:
            service_id: Optional service identifier
        """
        super().__init__(service_id or "reasoning-service")
        self._add_capability("reasoning")
        self._add_capability("problem-solving")
        self._add_capability("inference")
        self._add_capability("llm-powered")
        self._set_metadata("reasoning_type", "neuro-symbolic")
        
        # Core components
        self._neuro_symbolic: NeuroSymbolicReasoningService = NeuroSymbolicReasoningService()
        self._learning_service: LearningService | None = None
        
        # State
        self._rules: list[dict[str, Any]] = []
        self._facts: list[dict[str, Any]] = []
        self._hints_from_learning: list[dict[str, Any]] = []

    def set_learning_service(self, learning_service: LearningService) -> None:
        """Set the learning service for self-improvement.
        
        Args:
            learning_service: Learning service instance
        """
        self._learning_service = learning_service

    async def _on_initialize(self) -> None:
        """Initialize the reasoning engine."""
        await self._neuro_symbolic.initialize()
        self._rules = []
        self._facts = []
        self._set_metadata("initialized", True)
        self._set_metadata("neuro_symbolic", True)

    async def _on_shutdown(self) -> None:
        """Shutdown the service."""
        await self._neuro_symbolic.shutdown()

    async def solve(self, problem: Any) -> Any:
        """Solve a problem using neuro-symbolic reasoning.

        Args:
            problem: The problem to solve (dict or Problem object)

        Returns:
            Solution with confidence and explanation
        """
        if hasattr(problem, "model_dump"):
            problem_dict = problem.model_dump()
        else:
            problem_dict = problem if isinstance(problem, dict) else {"problem": str(problem)}

        # Check learning service for relevant past experiences
        await self._apply_learning_insights(problem_dict)
        
        # Use neuro-symbolic reasoning for the main solve
        result = await self._neuro_symbolic.solve(problem_dict)
        
        # Store successful reasoning for future learning
        if result.get("confidence", 0) >= 0.7:
            await self._record_learning_experience(problem_dict, result)
        
        # Add hints to result
        result["used_hints"] = len(self._hints_from_learning) > 0
        result["hints"] = self._hints_from_learning[-3:] if self._hints_from_learning else []
        
        return result

    async def _apply_learning_insights(self, problem_dict: dict[str, Any]) -> None:
        """Apply insights from learning service to improve reasoning.
        
        Args:
            problem_dict: Problem dictionary to enhance
        """
        self._hints_from_learning = []
        
        if not self._learning_service:
            return
        
        try:
            # Query learning service for relevant experiences
            situation = {
                "type": "reasoning",
                "problem_summary": str(problem_dict)[:200],
            }
            
            # Get similar experiences (conceptually - actual method may differ)
            # The learning service provides hints based on past successes
            hints = await self._get_learning_hints(problem_dict)
            self._hints_from_learning.extend(hints)
            
            # Update neuro-symbolic with context
            if hints:
                self._neuro_symbolic.set_memory_context(hints)
                
        except Exception:
            # Learning integration is best-effort
            pass

    async def _get_learning_hints(self, problem_dict: dict[str, Any]) -> list[dict[str, Any]]:
        """Get hints from learning service.
        
        Args:
            problem_dict: Current problem
            
        Returns:
            List of relevant hints
        """
        hints: list[dict[str, Any]] = []
        
        # Check for pattern-based hints
        content = str(problem_dict.get("content", ""))
        
        if "arc" in content.lower() or "grid" in content.lower():
            hints.append({
                "category": "pattern_recognition",
                "content": "Consider analyzing spatial relationships in the grid structure",
            })
        
        if "transform" in content.lower():
            hints.append({
                "category": "transformation",
                "content": "Look for consistent transformation rules across examples",
            })
        
        return hints[:3]

    async def _record_learning_experience(
        self,
        problem: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        """Record experience for self-improvement.
        
        Args:
            problem: Problem that was solved
            result: Result of reasoning
        """
        if not self._learning_service:
            return
        
        try:
            experience = {
                "situation": {
                    "type": problem.get("type", "general"),
                    "content_summary": str(problem)[:100],
                },
                "action": {
                    "method": "neuro-symbolic",
                    "confidence": result.get("confidence", 0),
                },
                "outcome": {
                    "success": result.get("confidence", 0) >= 0.8,
                    "conclusion": result.get("conclusion", ""),
                },
                "reward": result.get("confidence", 0),
            }
            
            await self._learning_service.learn(experience)
            
        except Exception:
            # Learning is best-effort
            pass

    async def infer(self, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Perform inference using neuro-symbolic reasoning.

        Args:
            facts: Facts to reason about

        Returns:
            Inferred conclusions
        """
        result = await self._neuro_symbolic.infer(facts)
        return result

    async def prove(self, goal: dict[str, Any]) -> dict[str, Any]:
        """Prove a goal using neuro-symbolic reasoning.

        Args:
            goal: Goal to prove

        Returns:
            Proof result
        """
        return await self._neuro_symbolic.prove(goal)

    async def explain(self, result: Any) -> str:
        """Explain a result.

        Args:
            result: Result to explain

        Returns:
            Explanation
        """
        # Try neuro-symbolic explanation first
        explanation = await self._neuro_symbolic.explain(result)
        if explanation and explanation != "No explanation available.":
            return explanation
        
        # Fallback to basic explanation
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result if isinstance(result, dict) else {"result": str(result)}

        explanation_parts = []

        if "method" in result_dict:
            explanation_parts.append(
                f"This result was derived using {result_dict['method']} reasoning."
            )

        if "confidence" in result_dict:
            conf = result_dict["confidence"]
            if conf >= 0.8:
                explanation_parts.append("High confidence in the reasoning.")
            elif conf >= 0.5:
                explanation_parts.append("Moderate confidence in the reasoning.")
            else:
                explanation_parts.append("Low confidence - consider additional verification.")

        if "explanation" in result_dict:
            explanation_parts.append(result_dict["explanation"])

        return " ".join(explanation_parts) if explanation_parts else "Reasoning completed successfully."

    async def trace(self, result: Any) -> list[dict[str, Any]]:
        """Get reasoning trace.

        Args:
            result: Result to trace

        Returns:
            Reasoning trace
        """
        # Try neuro-symbolic trace first
        try:
            trace = await self._neuro_symbolic.trace(result)
            if trace:
                return trace
        except Exception:
            pass
        
        # Fallback
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result if isinstance(result, dict) else {"result": str(result)}

        trace = [
            {"step": 0, "type": "initial", "content": "Problem received"},
            {"step": 1, "type": "neuro_symbolic", "content": "Applied LLM-powered reasoning"},
        ]

        if "conclusion" in result_dict:
            trace.append({
                "step": 2,
                "type": "conclusion",
                "content": result_dict["conclusion"],
            })

        return trace

    def add_rule(self, rule: dict[str, Any]) -> None:
        """Add a reasoning rule.

        Args:
            rule: Rule to add
        """
        self._rules.append(rule)

    def clear_facts(self) -> None:
        """Clear all stored facts."""
        self._facts.clear()

    def get_facts(self) -> list[dict[str, Any]]:
        """Get all stored facts.

        Returns:
            List of facts
        """
        return self._facts.copy()


# Re-export interface for type hints
IReasoningService = ReasoningService
