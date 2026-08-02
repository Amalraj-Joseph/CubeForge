import pytest

from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_type import PieceType


# ==============================================================================
# Construction
# ==============================================================================

def test_create_center_layout():
    layout = PieceLayout(
        PieceType.CENTER,
        (
            LogicalFace.UP,
            Color.WHITE,
        ),
    )

    assert layout.piece_type is PieceType.CENTER

    assert layout.stickers == (
        (
            LogicalFace.UP,
            Color.WHITE,
        ),
    )


def test_create_edge_layout():
    layout = PieceLayout(
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

    assert layout.piece_type is PieceType.EDGE

    assert layout.stickers == (
        (
            LogicalFace.UP,
            Color.WHITE,
        ),
        (
            LogicalFace.FRONT,
            Color.GREEN,
        ),
    )


def test_create_corner_layout():
    layout = PieceLayout(
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

    assert layout.piece_type is PieceType.CORNER

    assert layout.stickers == (
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
# Ordering
# ==============================================================================

def test_stickers_preserve_order():
    layout = PieceLayout(
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

    assert layout.stickers == (
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

@pytest.mark.parametrize(
    ("piece_type", "stickers"),
    [
        (PieceType.CENTER, []),
        (
            PieceType.CENTER,
            [
                (
                    LogicalFace.UP,
                    Color.WHITE,
                ),
                (
                    LogicalFace.FRONT,
                    Color.GREEN,
                ),
            ],
        ),
        (
            PieceType.EDGE,
            [
                (
                    LogicalFace.UP,
                    Color.WHITE,
                ),
            ],
        ),
        (
            PieceType.EDGE,
            [
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
            ],
        ),
        (
            PieceType.CORNER,
            [
                (
                    LogicalFace.UP,
                    Color.WHITE,
                ),
            ],
        ),
        (
            PieceType.CORNER,
            [
                (
                    LogicalFace.UP,
                    Color.WHITE,
                ),
                (
                    LogicalFace.FRONT,
                    Color.GREEN,
                ),
            ],
        ),
    ],
)
def test_invalid_sticker_count(
    piece_type,
    stickers,
):
    with pytest.raises(ValueError):
        PieceLayout(
            piece_type,
            *stickers,
        )


def test_duplicate_faces_not_allowed():
    with pytest.raises(ValueError):
        PieceLayout(
            PieceType.EDGE,
            (
                LogicalFace.UP,
                Color.WHITE,
            ),
            (
                LogicalFace.UP,
                Color.YELLOW,
            ),
        )


# ==============================================================================
# Lookup
# ==============================================================================

def test_color_on():
    layout = PieceLayout(
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

    assert (
        layout.color_on(
            LogicalFace.UP,
        )
        is Color.WHITE
    )

    assert (
        layout.color_on(
            LogicalFace.FRONT,
        )
        is Color.GREEN
    )

    assert (
        layout.color_on(
            LogicalFace.RIGHT,
        )
        is Color.RED
    )


def test_color_on_invalid_face():
    layout = PieceLayout(
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

    with pytest.raises(ValueError):
        layout.color_on(
            LogicalFace.LEFT,
        )


# ==============================================================================
# Membership
# ==============================================================================

def test_contains():
    layout = PieceLayout(
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

    assert layout.contains(
        LogicalFace.UP,
    )

    assert layout.contains(
        LogicalFace.FRONT,
    )

    assert not layout.contains(
        LogicalFace.RIGHT,
    )


# ==============================================================================
# Faces & Colors
# ==============================================================================

def test_faces():
    layout = PieceLayout(
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

    assert layout.faces == frozenset({
        LogicalFace.UP,
        LogicalFace.FRONT,
    })


def test_colors():
    layout = PieceLayout(
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

    assert layout.colors == frozenset({
        Color.WHITE,
        Color.GREEN,
    })


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality():
    first = PieceLayout(
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

    second = PieceLayout(
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

    assert first == second
    assert hash(first) == hash(second)


def test_different_sticker_order_not_equal():
    first = PieceLayout(
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

    second = PieceLayout(
        PieceType.CORNER,
        (
            LogicalFace.FRONT,
            Color.GREEN,
        ),
        (
            LogicalFace.RIGHT,
            Color.RED,
        ),
        (
            LogicalFace.UP,
            Color.WHITE,
        ),
    )

    assert first != second


# ==============================================================================
# Contract
# ==============================================================================

def test_piece_layout_contract():
    layout = PieceLayout(
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

    assert isinstance(
        layout.faces,
        frozenset,
    )

    assert isinstance(
        layout.colors,
        frozenset,
    )

    assert isinstance(
        layout.stickers,
        tuple,
    )

    assert isinstance(
        layout.sticker_map,
        dict,
    )

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

    assert (
        len(layout.sticker_map)
        == layout.piece_type.color_count
    )