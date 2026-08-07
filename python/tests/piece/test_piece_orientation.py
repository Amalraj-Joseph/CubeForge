import pytest

from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_type import PieceType

# ==============================================================================
# Construction
# ==============================================================================

@pytest.mark.parametrize(
    ("piece_type", "value"),
    [
        (PieceType.CENTER, 0),
        (PieceType.EDGE, 0),
        (PieceType.EDGE, 1),
        (PieceType.CORNER, 0),
        (PieceType.CORNER, 1),
        (PieceType.CORNER, 2),
    ],
)
def test_create_orientation(piece_type, value):
    orientation = PieceOrientation(
        piece_type,
        value,
    )

    assert orientation.piece_type is piece_type
    assert orientation.value == value


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    ("piece_type", "value"),
    [
        (PieceType.CENTER, -1),
        (PieceType.CENTER, 1),

        (PieceType.EDGE, -1),
        (PieceType.EDGE, 2),

        (PieceType.CORNER, -1),
        (PieceType.CORNER, 3),
    ],
)
def test_invalid_orientation(piece_type, value):
    with pytest.raises(ValueError):
        PieceOrientation(
            piece_type,
            value,
        )


# ==============================================================================
# Modulus
# ==============================================================================

@pytest.mark.parametrize(
    ("piece_type", "expected"),
    [
        (PieceType.CENTER, 1),
        (PieceType.EDGE, 2),
        (PieceType.CORNER, 3),
    ],
)
def test_modulus(piece_type, expected):
    orientation = PieceOrientation(
        piece_type,
        0,
    )

    assert orientation.modulus == expected


# ==============================================================================
# Rotation
# ==============================================================================

def test_center_rotation():
    orientation = PieceOrientation(
        PieceType.CENTER,
        0,
    )

    assert orientation.rotate(1).value == 0


def test_edge_rotation():
    orientation = PieceOrientation(
        PieceType.EDGE,
        0,
    )

    assert orientation.rotate(1).value == 1
    assert orientation.rotate(2).value == 0
    assert orientation.rotate(3).value == 1


def test_corner_rotation():
    orientation = PieceOrientation(
        PieceType.CORNER,
        0,
    )

    assert orientation.rotate(1).value == 1
    assert orientation.rotate(2).value == 2
    assert orientation.rotate(3).value == 0
    assert orientation.rotate(4).value == 1


def test_negative_rotation():
    orientation = PieceOrientation(
        PieceType.CORNER,
        1,
    )

    assert orientation.rotate(-1).value == 0
    assert orientation.rotate(-2).value == 2


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_and_hashing():
    first = PieceOrientation(
        PieceType.EDGE,
        1,
    )

    second = PieceOrientation(
        PieceType.EDGE,
        1,
    )

    assert first == second
    assert hash(first) == hash(second)


def test_different_orientations_are_not_equal():
    first = PieceOrientation(
        PieceType.CORNER,
        0,
    )

    second = PieceOrientation(
        PieceType.CORNER,
        1,
    )

    assert first != second


# ==============================================================================
# Representation
# ==============================================================================

def test_description():
    orientation = PieceOrientation(
        PieceType.CORNER,
        2,
    )

    assert (
        orientation.describe()
        == "CornerOrientation(2)"
    )


def test_string_representation():
    orientation = PieceOrientation(
        PieceType.EDGE,
        1,
    )

    assert str(orientation) == orientation.describe()

# ==============================================================================
# Convention
# ==============================================================================

def test_orientation_convention():
    center = PieceOrientation(
        PieceType.CENTER,
        0,
    )

    edge = PieceOrientation(
        PieceType.EDGE,
        0,
    )

    corner = PieceOrientation(
        PieceType.CORNER,
        0,
    )

    assert center.rotate(1) == center

    assert edge.rotate(2) == edge

    assert corner.rotate(3) == corner

# ==============================================================================
# Contract
# ==============================================================================

def test_piece_orientation_contract():
    for piece_type in PieceType:
        orientation = PieceOrientation(
            piece_type,
            0,
        )

        assert (
            0
            <= orientation.value
            < orientation.modulus
        )

        assert (
            orientation.modulus
            == piece_type.color_count
        )
