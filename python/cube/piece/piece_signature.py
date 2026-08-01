from __future__ import annotations

from dataclasses import dataclass, field

from cube.color.color import Color
from cube.piece.piece_type import PieceType


@dataclass(frozen=True, slots=True, init=False)
class PieceSignature:
    """
    Immutable identity of a physical cube piece.

    A PieceSignature consists of

    - PieceType
    - unordered set of Colors

    Position and orientation are intentionally excluded.
    """

    piece_type: PieceType
    _colors: frozenset[Color] = field(repr=False)

    def __init__(self, piece_type: PieceType, *colors: Color):
        if not colors:
            raise ValueError("At least one color must be provided.")

        unique_colors = frozenset(colors)

        if len(unique_colors) != len(colors):
            raise ValueError("Duplicate colors are not permitted.")

        expected = piece_type.color_count

        if len(unique_colors) != expected:
            raise ValueError(
                f"{piece_type.display_name} requires "
                f"{expected} colors, got {len(unique_colors)}."
            )

        object.__setattr__(self, "piece_type", piece_type)
        object.__setattr__(self, "_colors", unique_colors)

    @property
    def colors(self) -> frozenset[Color]:
        """
        Returns the unordered immutable set of colors.
        """
        return self._colors

    @property
    def ordered_colors(self) -> tuple[Color, ...]:
        """
        Returns the colors in canonical specification order.

        Canonical order is determined by Color.bit_index.
        """
        return tuple(
            sorted(
                self._colors,
                key=lambda color: color.bit_index,
            )
        )

    @property
    def mask(self) -> int:
        """
        Returns the bit-mask representation of this PieceSignature.
        """
        mask = 0

        for color in self._colors:
            mask |= color.mask

        return mask

    def contains(self, color: Color) -> bool:
        """
        Returns True if the PieceSignature contains the given Color.
        """
        return color in self._colors

    @property
    def description(self) -> str:
        """
        Returns a human-readable description.
        """
        color_names = (
            color.display_name
            for color in self.ordered_colors
        )

        return (
            f"{self.piece_type.display_name}"
            f"({', '.join(color_names)})"
        )

    def describe(self) -> str:
        return self.description

    def __str__(self) -> str:
        return self.description