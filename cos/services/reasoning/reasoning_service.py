"""Reasoning Service Implementation.

This module provides the Reasoning Service for cognitive reasoning operations.
"""

from __future__ import annotations

from typing import Any

from cos.services.base import ServiceBase


class ReasoningService(ServiceBase):
    """Reasoning Service for cognitive reasoning operations.

    This service provides various reasoning capabilities:
    - Problem solving
    - Logical inference
    - Goal proving
    - Result explanation
    - Reasoning traces
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
        self._set_metadata("reasoning_type", "general")
        self._rules: list[dict[str, Any]] = []
        self._facts: list[dict[str, Any]] = []

    async def _on_initialize(self) -> None:
        """Initialize the reasoning engine."""
        self._rules = []
        self._facts = []
        self._set_metadata("initialized", True)

    async def solve(self, problem: Any) -> Any:
        """Solve a problem.

        Args:
            problem: The problem to solve (dict or Problem object)

        Returns:
            Solution
        """
        if hasattr(problem, "model_dump"):
            problem_dict = problem.model_dump()
        else:
            problem_dict = problem if isinstance(problem, dict) else {"problem": str(problem)}

        solution = {
            "status": "solved",
            "problem": problem_dict.get("problem", problem_dict),
            "method": "general_reasoning",
            "confidence": 0.8,
        }

        if "type" in problem_dict:
            if problem_dict["type"] == "deduction":
                solution["result"] = self._apply_deduction(problem_dict)
            elif problem_dict["type"] == "induction":
                solution["result"] = self._apply_induction(problem_dict)
            elif problem_dict["type"] == "abduction":
                solution["result"] = self._apply_abduction(problem_dict)
            else:
                solution["result"] = self._general_reasoning(problem_dict)

        return solution

    def _apply_deduction(self, problem: dict[str, Any]) -> Any:
        """Apply deductive reasoning.

        Args:
            problem: Problem definition

        Returns:
            Deduced result
        """
        premises = problem.get("premises", [])
        conclusion = problem.get("conclusion", {})

        valid = True
        for premise in premises:
            if premise not in self._facts:
                self._facts.append(premise)

        return {
            "type": "deduction",
            "premises": premises,
            "conclusion": conclusion,
            "valid": valid,
            "confidence": 0.95 if valid else 0.5,
        }

    def _apply_induction(self, problem: dict[str, Any]) -> Any:
        """Apply inductive reasoning.

        Args:
            problem: Problem definition

        Returns:
            Induced hypothesis
        """
        observations = problem.get("observations", [])

        hypothesis = {
            "type": "induction",
            "observations": observations,
            "generalization": "Based on " + str(len(observations)) + " observations",
            "confidence": 0.7,
        }

        return hypothesis

    def _apply_abduction(self, problem: dict[str, Any]) -> Any:
        """Apply abductive reasoning.

        Args:
            problem: Problem definition

        Returns:
            Abduced explanation
        """
        observation = problem.get("observation", {})

        explanation = {
            "type": "abduction",
            "observation": observation,
            "possible_explanations": [],
            "best_explanation": None,
            "confidence": 0.6,
        }

        return explanation

    def _general_reasoning(self, problem: dict[str, Any]) -> Any:
        """Apply general reasoning.

        Args:
            problem: Problem definition

        Returns:
            Reasoning result
        """
        return {
            "type": "general",
            "problem": problem,
            "steps": [],
            "confidence": 0.75,
        }

    async def infer(self, facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Perform inference.

        Args:
            facts: Facts to reason about

        Returns:
            Inferred conclusions
        """
        conclusions = []

        for fact in facts:
            if "rule" in fact:
                conclusion = self._apply_rule(fact)
                if conclusion:
                    conclusions.append(conclusion)
            else:
                self._facts.append(fact)
                conclusions.append({"fact": fact, "derived": False})

        return conclusions

    def _apply_rule(self, fact: dict[str, Any]) -> dict[str, Any] | None:
        """Apply a reasoning rule.

        Args:
            fact: Fact with rule

        Returns:
            Rule application result
        """
        rule = fact.get("rule", {})
        premises = rule.get("premises", [])
        conclusion = rule.get("conclusion", {})

        if all(p in self._facts for p in premises):
            self._facts.append(conclusion)
            return {
                "rule_applied": rule,
                "premises_matched": premises,
                "conclusion": conclusion,
                "derived": True,
            }

        return None

    async def prove(self, goal: dict[str, Any]) -> dict[str, Any]:
        """Prove a goal.

        Args:
            goal: Goal to prove

        Returns:
            Proof result
        """
        goal_str = goal.get("goal", goal)

        proof = {
            "goal": goal_str,
            "proved": False,
            "method": "direct_proof",
            "steps": [],
            "confidence": 0.0,
        }

        if goal_str in [f.get("goal", f) if isinstance(f, dict) else f for f in self._facts]:
            proof["proved"] = True
            proof["confidence"] = 1.0
            proof["steps"].append({"type": "fact", "content": goal_str})
        else:
            for fact in self._facts:
                if self._matches_goal(fact, goal_str):
                    proof["proved"] = True
                    proof["confidence"] = 0.9
                    proof["steps"].append({"type": "derived", "content": fact})
                    break

        return proof

    def _matches_goal(self, fact: dict[str, Any], goal: str) -> bool:
        """Check if a fact matches a goal.

        Args:
            fact: Fact to check
            goal: Goal to match

        Returns:
            True if matches
        """
        if isinstance(fact, dict):
            return any(str(v) == goal for v in fact.values())
        return str(fact) == goal

    async def explain(self, result: Any) -> str:
        """Explain a result.

        Args:
            result: Result to explain

        Returns:
            Explanation
        """
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result if isinstance(result, dict) else {"result": str(result)}

        explanation_parts = []

        if "method" in result_dict:
            explanation_parts.append(
                f"This result was derived using {result_dict['method']} reasoning."
            )

        if "steps" in result_dict:
            steps_count = len(result_dict["steps"])
            explanation_parts.append(
                f"The reasoning process involved {steps_count} step(s)."
            )

        if "confidence" in result_dict:
            conf = result_dict["confidence"]
            if conf >= 0.9:
                explanation_parts.append("The confidence in this result is very high.")
            elif conf >= 0.7:
                explanation_parts.append("The confidence is moderate to high.")
            else:
                explanation_parts.append("The confidence in this result is moderate.")

        return " ".join(explanation_parts) if explanation_parts else "No explanation available."

    async def trace(self, result: Any) -> list[dict[str, Any]]:
        """Get reasoning trace.

        Args:
            result: Result to trace

        Returns:
            Reasoning trace
        """
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result if isinstance(result, dict) else {"result": str(result)}

        trace = [
            {"step": 0, "type": "initial", "content": "Problem received"},
        ]

        if "steps" in result_dict:
            for i, step in enumerate(result_dict["steps"]):
                trace.append({"step": i + 1, "type": "reasoning", "content": step})

        trace.append({
            "step": len(trace),
            "type": "final",
            "content": result_dict,
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
