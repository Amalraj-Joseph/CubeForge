from __future__ import annotations

from dataclasses import dataclass

from cube.color.color import Color
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_type import PieceType


@dataclass(frozen=True, slots=True)
class Piece:
    """
    Represents a physical cubie.

    A Piece is immutable and is uniquely identified by its
    PieceSignature.
    """

    signature: PieceSignature

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

    def contains(self, color: Color) -> bool:
        """
        Returns True if this Piece contains the given Color.
        """
        return self.signature.contains(color)

    def describe(self) -> str:
        """
        Returns a human-readable description.
        """
        return self.signature.describe()

    def __str__(self) -> str:
        return self.describe()