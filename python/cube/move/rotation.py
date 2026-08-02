from __future__ import annotations

from enum import Enum


class Rotation(Enum):
    """
    Represents the rotation applied to a face.
    """

    CLOCKWISE = ("", 1)
    HALF_TURN = ("2", 2)
    COUNTERCLOCKWISE = ("'", 3)

    def __init__(
        self,
        notation: str,
        quarter_turns: int,
    ):
        self._notation = notation
        self._quarter_turns = quarter_turns

    @property
    def notation(self) -> str:
        """
        Returns the Singmaster notation suffix.
        """
        return self._notation

    @property
    def quarter_turns(self) -> int:
        """
        Returns the number of clockwise
        quarter turns.
        """
        return self._quarter_turns

    @property
    def inverse(self) -> Rotation:
        """
        Returns the inverse rotation.
        """
        match self:
            case Rotation.CLOCKWISE:
                return Rotation.COUNTERCLOCKWISE

            case Rotation.HALF_TURN:
                return Rotation.HALF_TURN

            case Rotation.COUNTERCLOCKWISE:
                return Rotation.CLOCKWISE

        raise AssertionError("Unreachable")

    @property
    def display_name(self) -> str:
        """
        Returns a human-readable name.
        """
        return self.name.replace(
            "_",
            " ",
        ).title()

    def describe(self) -> str:
        return self.display_name

    def __str__(self) -> str:
        return self.name