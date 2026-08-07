import pytest

from cube.face.logical_face import LogicalFace
from cube.move.move import Move
from cube.move.rotation import Rotation

# ==============================================================================
# Construction
# ==============================================================================

def test_create_move():
    move = Move(
        LogicalFace.RIGHT,
        Rotation.CLOCKWISE,
    )

    assert move.face is LogicalFace.RIGHT
    assert move.rotation is Rotation.CLOCKWISE


# ==============================================================================
# Notation
# ==============================================================================

@pytest.mark.parametrize(
    ("move", "notation"),
    [
        (
            Move(
                LogicalFace.UP,
                Rotation.CLOCKWISE,
            ),
            "U",
        ),
        (
            Move(
                LogicalFace.RIGHT,
                Rotation.HALF_TURN,
            ),
            "R2",
        ),
        (
            Move(
                LogicalFace.FRONT,
                Rotation.COUNTERCLOCKWISE,
            ),
            "F'",
        ),
    ],
)
def test_notation(move, notation):
    assert move.notation == notation


# ==============================================================================
# Inverse
# ==============================================================================

def test_clockwise_inverse():
    move = Move(
        LogicalFace.UP,
        Rotation.CLOCKWISE,
    )

    inverse = move.inverse

    assert inverse.face is LogicalFace.UP
    assert (
        inverse.rotation
        is Rotation.COUNTERCLOCKWISE
    )


def test_counterclockwise_inverse():
    move = Move(
        LogicalFace.LEFT,
        Rotation.COUNTERCLOCKWISE,
    )

    inverse = move.inverse

    assert inverse.face is LogicalFace.LEFT
    assert (
        inverse.rotation
        is Rotation.CLOCKWISE
    )


def test_half_turn_inverse():
    move = Move(
        LogicalFace.BACK,
        Rotation.HALF_TURN,
    )

    assert (
        move.inverse
        ==
        move
    )


# ==============================================================================
# Half Turn
# ==============================================================================

def test_is_half_turn():
    assert Move(
        LogicalFace.UP,
        Rotation.HALF_TURN,
    ).is_half_turn

    assert not Move(
        LogicalFace.UP,
        Rotation.CLOCKWISE,
    ).is_half_turn


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_and_hashing():
    first = Move(
        LogicalFace.RIGHT,
        Rotation.CLOCKWISE,
    )

    second = Move(
        LogicalFace.RIGHT,
        Rotation.CLOCKWISE,
    )

    third = Move(
        LogicalFace.RIGHT,
        Rotation.HALF_TURN,
    )

    assert first == second
    assert first != third
    assert hash(first) == hash(second)


# ==============================================================================
# Contract
# ==============================================================================

def test_move_contract():
    move = Move(
        LogicalFace.DOWN,
        Rotation.COUNTERCLOCKWISE,
    )

    assert isinstance(
        move.notation,
        str,
    )

    assert (
        move.inverse.inverse
        ==
        move
    )

    assert (
        move.notation
        ==
        "D'"
    )
