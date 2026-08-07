from __future__ import annotations

from dataclasses import dataclass

from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.internal.piece_projection import (
    project_at_position,
)
from cube.piece.piece import Piece
from cube.piece.piece_layout import PieceLayout
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
        piece_type = self.piece_type

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
        Returns the type of this Piece.
        """
        return self.piece.piece_type

    @property
    def projected_layout(self) -> PieceLayout:
        """
        Returns the PieceLayout projected according to the
        current PieceOrientation.
        """
        return project_at_position(
            self.piece.layout,
            self.orientation,
            self.position,
        )

    def occupies(
        self,
        face: LogicalFace,
    ) -> bool:
        """
        Returns True if this Piece occupies the given
        LogicalFace.
        """
        return self.position.contains(face)

    def color_on(
        self,
        face: LogicalFace,
    ) -> Color:
        """
        Returns the Color visible on the given LogicalFace.

        Raises:
            ValueError:
                If this Piece does not occupy the requested
                LogicalFace.
        """
        if not self.occupies(face):
            raise ValueError(
                f"{self.position} does not occupy {face}."
            )

        return self.projected_layout.color_on(face)

    def describe(self) -> str:
        """
        Returns a human-readable description.
        """
        return (
            f"Piece={self.piece.describe()}, "
            f"Position={self.position.describe()}, "
            f"Orientation={self.orientation.value}"
        )

    def __str__(self) -> str:
        return self.describe()
