from __future__ import annotations

from enum import Enum


class Color(Enum):
    """
    Represents one of the six immutable cube colors.

    Each color is represented by a unique bit mask.
    """

    WHITE = 0b000001
    YELLOW = 0b000010
    GREEN = 0b000100
    BLUE = 0b001000
    RED = 0b010000
    ORANGE = 0b100000

    @property
    def mask(self) -> int:
        """
        Returns the unique bit mask.
        """
        return self.value

    @property
    def bit_index(self) -> int:
        """
        Returns the zero-based bit index.
        """
        return self.mask.bit_length() - 1

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

    @property
    def opposite(self) -> Color:
        """
        Returns the color on the opposite center piece.
        """
        return OPPOSITE_COLORS[self]

    @classmethod
    def from_mask(cls, mask: int) -> Color:
        """
        Returns the Color corresponding to the given bit mask.

        Raises:
            ValueError: If the mask does not correspond to a valid Color.
        """
        try:
            return _MASK_LOOKUP[mask]
        except KeyError as ex:
            raise ValueError(f"Unknown color mask: {mask:#08b}") from ex

    def __str__(self) -> str:
        return self.name


_MASK_LOOKUP: dict[int, Color] = {
    color.mask: color
    for color in Color
}


OPPOSITE_COLORS: dict[Color, Color] = {
    Color.WHITE: Color.YELLOW,
    Color.YELLOW: Color.WHITE,
    Color.GREEN: Color.BLUE,
    Color.BLUE: Color.GREEN,
    Color.RED: Color.ORANGE,
    Color.ORANGE: Color.RED,
}
