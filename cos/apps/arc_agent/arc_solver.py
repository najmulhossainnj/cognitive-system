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
        await self._reflect_on_solution(solution)

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
        elif rule_type == "rotate":
            return self._rotate(grid, rule.parameters.get("degrees", 90))
        elif rule_type == "mirror":
            return self._mirror(grid, rule.parameters.get("axis", "horizontal"))
        elif rule_type == "extract_pattern":
            return self._extract_pattern(grid, rule.parameters)
        elif rule_type == "overlay":
            return self._overlay(grid, rule.parameters)
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
        """Duplicate grid content by mirroring.

        Args:
            grid: Input grid

        Returns:
            Duplicated/mirrored grid
        """
        if not grid:
            return []
        return [row + row[::-1] for row in grid]

    def _delete(self, grid: list[list[int]]) -> list[list[int]]:
        """Delete specific objects/colors from grid.

        Args:
            grid: Input grid

        Returns:
            Grid with objects removed (set to background 0)
        """
        if not grid:
            return []
        
        # Find the most common non-zero color and keep only that
        color_counts: dict[int, int] = {}
        for row in grid:
            for cell in row:
                if cell != 0:
                    color_counts[cell] = color_counts.get(cell, 0) + 1
        
        if not color_counts:
            return [row[:] for row in grid]
        
        # Keep the most common non-zero color
        target_color = max(color_counts, key=color_counts.get)
        
        result = []
        for row in grid:
            new_row = [target_color if cell == target_color else 0 for cell in row]
            result.append(new_row)
        
        return result

    def _move_to_corner(self, grid: list[list[int]]) -> list[list[int]]:
        """Move non-background objects to top-left corner.

        Args:
            grid: Input grid

        Returns:
            Grid with objects in top-left corner
        """
        if not grid:
            return []
        
        height = len(grid)
        width = len(grid[0])
        
        # Extract non-background cells
        objects: list[tuple[int, int, int]] = []  # (row, col, color)
        for r in range(height):
            for c in range(width):
                if grid[r][c] != 0:
                    objects.append((r, c, grid[r][c]))
        
        if not objects:
            return [row[:] for row in grid]
        
        # Find bounding box of objects
        min_r = min(r for r, c, color in objects)
        max_r = max(r for r, c, color in objects)
        min_c = min(c for r, c, color in objects)
        max_c = max(c for r, c, color in objects)
        
        bbox_height = max_r - min_r + 1
        bbox_width = max_c - min_c + 1
        
        # Create output grid with objects moved to corner
        result = [[0] * width for _ in range(height)]
        for r, c, color in objects:
            new_r = r - min_r
            new_c = c - min_c
            if 0 <= new_r < height and 0 <= new_c < width:
                result[new_r][new_c] = color
        
        return result

    def _move_to_center(self, grid: list[list[int]]) -> list[list[int]]:
        """Move non-background objects to center of grid.

        Args:
            grid: Input grid

        Returns:
            Grid with objects centered
        """
        if not grid:
            return []
        
        height = len(grid)
        width = len(grid[0])
        
        # Extract non-background cells with relative positions
        objects: list[tuple[int, int, int]] = []
        for r in range(height):
            for c in range(width):
                if grid[r][c] != 0:
                    objects.append((r, c, grid[r][c]))
        
        if not objects:
            return [row[:] for row in grid]
        
        # Find bounding box
        min_r = min(r for r, c, color in objects)
        max_r = max(r for r, c, color in objects)
        min_c = min(c for r, c, color in objects)
        max_c = max(c for r, c, color in objects)
        
        bbox_height = max_r - min_r + 1
        bbox_width = max_c - min_c + 1
        
        # Calculate offset to center
        offset_r = (height - bbox_height) // 2 - min_r
        offset_c = (width - bbox_width) // 2 - min_c
        
        # Create output grid
        result = [[0] * width for _ in range(height)]
        for r, c, color in objects:
            new_r = r + offset_r
            new_c = c + offset_c
            if 0 <= new_r < height and 0 <= new_c < width:
                result[new_r][new_c] = color
        
        return result

    def _color_change(
        self,
        grid: list[list[int]],
        parameters: dict[str, Any],
    ) -> list[list[int]]:
        """Change colors in grid based on pattern.

        Args:
            grid: Input grid
            parameters: Color change parameters

        Returns:
            Modified grid
        """
        added_colors = parameters.get("added_colors", [])
        removed_colors = parameters.get("removed_colors", [])
        
        if not added_colors and not removed_colors:
            return [row[:] for row in grid]
        
        result = []
        for row in grid:
            new_row = []
            for cell in row:
                if removed_colors and cell in removed_colors:
                    new_row.append(added_colors[0] if added_colors else 0)
                else:
                    new_row.append(cell)
            result.append(new_row)
        
        return result

    def _remove_background(self, grid: list[list[int]]) -> list[list[int]]:
        """Extract and crop non-background region.

        Args:
            grid: Input grid

        Returns:
            Cropped grid containing only non-background content
        """
        if not grid:
            return []
        
        height = len(grid)
        width = len(grid[0])
        
        # Find bounding box of non-zero cells
        min_r, max_r, min_c, max_c = height, -1, width, -1
        for r in range(height):
            for c in range(width):
                if grid[r][c] != 0:
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
        
        if max_r == -1:  # All background
            return [[0]]
        
        # Extract the region
        return [
            [grid[r][c] for c in range(min_c, max_c + 1)]
            for r in range(min_r, max_r + 1)
        ]

    def _rotate(self, grid: list[list[int]], degrees: int = 90) -> list[list[int]]:
        """Rotate grid by specified degrees.

        Args:
            grid: Input grid
            degrees: Rotation degrees (90, 180, 270)

        Returns:
            Rotated grid
        """
        if not grid:
            return []
        
        degrees = degrees % 360
        if degrees == 0:
            return [row[:] for row in grid]
        elif degrees == 180:
            return [row[::-1] for row in grid[::-1]]
        elif degrees == 90:
            height = len(grid)
            width = len(grid[0]) if grid else 0
            return [[grid[r][c] for r in range(height)] for c in range(width - 1, -1, -1)]
        elif degrees == 270:
            height = len(grid)
            width = len(grid[0]) if grid else 0
            return [[grid[r][c] for r in range(height - 1, -1, -1)] for c in range(width)]
        
        return [row[:] for row in grid]

    def _mirror(self, grid: list[list[int]], axis: str = "horizontal") -> list[list[int]]:
        """Mirror grid along axis.

        Args:
            grid: Input grid
            axis: 'horizontal' or 'vertical'

        Returns:
            Mirrored grid
        """
        if not grid:
            return []
        
        if axis == "horizontal":
            return [row[::-1] for row in grid]
        elif axis == "vertical":
            return grid[::-1]
        elif axis == "both":
            return [row[::-1] for row in grid[::-1]]
        
        return [row[:] for row in grid]

    def _extract_pattern(self, grid: list[list[int]], parameters: dict[str, Any]) -> list[list[int]]:
        """Extract a specific pattern from the grid.

        Args:
            grid: Input grid
            parameters: Extraction parameters

        Returns:
            Extracted pattern
        """
        # Get pattern type from parameters
        pattern_type = parameters.get("type", "bounding_box")
        
        if pattern_type == "bounding_box":
            return self._remove_background(grid)
        elif pattern_type == "color_region":
            target_color = parameters.get("color", 1)
            return self._extract_color_region(grid, target_color)
        
        return [row[:] for row in grid]

    def _extract_color_region(self, grid: list[list[int]], target_color: int) -> list[list[int]]:
        """Extract region of specific color.

        Args:
            grid: Input grid
            target_color: Color to extract

        Returns:
            Grid with only target color, others set to 0
        """
        if not grid:
            return []
        
        height = len(grid)
        width = len(grid[0])
        
        # Find bounding box of target color
        min_r, max_r, min_c, max_c = height, -1, width, -1
        for r in range(height):
            for c in range(width):
                if grid[r][c] == target_color:
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
        
        if max_r == -1:
            return [[0]]
        
        # Create output with target color isolated
        result = []
        for r in range(min_r, max_r + 1):
            row = []
            for c in range(min_c, max_c + 1):
                row.append(grid[r][c] if grid[r][c] == target_color else 0)
            result.append(row)
        
        return result

    def _overlay(self, grid: list[list[int]], parameters: dict[str, Any]) -> list[list[int]]:
        """Overlay pattern on grid.

        Args:
            grid: Input grid
            parameters: Overlay parameters

        Returns:
            Grid with overlay applied
        """
        overlay_pattern = parameters.get("pattern", [])
        position = parameters.get("position", (0, 0))
        
        if not overlay_pattern:
            return [row[:] for row in grid]
        
        result = [row[:] for row in grid]
        start_r, start_c = position
        
        for r, row in enumerate(overlay_pattern):
            for c, color in enumerate(row):
                if color != 0:
                    new_r = start_r + r
                    new_c = start_c + c
                    if 0 <= new_r < len(result) and 0 <= new_c < len(result[0]):
                        result[new_r][new_c] = color
        
        return result

    async def _reflect_on_solution(self, solution: Any) -> None:
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
