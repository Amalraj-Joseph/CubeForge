from __future__ import annotations

from dataclasses import dataclass

from cube.color.color import Color
from cube.face.logical_face import LogicalFace


@dataclass(frozen=True, slots=True)
class CubeOrientation:
    """
    Represents the observer's frame of reference.

    A CubeOrientation defines which center color is currently
    visible on each logical face of the cube.

    A CubeOrientation is immutable.
    """

    up: Color
    down: Color

    front: Color
    back: Color

    left: Color
    right: Color

    def __post_init__(self) -> None:
        colors = {
            self.up,
            self.down,
            self.front,
            self.back,
            self.left,
            self.right,
        }

        if len(colors) != 6:
            raise ValueError(
                "CubeOrientation must contain each color exactly once."
            )

        if self.front is self.up.opposite:
            raise ValueError(
                "CubeOrientation top and front colors must be adjacent."
            )

        if self.down is not self.up.opposite:
            raise ValueError(
                "CubeOrientation bottom color must oppose the top color."
            )

        if self.back is not self.front.opposite:
            raise ValueError(
                "CubeOrientation back color must oppose the front color."
            )

        if self.right is not _right_color(self.up, self.front):
            raise ValueError(
                "CubeOrientation left and right colors must match the "
                "top and front colors."
            )

    @property
    def top(self) -> Color:
        return self.up

    @property
    def bottom(self) -> Color:
        return self.down

    def color_at(
        self,
        face: LogicalFace,
    ) -> Color:
        """
        Returns the center color mapped to the given logical face.
        """
        return {
            LogicalFace.UP: self.up,
            LogicalFace.DOWN: self.down,
            LogicalFace.FRONT: self.front,
            LogicalFace.BACK: self.back,
            LogicalFace.LEFT: self.left,
            LogicalFace.RIGHT: self.right,
        }[face]

    @classmethod
    def from_top_front(
        cls,
        top: Color,
        front: Color,
    ) -> CubeOrientation:
        """
        Creates the unique legal orientation for top and front colors.
        """
        right = _right_color(top, front)

        return cls(
            up=top,
            down=top.opposite,
            front=front,
            back=front.opposite,
            left=right.opposite,
            right=right,
        )

    def describe(self) -> str:
        return (
            f"Top={self.up.display_name}, "
            f"Front={self.front.display_name}"
        )

    def __str__(self) -> str:
        return self.describe()


_COLOR_VECTORS: dict[Color, tuple[int, int, int]] = {
    Color.WHITE: (0, 1, 0),
    Color.YELLOW: (0, -1, 0),
    Color.GREEN: (0, 0, 1),
    Color.BLUE: (0, 0, -1),
    Color.RED: (1, 0, 0),
    Color.ORANGE: (-1, 0, 0),
}


_COLOR_BY_VECTOR = {
    vector: color
    for color, vector in _COLOR_VECTORS.items()
}


def _right_color(
    top: Color,
    front: Color,
) -> Color:
    if top is front or top is front.opposite:
        raise ValueError(
            "CubeOrientation top and front colors must be adjacent."
        )

    top_x, top_y, top_z = _COLOR_VECTORS[top]
    front_x, front_y, front_z = _COLOR_VECTORS[front]

    vector = (
        top_y * front_z - top_z * front_y,
        top_z * front_x - top_x * front_z,
        top_x * front_y - top_y * front_x,
    )

    return _COLOR_BY_VECTOR[vector]


CANONICAL_ORIENTATION = CubeOrientation(
    up=Color.WHITE,
    down=Color.YELLOW,
    front=Color.GREEN,
    back=Color.BLUE,
    left=Color.ORANGE,
    right=Color.RED,
)
