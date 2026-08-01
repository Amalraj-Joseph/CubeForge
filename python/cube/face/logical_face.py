from __future__ import annotations

from enum import Enum


class LogicalFace(Enum):
    """
    Represents one of the six logical faces of the cube.

    Logical faces are relative to the current Cube Orientation.
    """

    UP = ("U", "Up", "Y", 0)
    DOWN = ("D", "Down", "Y", 1)

    FRONT = ("F", "Front", "Z", 2)
    BACK = ("B", "Back", "Z", 3)

    LEFT = ("L", "Left", "X", 4)
    RIGHT = ("R", "Right", "X", 5)

    @property
    def symbol(self) -> str:
        """
        Returns the canonical single-letter symbol.
        """
        return self.value[0]

    @property
    def display_name(self) -> str:
        """
        Returns the human-readable name.
        """
        return self.value[1]

    @property
    def axis(self) -> str:
        """
        Returns the axis to which this face belongs.
        """
        return self.value[2]

    @property
    def bit_index(self) -> int:
        """
        Returns the canonical ordering index.
        """
        return self.value[3]

    @property
    def opposite(self) -> "LogicalFace":
        """
        Returns the opposite logical face.
        """
        return _OPPOSITES[self]

    def describe(self) -> str:
        return self.display_name

    @classmethod
    def from_symbol(cls, symbol: str) -> "LogicalFace":
        """
        Returns the LogicalFace corresponding to the given symbol.
        """
        try:
            return _BY_SYMBOL[symbol]
        except KeyError as ex:
            raise ValueError(
                f"Unknown logical face symbol: {symbol}"
            ) from ex

    def __str__(self) -> str:
        return self.symbol


_OPPOSITES = {
    LogicalFace.UP: LogicalFace.DOWN,
    LogicalFace.DOWN: LogicalFace.UP,

    LogicalFace.FRONT: LogicalFace.BACK,
    LogicalFace.BACK: LogicalFace.FRONT,

    LogicalFace.LEFT: LogicalFace.RIGHT,
    LogicalFace.RIGHT: LogicalFace.LEFT,
}


_BY_SYMBOL = {
    face.symbol: face
    for face in LogicalFace
}