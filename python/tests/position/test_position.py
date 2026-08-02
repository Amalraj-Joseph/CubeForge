import pytest

from cube.face.logical_face import LogicalFace
from cube.position.position import Position
from cube.position.position_type import PositionType


# ==============================================================================
# Construction
# ==============================================================================

def test_create_center_position():
    position = Position(
        PositionType.CENTER,
        LogicalFace.UP,
    )

    assert position.position_type is PositionType.CENTER
    assert position.faces == frozenset({
        LogicalFace.UP,
    })


def test_create_edge_position():
    position = Position(
        PositionType.EDGE,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

    assert position.position_type is PositionType.EDGE
    assert position.faces == frozenset({
        LogicalFace.UP,
        LogicalFace.FRONT,
    })


def test_create_corner_position():
    position = Position(
        PositionType.CORNER,
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    )

    assert position.position_type is PositionType.CORNER
    assert position.faces == frozenset({
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    })


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    ("position_type", "faces"),
    [
        (PositionType.CENTER, []),
        (PositionType.CENTER, [LogicalFace.UP, LogicalFace.FRONT]),
        (PositionType.EDGE, [LogicalFace.UP]),
        (PositionType.EDGE, [LogicalFace.UP, LogicalFace.FRONT, LogicalFace.RIGHT]),
        (PositionType.CORNER, [LogicalFace.UP]),
        (PositionType.CORNER, [LogicalFace.UP, LogicalFace.FRONT]),
        (
            PositionType.CORNER,
            [
                LogicalFace.UP,
                LogicalFace.FRONT,
                LogicalFace.RIGHT,
                LogicalFace.LEFT,
            ],
        ),
    ],
)
def test_invalid_face_count(position_type, faces):
    with pytest.raises(ValueError):
        Position(position_type, *faces)


def test_duplicate_faces_not_allowed():
    with pytest.raises(ValueError):
        Position(
            PositionType.EDGE,
            LogicalFace.UP,
            LogicalFace.UP,
        )


# ==============================================================================
# Faces
# ==============================================================================

def test_faces_are_immutable():
    position = Position(
        PositionType.EDGE,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

    assert isinstance(position.faces, frozenset)

    with pytest.raises(AttributeError):
        position.faces.add(LogicalFace.RIGHT)


# ==============================================================================
# Membership
# ==============================================================================

def test_contains():
    position = Position(
        PositionType.CORNER,
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    )

    assert position.contains(LogicalFace.UP)
    assert position.contains(LogicalFace.FRONT)
    assert position.contains(LogicalFace.RIGHT)

    assert not position.contains(LogicalFace.DOWN)
    assert not position.contains(LogicalFace.LEFT)
    assert not position.contains(LogicalFace.BACK)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_is_order_independent():
    first = Position(
        PositionType.CORNER,
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    )

    second = Position(
        PositionType.CORNER,
        LogicalFace.RIGHT,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

    assert first == second
    assert hash(first) == hash(second)


def test_different_positions_are_not_equal():
    first = Position(
        PositionType.CENTER,
        LogicalFace.UP,
    )

    second = Position(
        PositionType.EDGE,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

    assert first != second


def test_hashable():
    positions = {
        Position(
            PositionType.CENTER,
            LogicalFace.UP,
        ),
        Position(
            PositionType.EDGE,
            LogicalFace.UP,
            LogicalFace.FRONT,
        ),
    }

    assert len(positions) == 2


# ==============================================================================
# Contract
# ==============================================================================

def test_position_contract():
    position = Position(
        PositionType.CORNER,
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    )

    assert isinstance(position.faces, frozenset)

    assert len(position.faces) == position.position_type.face_count

    assert position.faces == frozenset({
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    })


# ==============================================================================
# Ordering
# ==============================================================================

def test_ordered_faces():
    position = Position(
        PositionType.CORNER,
        LogicalFace.RIGHT,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

    assert position.ordered_faces == (
        LogicalFace.RIGHT,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

def test_faces_are_order_independent():
    position = Position(
        PositionType.CORNER,
        LogicalFace.RIGHT,
        LogicalFace.UP,
        LogicalFace.FRONT,
    )

    assert position.faces == frozenset({
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.RIGHT,
    })

# ==============================================================================
# Representation
# ==============================================================================

@pytest.mark.parametrize(
    ("position", "expected"),
    [
        (
            Position(
                PositionType.CENTER,
                LogicalFace.UP,
            ),
            "U",
        ),
        (
            Position(
                PositionType.EDGE,
                LogicalFace.UP,
                LogicalFace.FRONT,
            ),
            "UF",
        ),
        (
            Position(
                PositionType.CORNER,
                LogicalFace.UP,
                LogicalFace.FRONT,
                LogicalFace.RIGHT,
            ),
            "UFR",
        ),
    ],
)
def test_description(
    position,
    expected,
):
    assert position.describe() == expected


@pytest.mark.parametrize(
    ("position", "expected"),
    [
        (
            Position(
                PositionType.CENTER,
                LogicalFace.UP,
            ),
            "U",
        ),
        (
            Position(
                PositionType.EDGE,
                LogicalFace.UP,
                LogicalFace.FRONT,
            ),
            "UF",
        ),
        (
            Position(
                PositionType.CORNER,
                LogicalFace.UP,
                LogicalFace.FRONT,
                LogicalFace.RIGHT,
            ),
            "UFR",
        ),
    ],
)
def test_string_representation(
    position,
    expected,
):
    assert str(position) == expected