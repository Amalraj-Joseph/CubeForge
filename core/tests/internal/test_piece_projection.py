import pytest

from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.internal.piece_projection import (
    project,
    project_at_position,
)
from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_type import PieceType
from cube.position.position import Position
from cube.position.position_type import PositionType

# ==============================================================================
# Fixtures
# ==============================================================================

CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
)

EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
)

CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)


# ==============================================================================
# Validation
# ==============================================================================

def test_piece_type_must_match():
    with pytest.raises(ValueError):
        project(
            EDGE_LAYOUT,
            PieceOrientation(
                PieceType.CORNER,
                0,
            ),
        )


# ==============================================================================
# Centers
# ==============================================================================

def test_center_projection():
    projected = project(
        CENTER_LAYOUT,
        PieceOrientation(
            PieceType.CENTER,
            0,
        ),
    )

    assert projected == CENTER_LAYOUT


# ==============================================================================
# Edges
# ==============================================================================

def test_edge_orientation_zero():
    projected = project(
        EDGE_LAYOUT,
        PieceOrientation(
            PieceType.EDGE,
            0,
        ),
    )

    assert (
        projected.color_on(LogicalFace.UP)
        is Color.WHITE
    )

    assert (
        projected.color_on(LogicalFace.FRONT)
        is Color.GREEN
    )


def test_edge_orientation_one():
    projected = project(
        EDGE_LAYOUT,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
    )

    assert (
        projected.color_on(LogicalFace.UP)
        is Color.GREEN
    )

    assert (
        projected.color_on(LogicalFace.FRONT)
        is Color.WHITE
    )


# ==============================================================================
# Corners
# ==============================================================================

def test_corner_orientation_zero():
    projected = project(
        CORNER_LAYOUT,
        PieceOrientation(
            PieceType.CORNER,
            0,
        ),
    )

    assert (
        projected.color_on(LogicalFace.UP)
        is Color.WHITE
    )

    assert (
        projected.color_on(LogicalFace.FRONT)
        is Color.GREEN
    )

    assert (
        projected.color_on(LogicalFace.RIGHT)
        is Color.RED
    )


def test_corner_orientation_one():
    projected = project(
        CORNER_LAYOUT,
        PieceOrientation(
            PieceType.CORNER,
            1,
        ),
    )

    assert (
        projected.color_on(LogicalFace.UP)
        is Color.GREEN
    )

    assert (
        projected.color_on(LogicalFace.FRONT)
        is Color.RED
    )

    assert (
        projected.color_on(LogicalFace.RIGHT)
        is Color.WHITE
    )


def test_corner_orientation_two():
    projected = project(
        CORNER_LAYOUT,
        PieceOrientation(
            PieceType.CORNER,
            2,
        ),
    )

    assert (
        projected.color_on(LogicalFace.UP)
        is Color.RED
    )

    assert (
        projected.color_on(LogicalFace.FRONT)
        is Color.WHITE
    )

    assert (
        projected.color_on(LogicalFace.RIGHT)
        is Color.GREEN
    )


# ==============================================================================
# Immutability
# ==============================================================================

def test_projection_returns_new_layout():
    projected = project(
        EDGE_LAYOUT,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
    )

    assert projected is not EDGE_LAYOUT


# ==============================================================================
# Cyclic Behaviour
# ==============================================================================

def test_edge_full_rotation_restores_layout():
    projected = project(
        EDGE_LAYOUT,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
    )

    restored = project(
        projected,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
    )

    assert restored == EDGE_LAYOUT


def test_corner_full_rotation_restores_layout():
    projected = project(
        CORNER_LAYOUT,
        PieceOrientation(
            PieceType.CORNER,
            1,
        ),
    )

    projected = project(
        projected,
        PieceOrientation(
            PieceType.CORNER,
            1,
        ),
    )

    restored = project(
        projected,
        PieceOrientation(
            PieceType.CORNER,
            1,
        ),
    )

    assert restored == CORNER_LAYOUT


# ==============================================================================
# Contract
# ==============================================================================

def test_projection_contract():
    for piece_type, layout in (
        (PieceType.CENTER, CENTER_LAYOUT),
        (PieceType.EDGE, EDGE_LAYOUT),
        (PieceType.CORNER, CORNER_LAYOUT),
    ):
        projected = project(
            layout,
            PieceOrientation(
                piece_type,
                0,
            ),
        )

        assert (
            projected.piece_type
            is piece_type
        )

        assert (
            projected.faces
            == layout.faces
        )

        assert (
            projected.colors
            == layout.colors
        )

        assert (
            len(projected.stickers)
            == piece_type.color_count
        )


# ==============================================================================
# Position Remapping
# ==============================================================================

def test_project_at_position_remaps_faces():
    position = Position(
        PositionType.EDGE,
        LogicalFace.UP,
        LogicalFace.RIGHT,
    )

    projected = project_at_position(
        EDGE_LAYOUT,
        PieceOrientation(
            PieceType.EDGE,
            0,
        ),
        position,
    )

    assert projected.faces == position.faces

    assert (
        projected.color_on(
            LogicalFace.UP,
        )
        is Color.WHITE
    )

    assert (
        projected.color_on(
            LogicalFace.RIGHT,
        )
        is Color.GREEN
    )


def test_project_at_position_preserves_orientation():
    position = Position(
        PositionType.EDGE,
        LogicalFace.UP,
        LogicalFace.RIGHT,
    )

    projected = project_at_position(
        EDGE_LAYOUT,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
        position,
    )

    assert (
        projected.color_on(
            LogicalFace.UP,
        )
        is Color.GREEN
    )

    assert (
        projected.color_on(
            LogicalFace.RIGHT,
        )
        is Color.WHITE
    )
