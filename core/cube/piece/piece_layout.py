from __future__ import annotations

from dataclasses import dataclass, field

from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.piece.piece_type import PieceType


@dataclass(frozen=True, slots=True, init=False)
class PieceLayout:
    """
    Canonical sticker layout of a physical cube piece.

    A PieceLayout maps each occupied LogicalFace to the
    Color visible on that face when the Piece is in its
    canonical orientation (orientation = 0).

    The order of stickers defines the canonical orientation
    of the Piece and is therefore preserved.
    """

    piece_type: PieceType

    _stickers: tuple[
        tuple[LogicalFace, Color],
        ...
    ] = field(repr=False)

    def __init__(
        self,
        piece_type: PieceType,
        *stickers: tuple[
            LogicalFace,
            Color,
        ],
    ):
        if not stickers:
            raise ValueError(
                "At least one sticker must be provided."
            )

        faces = {
            face
            for face, _ in stickers
        }

        if len(faces) != len(stickers):
            raise ValueError(
                "Duplicate LogicalFaces are not permitted."
            )

        expected = piece_type.color_count

        if len(stickers) != expected:
            raise ValueError(
                f"{piece_type.display_name} requires "
                f"{expected} stickers, "
                f"got {len(stickers)}."
            )

        object.__setattr__(
            self,
            "piece_type",
            piece_type,
        )

        object.__setattr__(
            self,
            "_stickers",
            tuple(stickers),
        )

    @property
    def stickers(
        self,
    ) -> tuple[
        tuple[LogicalFace, Color],
        ...,
    ]:
        """
        Returns the canonical ordered sticker layout.
        """
        return self._stickers

    @property
    def sticker_map(
        self,
    ) -> dict[
        LogicalFace,
        Color,
    ]:
        """
        Returns the sticker mapping.
        """
        return dict(self._stickers)

    @property
    def faces(
        self,
    ) -> frozenset[LogicalFace]:
        """
        Returns the occupied LogicalFaces.
        """
        return frozenset(
            face
            for face, _
            in self._stickers
        )

    @property
    def colors(
        self,
    ) -> frozenset[Color]:
        """
        Returns the sticker Colors.
        """
        return frozenset(
            color
            for _, color
            in self._stickers
        )

    def color_on(
        self,
        face: LogicalFace,
    ) -> Color:
        """
        Returns the Color visible on the given LogicalFace.
        """
        try:
            return self.sticker_map[face]
        except KeyError as ex:
            raise ValueError(
                f"{face} is not part of this PieceLayout."
            ) from ex

    def contains(
        self,
        face: LogicalFace,
    ) -> bool:
        """
        Returns True if this PieceLayout occupies the given
        LogicalFace.
        """
        return face in self.faces
