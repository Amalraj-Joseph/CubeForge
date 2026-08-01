import pytest

from cube.color.color import Color
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_type import PieceType


# ==============================================================================
# Construction
# ==============================================================================

def test_create_center_signature():
    signature = PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    )

    assert signature.piece_type is PieceType.CENTER
    assert signature.colors == frozenset({
        Color.WHITE,
    })


def test_create_edge_signature():
    signature = PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )

    assert signature.piece_type is PieceType.EDGE
    assert signature.colors == frozenset({
        Color.WHITE,
        Color.GREEN,
    })


def test_create_corner_signature():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )

    assert signature.piece_type is PieceType.CORNER
    assert signature.colors == frozenset({
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    })


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    ("piece_type", "colors"),
    [
        (PieceType.CENTER, []),
        (PieceType.CENTER, [Color.WHITE, Color.GREEN]),

        (PieceType.EDGE, [Color.WHITE]),
        (PieceType.EDGE, [Color.WHITE, Color.GREEN, Color.RED]),

        (PieceType.CORNER, [Color.WHITE]),
        (PieceType.CORNER, [Color.WHITE, Color.GREEN]),
        (
            PieceType.CORNER,
            [
                Color.WHITE,
                Color.GREEN,
                Color.RED,
                Color.BLUE,
            ],
        ),
    ],
)
def test_invalid_color_count(piece_type, colors):
    with pytest.raises(ValueError):
        PieceSignature(piece_type, *colors)


def test_duplicate_colors_not_allowed():
    with pytest.raises(ValueError):
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.WHITE,
        )


# ==============================================================================
# Colors
# ==============================================================================

def test_colors_are_immutable():
    signature = PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )

    assert isinstance(signature.colors, frozenset)


def test_ordered_colors_are_canonical():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.RED,
        Color.WHITE,
        Color.GREEN,
    )

    assert signature.ordered_colors == (
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )


# ==============================================================================
# Mask
# ==============================================================================

def test_mask_center():
    signature = PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    )

    assert signature.mask == Color.WHITE.mask


def test_mask_edge():
    signature = PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )

    assert signature.mask == (
        Color.WHITE.mask |
        Color.GREEN.mask
    )


def test_mask_corner():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )

    assert signature.mask == (
        Color.WHITE.mask |
        Color.GREEN.mask |
        Color.RED.mask
    )


# ==============================================================================
# Membership
# ==============================================================================

def test_contains():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )

    assert signature.contains(Color.WHITE)
    assert signature.contains(Color.GREEN)
    assert signature.contains(Color.RED)

    assert not signature.contains(Color.BLUE)
    assert not signature.contains(Color.YELLOW)
    assert not signature.contains(Color.ORANGE)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_is_order_independent():
    first = PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )

    second = PieceSignature(
        PieceType.CORNER,
        Color.RED,
        Color.WHITE,
        Color.GREEN,
    )

    assert first == second
    assert hash(first) == hash(second)


def test_different_piece_signatures_are_not_equal():
    center = PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    )

    edge = PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )

    assert center != edge


def test_hashable():
    signatures = {
        PieceSignature(
            PieceType.CENTER,
            Color.WHITE,
        ),
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.GREEN,
        ),
    }

    assert len(signatures) == 2


# ==============================================================================
# Representation
# ==============================================================================

def test_description_is_canonical():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.RED,
        Color.WHITE,
        Color.GREEN,
    )

    assert (
        signature.describe()
        == "Corner(White, Green, Red)"
    )


def test_string_representation():
    signature = PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    )

    assert str(signature) == signature.describe()


# ==============================================================================
# Contract
# ==============================================================================

def test_piece_signature_contract():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )

    assert isinstance(signature.colors, frozenset)
    assert isinstance(signature.ordered_colors, tuple)
    assert isinstance(signature.mask, int)
    assert isinstance(signature.description, str)

    assert len(signature.colors) == signature.piece_type.color_count
    assert len(signature.ordered_colors) == signature.piece_type.color_count

    assert signature.mask == (
        Color.WHITE.mask |
        Color.GREEN.mask |
        Color.RED.mask
    )

    assert signature.description == "Corner(White, Green, Red)"