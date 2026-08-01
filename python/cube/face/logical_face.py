from __future__ import annotations

from enum import Enum


class LogicalFace(Enum):
    """
    Represents one of the six logical faces of the cube.

    Logical faces are relative to the current Cube Orientation.
    """

    UP = ("U", "Up", "Y")
    DOWN = ("D", "Down", "Y")

    FRONT = ("F", "Front", "Z")
    BACK = ("B", "Back", "Z")

    LEFT = ("L", "Left", "X")
    RIGHT = ("R", "Right", "X")

    def __init__(self, notation: str, display_name: str, axis: str):
        self._notation = notation
        self._display_name = display_name
        self._axis = axis

    @property
    def notation(self) -> str:
        return self._notation

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def axis(self) -> str:
        return self._axis

    @property
    def opposite(self) -> "LogicalFace":
        return _OPPOSITES[self]

    def describe(self) -> str:
        return self.display_name

    @classmethod
    def from_notation(cls, notation: str) -> "LogicalFace":
        try:
            return _BY_NOTATION[notation]
        except KeyError as ex:
            raise ValueError(f"Unknown face notation: {notation}") from ex

    def __str__(self) -> str:
        return self.notation


_OPPOSITES = {
    LogicalFace.UP: LogicalFace.DOWN,
    LogicalFace.DOWN: LogicalFace.UP,

    LogicalFace.FRONT: LogicalFace.BACK,
    LogicalFace.BACK: LogicalFace.FRONT,

    LogicalFace.LEFT: LogicalFace.RIGHT,
    LogicalFace.RIGHT: LogicalFace.LEFT,
}


_BY_NOTATION = {
    face.notation: face
    for face in LogicalFace
}