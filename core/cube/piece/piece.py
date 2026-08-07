from __future__ import annotations

from dataclasses import dataclass

from cube.color.color import Color
from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_type import PieceType


@dataclass(frozen=True, slots=True, eq=False)
class Piece:
    """
    Represents a physical cubie.

    A Piece is immutable and is uniquely identified by its
    PieceSignature and canonical PieceLayout.
    """

    signature: PieceSignature
    layout: PieceLayout

    def __post_init__(self) -> None:
        if (
            self.layout.piece_type
            is not self.signature.piece_type
        ):
            raise ValueError(
                "PieceSignature and PieceLayout "
                "must have the same PieceType."
            )

        if (
            self.layout.colors
            != self.signature.colors
        ):
            raise ValueError(
                "PieceSignature and PieceLayout "
                "must contain the same Colors."
            )

    @property
    def piece_type(self) -> PieceType:
        """
        Returns the type of this Piece.
        """
        return self.signature.piece_type

    @property
    def colors(self) -> frozenset[Color]:
        """
        Returns the colors belonging to this Piece.
        """
        return self.signature.colors

    def contains(
        self,
        color: Color,
    ) -> bool:
        """
        Returns True if this Piece contains the given Color.
        """
        return self.signature.contains(color)

    def __eq__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(other, Piece):
            return NotImplemented

        return self.signature == other.signature

    def __hash__(self) -> int:
        return hash(self.signature)

    def describe(self) -> str:
        """
        Returns a human-readable description.
        """
        return self.signature.describe()

    def __str__(self) -> str:
        return self.describe()
