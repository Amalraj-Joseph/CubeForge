import pytest

from cube.piece.piece_type import PieceType

# ==============================================================================
# Enumeration
# ==============================================================================

def test_contains_exactly_three_piece_types():
    assert list(PieceType) == [
        PieceType.CENTER,
        PieceType.EDGE,
        PieceType.CORNER,
    ]


# ==============================================================================
# Properties
# ==============================================================================

@pytest.mark.parametrize(
    ("piece_type", "color_count"),
    [
        (PieceType.CENTER, 1),
        (PieceType.EDGE, 2),
        (PieceType.CORNER, 3),
    ],
)
def test_color_count(piece_type, color_count):
    assert piece_type.color_count == color_count


@pytest.mark.parametrize(
    ("piece_type", "display_name"),
    [
        (PieceType.CENTER, "Center"),
        (PieceType.EDGE, "Edge"),
        (PieceType.CORNER, "Corner"),
    ],
)
def test_display_name(piece_type, display_name):
    assert piece_type.display_name == display_name
    assert piece_type.describe() == display_name


# ==============================================================================
# Equality
# ==============================================================================

def test_identity():
    assert PieceType.CENTER is PieceType.CENTER
    assert PieceType.EDGE != PieceType.CORNER


# ==============================================================================
# Representation
# ==============================================================================

def test_string_representation():
    assert str(PieceType.CENTER) == "CENTER"
    assert str(PieceType.EDGE) == "EDGE"
    assert str(PieceType.CORNER) == "CORNER"


# ==============================================================================
# Immutability
# ==============================================================================

def test_piece_type_is_immutable():
    with pytest.raises(AttributeError):
        PieceType.CENTER.color_count = 99
