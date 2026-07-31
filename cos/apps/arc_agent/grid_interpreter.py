"""Grid Interpreter - Perception service for ARC grids.

Converts raw grid data into symbolic representations including
objects, colors, shapes, and relationships.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any


@dataclass
class GridSymbolic:
    """Symbolic representation of a grid."""

    id: str
    width: int
    height: int
    colors: dict[int, int]
    objects: list[dict[str, Any]]
    bounding_boxes: dict[str, tuple[int, int, int, int]]
    connected_components: list[list[tuple[int, int]]]
    shapes: list[str]
    symmetry: dict[str, bool]
    coordinates: dict[tuple[int, int], int]


@dataclass
class Transformation:
    """Represents a detected transformation."""

    type: str
    parameters: dict[str, Any]
    description: str


class GridInterpreter:
    """Interprets ARC grids into symbolic representations.

    Performs perception tasks:
    - Object detection
    - Color analysis
    - Shape recognition
    - Bounding box calculation
    - Connected component analysis
    - Symmetry detection
    """

    def __init__(self) -> None:
        """Initialize the grid interpreter."""
        self._shape_patterns = self._init_shape_patterns()

    async def interpret(self, grid_pair: dict[str, Any]) -> dict[str, Any]:
        """Interpret an input/output grid pair.

        Args:
            grid_pair: Dict with 'input' and 'output' grids

        Returns:
            Symbolic interpretation
        """
        input_grid = grid_pair.get("input", [])
        output_grid = grid_pair.get("output", [])

        input_symbolic = await self.interpret_grid(input_grid, "input")
        output_symbolic = await self.interpret_grid(output_grid, "output")

        return {
            "input_symbolic": input_symbolic,
            "output_symbolic": output_symbolic,
            "input_raw": input_grid,
            "output_raw": output_grid,
        }

    async def interpret_grid(self, grid: list[list[int]], grid_id: str) -> GridSymbolic:
        """Interpret a single grid.

        Args:
            grid: 2D grid of colors
            grid_id: Identifier for the grid

        Returns:
            Symbolic representation
        """
        if not grid:
            return GridSymbolic(
                id=grid_id,
                width=0,
                height=0,
                colors={},
                objects=[],
                bounding_boxes={},
                connected_components=[],
                shapes=[],
                symmetry={},
                coordinates={},
            )

        height = len(grid)
        width = len(grid[0]) if grid[0] else 0

        colors = self._count_colors(grid)
        coordinates = self._get_coordinates(grid)
        connected_components = self._find_connected_components(grid)
        objects = self._extract_objects(grid, connected_components)
        bounding_boxes = self._calculate_bounding_boxes(objects)
        shapes = self._recognize_shapes(objects)
        symmetry = self._detect_symmetry(grid)

        return GridSymbolic(
            id=grid_id,
            width=width,
            height=height,
            colors=colors,
            objects=objects,
            bounding_boxes=bounding_boxes,
            connected_components=connected_components,
            shapes=shapes,
            symmetry=symmetry,
            coordinates=coordinates,
        )

    def _count_colors(self, grid: list[list[int]]) -> dict[int, int]:
        """Count occurrences of each color.

        Args:
            grid: Input grid

        Returns:
            Dict mapping color to count
        """
        counts: dict[int, int] = defaultdict(int)
        for row in grid:
            for cell in row:
                counts[cell] += 1
        return dict(counts)

    def _get_coordinates(self, grid: list[list[int]]) -> dict[tuple[int, int], int]:
        """Get coordinate mapping.

        Args:
            grid: Input grid

        Returns:
            Dict mapping (row, col) to color
        """
        coords = {}
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                coords[(r, c)] = cell
        return coords

    def _find_connected_components(
        self,
        grid: list[list[int]],
        background_color: int = 0,
    ) -> list[list[tuple[int, int]]]:
        """Find connected components using BFS.

        Args:
            grid: Input grid
            background_color: Color considered as background

        Returns:
            List of connected components
        """
        if not grid:
            return []

        height = len(grid)
        width = len(grid[0]) if grid[0] else 0
        visited: set[tuple[int, int]] = set()
        components: list[list[tuple[int, int]]] = []

        for r in range(height):
            for c in range(width):
                if (r, c) not in visited and grid[r][c] != background_color:
                    component = self._bfs_component(grid, r, c, visited)
                    if component:
                        components.append(component)

        return components

    def _bfs_component(
        self,
        grid: list[list[int]],
        start_r: int,
        start_c: int,
        visited: set[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        """BFS to find a connected component.

        Args:
            grid: Input grid
            start_r: Starting row
            start_c: Starting column
            visited: Set of visited coordinates

        Returns:
            List of coordinates in the component
        """
        height = len(grid)
        width = len(grid[0]) if grid[0] else 0
        target_color = grid[start_r][start_c]
        component: list[tuple[int, int]] = []
        queue = [(start_r, start_c)]

        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited:
                continue
            if r < 0 or r >= height or c < 0 or c >= width:
                continue
            if grid[r][c] != target_color:
                continue

            visited.add((r, c))
            component.append((r, c))

            queue.extend([
                (r - 1, c), (r + 1, c),
                (r, c - 1), (r, c + 1),
            ])

        return component

    def _extract_objects(
        self,
        grid: list[list[int]],
        components: list[list[tuple[int, int]]],
    ) -> list[dict[str, Any]]:
        """Extract objects from connected components.

        Args:
            grid: Input grid
            components: Connected components

        Returns:
            List of object descriptions
        """
        objects = []
        for i, component in enumerate(components):
            if not component:
                continue

            min_r = min(r for r, c in component)
            max_r = max(r for r, c in component)
            min_c = min(c for r, c in component)
            max_c = max(c for r, c in component)

            color = grid[component[0][0]][component[0][1]]

            objects.append({
                "id": f"obj_{i}",
                "color": color,
                "cells": component,
                "size": len(component),
                "bbox": (min_r, min_c, max_r, max_c),
            })

        return objects

    def _calculate_bounding_boxes(
        self,
        objects: list[dict[str, Any]],
    ) -> dict[str, tuple[int, int, int, int]]:
        """Calculate bounding boxes for objects.

        Args:
            objects: List of objects

        Returns:
            Dict mapping object ID to bounding box
        """
        return {obj["id"]: obj["bbox"] for obj in objects}

    def _recognize_shapes(self, objects: list[dict[str, Any]]) -> list[str]:
        """Recognize shapes in objects.

        Args:
            objects: List of objects

        Returns:
            List of shape names
        """
        shapes = []
        for obj in objects:
            cells = obj["cells"]
            size = obj["size"]
            bbox = obj["bbox"]
            bbox_width = bbox[2] - bbox[0] + 1
            bbox_height = bbox[3] - bbox[1] + 1

            shape = self._classify_shape(cells, size, bbox_width, bbox_height)
            shapes.append(shape)

        return shapes

    def _classify_shape(
        self,
        cells: list[tuple[int, int]],
        size: int,
        width: int,
        height: int,
    ) -> str:
        """Classify the shape of an object.

        Args:
            cells: Object cells
            size: Number of cells
            width: Bounding box width
            height: Bounding box height

        Returns:
            Shape name
        """
        # Check if rectangle
        if size == width * height:
            if width == height:
                return "square"
            return "rectangle"

        # Check if line
        if size == width or size == height:
            if size > 1:
                return "line"

        # Check if L-shape
        if self._is_l_shape(cells):
            return "L_shape"

        # Check if T-shape
        if self._is_t_shape(cells):
            return "T_shape"

        # Check if plus/plus_sign
        if self._is_plus_shape(cells):
            return "plus_sign"

        # Default to general shape
        return "shape"

    def _is_l_shape(self, cells: list[tuple[int, int]]) -> bool:
        """Check if cells form an L shape."""
        min_r = min(r for r, c in cells)
        max_r = max(r for r, c in cells)
        min_c = min(c for r, c in cells)
        max_c = max(c for r, c in cells)

        corners = [
            (min_r, min_c), (min_r, max_c),
            (max_r, min_c), (max_r, max_c),
        ]

        for corner in corners:
            if corner in cells:
                arm1 = any(r == corner[0] for r, c in cells)
                arm2 = any(c == corner[1] for r, c in cells)
                if arm1 and arm2:
                    return True

        return False

    def _is_t_shape(self, cells: list[tuple[int, int]]) -> bool:
        """Check if cells form a T shape."""
        return False  # Simplified

    def _is_plus_shape(self, cells: list[tuple[int, int]]) -> bool:
        """Check if cells form a plus shape."""
        return False  # Simplified

    def _detect_symmetry(self, grid: list[list[int]]) -> dict[str, bool]:
        """Detect symmetries in the grid.

        Args:
            grid: Input grid

        Returns:
            Dict of symmetry types
        """
        horizontal = self._check_horizontal_symmetry(grid)
        vertical = self._check_vertical_symmetry(grid)
        diagonal = self._check_diagonal_symmetry(grid)

        return {
            "horizontal": horizontal,
            "vertical": vertical,
            "diagonal": diagonal,
            "rotational": horizontal and vertical,
        }

    def _check_horizontal_symmetry(self, grid: list[list[int]]) -> bool:
        """Check horizontal symmetry."""
        height = len(grid)
        if height < 2:
            return False

        for r in range(height // 2):
            if grid[r] != grid[height - 1 - r]:
                return False
        return True

    def _check_vertical_symmetry(self, grid: list[list[int]]) -> bool:
        """Check vertical symmetry."""
        if not grid or not grid[0]:
            return False
        width = len(grid[0])
        if width < 2:
            return False

        for row in grid:
            for c in range(width // 2):
                if row[c] != row[width - 1 - c]:
                    return False
        return True

    def _check_diagonal_symmetry(self, grid: list[list[int]]) -> bool:
        """Check diagonal symmetry."""
        return False  # Simplified

    def _init_shape_patterns(self) -> dict[str, Any]:
        """Initialize shape patterns.

        Returns:
            Dict of shape patterns
        """
        return {
            "square": [],
            "rectangle": [],
            "line": [],
            "L_shape": [],
            "T_shape": [],
            "plus_sign": [],
        }
