from __future__ import annotations

from dataclasses import dataclass

from cube.piece.piece import Piece
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_type import PieceType
from cube.position.position import Position


@dataclass(frozen=True, slots=True)
class PieceState:
    """
    Immutable state of a physical cube piece.

    A PieceState consists of

    - Piece
    - Position
    - PieceOrientation
    """

    piece: Piece
    position: Position
    orientation: PieceOrientation

    def __post_init__(self) -> None:
        piece_type = self.piece.signature.piece_type

        if (
            self.position.position_type.face_count
            != piece_type.color_count
        ):
            raise ValueError(
                "Piece type and Position type must match."
            )

        if (
            self.orientation.piece_type.color_count
            != piece_type.color_count
        ):
            raise ValueError(
                "Piece type and PieceOrientation type must match."
            )

    @property
    def piece_type(self) -> PieceType:
        """
        Returns the type of this piece.
        """
        return self.piece.signature.piece_type