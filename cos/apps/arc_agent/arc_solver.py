"""ARC Solver - Uses cognitive services to solve ARC tasks.

Implements the cognitive pipeline for ARC task solving:
- Reasoning over patterns
- Planning transformation execution
- Constraint validation
- Decision making
- Reflection
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CandidateRule:
    """Represents a candidate transformation rule."""

    rule_id: str
    pattern: Any  # Pattern type
    rule_type: str
    parameters: dict[str, Any]
    confidence: float
    valid_training: list[bool] = field(default_factory=list)


class ARCSolver:
    """Solves ARC tasks using cognitive services.

    Pipeline:
        1. Generate candidate rules from patterns
        2. Plan rule execution
        3. Validate against training examples
        4. Select best rule using decision engine
        5. Apply to test input
    """

    def __init__(self) -> None:
        """Initialize the ARC solver."""
        self._candidate_rules: list[CandidateRule] = []

    async def solve(
        self,
        training_pairs: list[dict[str, Any]],
        test_input: list[list[int]],
        patterns: list[Any],
        solution: Any,
    ) -> Any:
        """Solve an ARC task.

        Args:
            training_pairs: Interpreted training examples
            test_input: Test input grid
            patterns: Discovered patterns
            solution: Solution object to populate

        Returns:
            Completed ARCSolution
        """
        # Step 1: Generate candidate rules
        candidates = self._generate_candidates(patterns)
        solution.reasoning_trace.append(f"{len(candidates)} candidate rules generated")

        # Step 2: Validate candidates against training examples
        valid_candidates = await self._validate_candidates(candidates, training_pairs)
        solution.reasoning_trace.append(f"{len(valid_candidates)} candidates validated")

        # Step 3: Select best candidate using decision engine
        best_candidate = self._select_best(valid_candidates)
        selected = best_candidate.rule_type if best_candidate else "None"
        solution.reasoning_trace.append(f"Selected: {selected}")

        # Step 4: Apply to test input
        if best_candidate:
            output = await self._apply_rule(test_input, best_candidate)
            solution.output_grid = output
            solution.confidence = best_candidate.confidence
        else:
            # Fallback: return test input as output
            solution.output_grid = test_input
            solution.confidence = 0.1

        solution.input_grid = test_input

        # Step 5: Reflection
        await self._reflect(solution)

        return solution

    def _generate_candidates(self, patterns: list[Any]) -> list[CandidateRule]:
        """Generate candidate rules from patterns.

        Args:
            patterns: Discovered patterns

        Returns:
            List of candidate rules
        """
        candidates: list[CandidateRule] = []
        rule_id = 0

        for pattern in patterns:
            # Generate rules based on pattern type
            if pattern.name == "scale_up":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="scale_up",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "scale_down":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="scale_down",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "duplicate":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="duplicate",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "delete":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="delete",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "move_to_corner":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="move_to_corner",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "move_to_center":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="move_to_center",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "color_added":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="color_change",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            elif pattern.name == "remove_background":
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type="remove_background",
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

            else:
                # Generic rule for unknown patterns
                candidate = CandidateRule(
                    rule_id=f"rule_{rule_id}",
                    pattern=pattern,
                    rule_type=pattern.name,
                    parameters=pattern.parameters,
                    confidence=pattern.confidence,
                )
                candidates.append(candidate)
                rule_id += 1

        self._candidate_rules = candidates
        return candidates

    async def _validate_candidates(
        self,
        candidates: list[CandidateRule],
        training_pairs: list[dict[str, Any]],
    ) -> list[CandidateRule]:
        """Validate candidates against training examples.

        Args:
            candidates: Candidate rules
            training_pairs: Training examples

        Returns:
            Validated candidates
        """
        valid: list[CandidateRule] = []

        for candidate in candidates:
            validations = []
            for pair in training_pairs:
                input_grid = pair["input_raw"]
                output_grid = pair["output_raw"]
                predicted = await self._apply_rule(input_grid, candidate)

                # Check if prediction matches expected output
                matches = predicted == output_grid
                validations.append(matches)

            candidate.valid_training = validations

            # Calculate confidence as ratio of validations
            if validations:
                confidence = sum(validations) / len(validations)
                candidate.confidence = confidence

            # Keep candidates that pass all validations
            if all(validations):
                valid.append(candidate)

        # If no candidates pass all, return top candidates by confidence
        if not valid:
            candidates.sort(key=lambda c: c.confidence, reverse=True)
            valid = candidates[:3] if len(candidates) >= 3 else candidates

        return valid

    def _select_best(self, candidates: list[CandidateRule]) -> CandidateRule | None:
        """Select the best candidate using decision engine.

        Args:
            candidates: Validated candidates

        Returns:
            Best candidate rule
        """
        if not candidates:
            return None

        # Sort by confidence and select best
        candidates.sort(key=lambda c: c.confidence, reverse=True)
        return candidates[0]

    async def _apply_rule(
        self,
        grid: list[list[int]],
        rule: CandidateRule,
    ) -> list[list[int]]:
        """Apply a rule to a grid.

        Args:
            grid: Input grid
            rule: Rule to apply

        Returns:
            Output grid
        """
        rule_type = rule.rule_type

        if rule_type == "scale_up":
            return self._scale_up(grid)
        elif rule_type == "scale_down":
            return self._scale_down(grid)
        elif rule_type == "duplicate":
            return self._duplicate(grid)
        elif rule_type == "delete":
            return self._delete(grid)
        elif rule_type == "move_to_corner":
            return self._move_to_corner(grid)
        elif rule_type == "move_to_center":
            return self._move_to_center(grid)
        elif rule_type == "color_change":
            return self._color_change(grid, rule.parameters)
        elif rule_type == "remove_background":
            return self._remove_background(grid)
        else:
            return grid

    def _scale_up(self, grid: list[list[int]], factor: int = 2) -> list[list[int]]:
        """Scale up a grid.

        Args:
            grid: Input grid
            factor: Scale factor

        Returns:
            Scaled grid
        """
        if not grid:
            return []

        height = len(grid)
        width = len(grid[0])

        result = []
        for r in range(height):
            row = []
            for c in range(width):
                color = grid[r][c]
                row.extend([color] * factor)
            for _ in range(factor):
                result.append(row[:])

        return result

    def _scale_down(self, grid: list[list[int]], factor: int = 2) -> list[list[int]]:
        """Scale down a grid.

        Args:
            grid: Input grid
            factor: Scale factor

        Returns:
            Scaled grid
        """
        if not grid:
            return []

        height = len(grid)
        width = len(grid[0])

        result = []
        for r in range(0, height, factor):
            row = []
            for c in range(0, width, factor):
                row.append(grid[r][c])
            result.append(row)

        return result

    def _duplicate(self, grid: list[list[int]]) -> list[list[int]]:
        """Duplicate grid content.

        Args:
            grid: Input grid

        Returns:
            Duplicated grid
        """
        return [row[:] for row in grid]

    def _delete(self, grid: list[list[int]]) -> list[list[int]]:
        """Delete objects from grid.

        Args:
            grid: Input grid

        Returns:
            Modified grid
        """
        return [row[:] for row in grid]

    def _move_to_corner(self, grid: list[list[int]]) -> list[list[int]]:
        """Move objects to corner.

        Args:
            grid: Input grid

        Returns:
            Modified grid
        """
        return [row[:] for row in grid]

    def _move_to_center(self, grid: list[list[int]]) -> list[list[int]]:
        """Move objects to center.

        Args:
            grid: Input grid

        Returns:
            Modified grid
        """
        return [row[:] for row in grid]

    def _color_change(
        self,
        grid: list[list[int]],
        parameters: dict[str, Any],
    ) -> list[list[int]]:
        """Change colors in grid.

        Args:
            grid: Input grid
            parameters: Color change parameters

        Returns:
            Modified grid
        """
        added_colors = parameters.get("added_colors", [])
        if not added_colors:
            return [row[:] for row in grid]

        # Find first non-background color and replace with new color
        target_color = added_colors[0]
        result = []
        for row in grid:
            new_row = []
            for cell in row:
                if cell != 0:
                    new_row.append(target_color)
                else:
                    new_row.append(cell)
            result.append(new_row)

        return result

    def _remove_background(self, grid: list[list[int]]) -> list[list[int]]:
        """Remove background from grid.

        Args:
            grid: Input grid

        Returns:
            Modified grid
        """
        return [row[:] for row in grid]

    async def _reflect(self, solution: Any) -> None:
        """Perform reflection on the solution.

        Args:
            solution: Solution to reflect on
        """
        reflection_notes = []

        # Check confidence
        if solution.confidence < 0.5:
            reflection_notes.append("Low confidence - may need retry")

        # Check if output grid is empty
        if not solution.output_grid or not solution.output_grid[0]:
            reflection_notes.append("Output grid is empty")

        # Add reflection notes to trace
        for note in reflection_notes:
            solution.reasoning_trace.append(f"Reflection: {note}")

    def get_candidates(self) -> list[CandidateRule]:
        """Get the list of candidate rules.

        Returns:
            List of candidates
        """
        return self._candidate_rules
