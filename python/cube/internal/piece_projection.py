from __future__ import annotations

from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_orientation import PieceOrientation
from cube.position.position import Position


def project(
    layout: PieceLayout,
    orientation: PieceOrientation,
) -> PieceLayout:
    """
    Projects a canonical PieceLayout according to a PieceOrientation.

    The returned PieceLayout represents the visible sticker arrangement
    after applying the orientation.

    Convention

    Centers:
        orientation 0

    Edges:
        orientation 0 -> (A, B)
        orientation 1 -> (B, A)

    Corners:
        orientation 0 -> (A, B, C)
        orientation 1 -> (B, C, A)
        orientation 2 -> (C, A, B)
    """
    if (
        layout.piece_type
        is not orientation.piece_type
    ):
        raise ValueError(
            "PieceLayout and PieceOrientation "
            "must have the same PieceType."
        )

    if orientation.value == 0:
        return layout

    stickers = layout.stickers
    colors = tuple(
        color
        for _, color in stickers
    )

    rotation = orientation.value

    return PieceLayout(
        layout.piece_type,
        *(
            (
                face,
                colors[
                    (index + rotation)
                    % len(colors)
                ],
            )
            for index, (face, _)
            in enumerate(stickers)
        ),
    )


def project_at_position(
    layout: PieceLayout,
    orientation: PieceOrientation,
    position: Position,
) -> PieceLayout:
    """
    Projects a canonical PieceLayout according to orientation and
    remaps sticker faces to the piece's current Position.

    Sticker slot i in the canonical layout corresponds to
    position.ordered_faces[i] in the current location.
    """
    oriented = project(
        layout,
        orientation,
    )

    return PieceLayout(
        layout.piece_type,
        *(
            (
                position.ordered_faces[
                    index
                ],
                color,
            )
            for index, (_, color)
            in enumerate(
                oriented.stickers,
            )
        ),
    )