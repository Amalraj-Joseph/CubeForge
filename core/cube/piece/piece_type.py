from __future__ import annotations

from enum import Enum


class PieceType(Enum):
    """
    Represents the three physical piece types of a standard 3×3×3 cube.
    """

    CENTER = 1
    EDGE = 2
    CORNER = 3

    @property
    def color_count(self) -> int:
        """
        Returns the number of colors belonging to this piece type.
        """
        return self.value

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable name.
        """
        return self.name.capitalize()

    def describe(self) -> str:
        return self.display_name

    def __str__(self) -> str:
        return self.name
