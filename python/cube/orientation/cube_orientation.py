from __future__ import annotations

from dataclasses import dataclass

from cube.color.color import Color


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

    @property
    def top(self) -> Color:
        return self.up

    @property
    def bottom(self) -> Color:
        return self.down

    def describe(self) -> str:
        return (
            f"Top={self.up.display_name}, "
            f"Front={self.front.display_name}"
        )

    def __str__(self) -> str:
        return self.describe()