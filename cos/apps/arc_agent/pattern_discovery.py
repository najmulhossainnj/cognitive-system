"""Pattern Discovery Service for ARC tasks.

Discovers candidate transformation patterns from training examples.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from cos.apps.arc_agent.grid_interpreter import GridSymbolic


@dataclass
class Pattern:
    """Represents a discovered transformation pattern."""

    name: str
    description: str
    confidence: float = 0.5
    parameters: dict[str, Any] = field(default_factory=dict)
    applies_to_training: list[bool] = field(default_factory=list)


@dataclass
class TransformationRule:
    """Represents a transformation rule."""

    rule_type: str
    source: Any
    target: Any
    pattern: Pattern


class PatternDiscovery:
    """Discovers transformation patterns from ARC training examples.

    Detects patterns including:
    - Translation
    - Reflection
    - Rotation
    - Scaling
    - Mirror
    - Copy
    - Delete
    - Merge
    - Split
    - Repeat
    - Flood Fill
    - Symmetry
    """

    # Common ARC transformation types
    TRANSFORMATION_TYPES: ClassVar[list[str]] = [
        "translate",
        "reflect_horizontal",
        "reflect_vertical",
        "reflect_diagonal",
        "rotate_90",
        "rotate_180",
        "rotate_270",
        "scale_up",
        "scale_down",
        "mirror",
        "copy",
        "delete",
        "merge",
        "split",
        "repeat",
        "flood_fill",
        "color_change",
        "move_to_corner",
        "move_to_center",
        "duplicate",
        "remove_background",
        "overlay",
    ]

    def __init__(self) -> None:
        """Initialize pattern discovery."""
        self._discovered_patterns: list[Pattern] = []

    async def discover(
        self,
        training_pairs: list[dict[str, Any]],
    ) -> list[Pattern]:
        """Discover candidate transformation patterns.

        Args:
            training_pairs: List of interpreted training pairs

        Returns:
            List of candidate patterns
        """
        patterns: list[Pattern] = []

        # Analyze each training pair
        for pair in training_pairs:
            input_sym = pair["input_symbolic"]
            output_sym = pair["output_symbolic"]

            # Detect transformation patterns
            detected = self._analyze_transformation(input_sym, output_sym)
            patterns.extend(detected)

        # Validate patterns across all training examples
        validated = self._validate_patterns(patterns, training_pairs)

        self._discovered_patterns = validated
        return validated

    def _analyze_transformation(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> list[Pattern]:
        """Analyze transformation between input and output.

        Args:
            input_sym: Symbolic representation of input
            output_sym: Symbolic representation of output

        Returns:
            List of detected patterns
        """
        patterns: list[Pattern] = []

        # Check grid size changes
        size_pattern = self._check_size_change(input_sym, output_sym)
        if size_pattern:
            patterns.append(size_pattern)

        # Check color transformations
        color_patterns = self._check_color_change(input_sym, output_sym)
        patterns.extend(color_patterns)

        # Check object count changes
        object_pattern = self._check_object_count(input_sym, output_sym)
        if object_pattern:
            patterns.append(object_pattern)

        # Check position changes
        position_pattern = self._check_position_change(input_sym, output_sym)
        if position_pattern:
            patterns.append(position_pattern)

        # Check symmetry transformations
        symmetry_pattern = self._check_symmetry_change(input_sym, output_sym)
        if symmetry_pattern:
            patterns.append(symmetry_pattern)

        # Check background changes
        background_pattern = self._check_background_change(input_sym, output_sym)
        if background_pattern:
            patterns.append(background_pattern)

        return patterns

    def _check_size_change(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> Pattern | None:
        """Check for size/scale transformations.

        Args:
            input_sym: Input symbolic grid
            output_sym: Output symbolic grid

        Returns:
            Pattern if size change detected
        """
        if input_sym.width == output_sym.width and input_sym.height == output_sym.height:
            return None

        if output_sym.width > input_sym.width or output_sym.height > input_sym.height:
            return Pattern(
                name="scale_up",
                description="Grid scaled up",
                confidence=0.7,
                parameters={
                    "input_size": (input_sym.width, input_sym.height),
                    "output_size": (output_sym.width, output_sym.height),
                },
            )

        return Pattern(
            name="scale_down",
            description="Grid scaled down",
            confidence=0.7,
            parameters={
                "input_size": (input_sym.width, input_sym.height),
                "output_size": (output_sym.width, output_sym.height),
            },
        )

    def _check_color_change(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> list[Pattern]:
        """Check for color transformations.

        Args:
            input_sym: Input symbolic grid
            output_sym: Output symbolic grid

        Returns:
            List of color change patterns
        """
        patterns: list[Pattern] = []

        input_colors = set(input_sym.colors.keys())
        output_colors = set(output_sym.colors.keys())

        # Check if colors were added
        added_colors = output_colors - input_colors
        if added_colors:
            patterns.append(Pattern(
                name="color_added",
                description=f"Colors added: {added_colors}",
                confidence=0.6,
                parameters={"added_colors": list(added_colors)},
            ))

        # Check if colors were removed
        removed_colors = input_colors - output_colors
        if removed_colors:
            patterns.append(Pattern(
                name="color_removed",
                description=f"Colors removed: {removed_colors}",
                confidence=0.6,
                parameters={"removed_colors": list(removed_colors)},
            ))

        # Check for background change (color 0)
        if 0 in input_sym.colors and 0 not in output_sym.colors:
            patterns.append(Pattern(
                name="remove_background",
                description="Background color removed",
                confidence=0.8,
            ))

        return patterns

    def _check_object_count(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> Pattern | None:
        """Check for object count changes.

        Args:
            input_sym: Input symbolic grid
            output_sym: Output symbolic grid

        Returns:
            Pattern if object count change detected
        """
        input_count = len(input_sym.objects)
        output_count = len(output_sym.objects)

        if input_count == output_count:
            return None

        if output_count > input_count:
            return Pattern(
                name="duplicate",
                description=f"Objects duplicated: {input_count} -> {output_count}",
                confidence=0.7,
                parameters={
                    "input_count": input_count,
                    "output_count": output_count,
                    "duplication_factor": output_count / input_count if input_count > 0 else 1,
                },
            )

        return Pattern(
            name="delete",
            description=f"Objects removed: {input_count} -> {output_count}",
            confidence=0.7,
            parameters={
                "input_count": input_count,
                "output_count": output_count,
            },
        )

    def _check_position_change(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> Pattern | None:
        """Check for position transformations.

        Args:
            input_sym: Input symbolic grid
            output_sym: Output symbolic grid

        Returns:
            Pattern if position change detected
        """
        if not input_sym.objects or not output_sym.objects:
            return None

        # Check if objects moved to corners
        for obj in output_sym.objects:
            bbox = obj["bbox"]
            if bbox[0] == 0 or bbox[2] == output_sym.height - 1:
                if bbox[1] == 0 or bbox[3] == output_sym.width - 1:
                    return Pattern(
                        name="move_to_corner",
                        description="Object moved to corner",
                        confidence=0.7,
                    )

        # Check if objects moved to center
        center_r = output_sym.height // 2
        center_c = output_sym.width // 2
        for obj in output_sym.objects:
            bbox = obj["bbox"]
            if bbox[0] <= center_r <= bbox[2] and bbox[1] <= center_c <= bbox[3]:
                return Pattern(
                    name="move_to_center",
                    description="Object moved to center",
                    confidence=0.7,
                )

        return None

    def _check_symmetry_change(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> Pattern | None:
        """Check for symmetry transformations.

        Args:
            input_sym: Input symbolic grid
            output_sym: Output symbolic grid

        Returns:
            Pattern if symmetry change detected
        """
        for symmetry_type in ["horizontal", "vertical", "rotational"]:
            if not input_sym.symmetry.get(symmetry_type) and output_sym.symmetry.get(symmetry_type):
                return Pattern(
                    name=f"add_{symmetry_type}_symmetry",
                    description=f"Added {symmetry_type} symmetry",
                    confidence=0.8,
                )

        return None

    def _check_background_change(
        self,
        input_sym: GridSymbolic,
        output_sym: GridSymbolic,
    ) -> Pattern | None:
        """Check for background changes.

        Args:
            input_sym: Input symbolic grid
            output_sym: Output symbolic grid

        Returns:
            Pattern if background change detected
        """
        if input_sym.colors.get(0, 0) != output_sym.colors.get(0, 0):
            return Pattern(
                name="change_background",
                description="Background color changed",
                confidence=0.6,
                parameters={
                    "input_background": 0,
                    "output_background": 0,
                },
            )

        return None

    def _validate_patterns(
        self,
        patterns: list[Pattern],
        training_pairs: list[dict[str, Any]],
    ) -> list[Pattern]:
        """Validate patterns against all training examples.

        Args:
            patterns: Candidate patterns
            training_pairs: Training examples

        Returns:
            Validated patterns with confidence scores
        """
        validated: list[Pattern] = []

        for pattern in patterns:
            applies = []
            for pair in training_pairs:
                # Simple validation - check if pattern applies
                applies.append(self._pattern_applies(pattern, pair))

            # Calculate confidence based on how many examples it applies to
            if applies:
                confidence = sum(applies) / len(applies)
                pattern.confidence = confidence
                pattern.applies_to_training = applies

                if confidence >= 0.5:
                    validated.append(pattern)

        return validated

    def _pattern_applies(self, pattern: Pattern, pair: dict[str, Any]) -> bool:
        """Check if a pattern applies to a training pair.

        Args:
            pattern: Pattern to check
            pair: Training pair

        Returns:
            True if pattern applies
        """
        # Simplified validation logic
        return True

    def get_discovered_patterns(self) -> list[Pattern]:
        """Get the list of discovered patterns.

        Returns:
            List of patterns
        """
        return self._discovered_patterns
