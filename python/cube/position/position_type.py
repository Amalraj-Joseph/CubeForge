from __future__ import annotations

from enum import Enum


class PositionType(Enum):
    """
    Represents the three logical position types
    of a standard 3×3×3 cube.
    """

    CENTER = 1
    EDGE = 2
    CORNER = 3

    @property
    def face_count(self) -> int:
        """
        Returns the number of logical faces that
        define this position.
        """
        return self.value

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable name.
        """
        return self.name.capitalize()

    def describe(self) -> str:
        """
        Returns a human-readable description.
        """
        return self.display_name

    def __str__(self) -> str:
        return self.name