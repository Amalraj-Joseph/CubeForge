from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.internal.canonical_piece_layouts import (
    ALL_LAYOUTS,
    CENTER_LAYOUTS,
    EDGE_LAYOUTS,
    CORNER_LAYOUTS,
    WHITE_CENTER_LAYOUT,
    YELLOW_CENTER_LAYOUT,
    GREEN_CENTER_LAYOUT,
    BLUE_CENTER_LAYOUT,
    ORANGE_CENTER_LAYOUT,
    RED_CENTER_LAYOUT,
    WHITE_GREEN_EDGE_LAYOUT,
    GREEN_RED_EDGE_LAYOUT,
    YELLOW_BLUE_EDGE_LAYOUT,
    WHITE_GREEN_RED_CORNER_LAYOUT,
    WHITE_RED_BLUE_CORNER_LAYOUT,
    YELLOW_GREEN_ORANGE_CORNER_LAYOUT,
)
from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_type import PieceType


# ==============================================================================
# Counts
# ==============================================================================

def test_layout_counts():
    assert len(CENTER_LAYOUTS) == 6
    assert len(EDGE_LAYOUTS) == 12
    assert len(CORNER_LAYOUTS) == 8

    assert len(ALL_LAYOUTS) == 26


# ==============================================================================
# Types
# ==============================================================================

def test_all_are_piece_layouts():
    for layout in ALL_LAYOUTS:
        assert isinstance(
            layout,
            PieceLayout,
        )


def test_piece_types():
    assert all(
        layout.piece_type
        is PieceType.CENTER
        for layout in CENTER_LAYOUTS
    )

    assert all(
        layout.piece_type
        is PieceType.EDGE
        for layout in EDGE_LAYOUTS
    )

    assert all(
        layout.piece_type
        is PieceType.CORNER
        for layout in CORNER_LAYOUTS
    )


# ==============================================================================
# Canonical Centers
# ==============================================================================

def test_center_layouts():
    assert (
        WHITE_CENTER_LAYOUT.color_on(
            LogicalFace.UP,
        )
        is Color.WHITE
    )

    assert (
        YELLOW_CENTER_LAYOUT.color_on(
            LogicalFace.DOWN,
        )
        is Color.YELLOW
    )

    assert (
        GREEN_CENTER_LAYOUT.color_on(
            LogicalFace.FRONT,
        )
        is Color.GREEN
    )

    assert (
        BLUE_CENTER_LAYOUT.color_on(
            LogicalFace.BACK,
        )
        is Color.BLUE
    )

    assert (
        ORANGE_CENTER_LAYOUT.color_on(
            LogicalFace.LEFT,
        )
        is Color.ORANGE
    )

    assert (
        RED_CENTER_LAYOUT.color_on(
            LogicalFace.RIGHT,
        )
        is Color.RED
    )


# ==============================================================================
# Canonical Edge
# ==============================================================================

def test_white_green_edge_layout():
    assert (
        WHITE_GREEN_EDGE_LAYOUT.color_on(
            LogicalFace.UP,
        )
        is Color.WHITE
    )

    assert (
        WHITE_GREEN_EDGE_LAYOUT.color_on(
            LogicalFace.FRONT,
        )
        is Color.GREEN
    )


def test_green_red_edge_layout():
    assert (
        GREEN_RED_EDGE_LAYOUT.color_on(
            LogicalFace.FRONT,
        )
        is Color.GREEN
    )

    assert (
        GREEN_RED_EDGE_LAYOUT.color_on(
            LogicalFace.RIGHT,
        )
        is Color.RED
    )


def test_yellow_blue_edge_layout():
    assert (
        YELLOW_BLUE_EDGE_LAYOUT.color_on(
            LogicalFace.DOWN,
        )
        is Color.YELLOW
    )

    assert (
        YELLOW_BLUE_EDGE_LAYOUT.color_on(
            LogicalFace.BACK,
        )
        is Color.BLUE
    )


# ==============================================================================
# Canonical Corner
# ==============================================================================

def test_white_green_red_corner_layout():
    assert (
        WHITE_GREEN_RED_CORNER_LAYOUT.color_on(
            LogicalFace.UP,
        )
        is Color.WHITE
    )

    assert (
        WHITE_GREEN_RED_CORNER_LAYOUT.color_on(
            LogicalFace.FRONT,
        )
        is Color.GREEN
    )

    assert (
        WHITE_GREEN_RED_CORNER_LAYOUT.color_on(
            LogicalFace.RIGHT,
        )
        is Color.RED
    )


def test_white_red_blue_corner_layout():
    assert (
        WHITE_RED_BLUE_CORNER_LAYOUT.color_on(
            LogicalFace.UP,
        )
        is Color.WHITE
    )

    assert (
        WHITE_RED_BLUE_CORNER_LAYOUT.color_on(
            LogicalFace.RIGHT,
        )
        is Color.RED
    )

    assert (
        WHITE_RED_BLUE_CORNER_LAYOUT.color_on(
            LogicalFace.BACK,
        )
        is Color.BLUE
    )


def test_yellow_green_orange_corner_layout():
    assert (
        YELLOW_GREEN_ORANGE_CORNER_LAYOUT.color_on(
            LogicalFace.DOWN,
        )
        is Color.YELLOW
    )

    assert (
        YELLOW_GREEN_ORANGE_CORNER_LAYOUT.color_on(
            LogicalFace.FRONT,
        )
        is Color.GREEN
    )

    assert (
        YELLOW_GREEN_ORANGE_CORNER_LAYOUT.color_on(
            LogicalFace.LEFT,
        )
        is Color.ORANGE
    )


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_layouts_are_unique():
    assert len(
        set(ALL_LAYOUTS)
    ) == len(ALL_LAYOUTS)


# ==============================================================================
# Contract
# ==============================================================================

def test_canonical_layout_contract():
    for layout in ALL_LAYOUTS:
        assert (
            len(layout.faces)
            == layout.piece_type.color_count
        )

        assert (
            len(layout.colors)
            == layout.piece_type.color_count
        )

        assert (
            len(layout.stickers)
            == layout.piece_type.color_count
        )

        for face in layout.faces:
            assert layout.contains(face)

            assert (
                layout.color_on(face)
                in layout.colors
            )