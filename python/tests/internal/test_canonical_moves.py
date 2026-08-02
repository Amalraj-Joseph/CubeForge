from cube.face.logical_face import LogicalFace
from cube.internal.canonical_moves import (
    ALL_MOVES,
    BACK_MOVES,
    DOWN_MOVES,
    FRONT_MOVES,
    LEFT_MOVES,
    RIGHT_MOVES,
    UP_MOVES,
    U,
    D,
    F,
    B,
    L,
    R,
)
from cube.move.rotation import Rotation


# ==============================================================================
# Counts
# ==============================================================================

def test_move_counts():
    assert len(UP_MOVES) == 3
    assert len(DOWN_MOVES) == 3
    assert len(FRONT_MOVES) == 3
    assert len(BACK_MOVES) == 3
    assert len(LEFT_MOVES) == 3
    assert len(RIGHT_MOVES) == 3

    assert len(ALL_MOVES) == 18


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_all_moves_are_unique():
    assert len(set(ALL_MOVES)) == 18


def test_all_notations_are_unique():
    assert len({
        move.notation
        for move in ALL_MOVES
    }) == 18


# ==============================================================================
# Collections
# ==============================================================================

def test_all_moves_collection():
    assert ALL_MOVES == (
        *UP_MOVES,
        *DOWN_MOVES,
        *FRONT_MOVES,
        *BACK_MOVES,
        *LEFT_MOVES,
        *RIGHT_MOVES,
    )


# ==============================================================================
# Faces
# ==============================================================================

def test_up_moves():
    assert all(
        move.face is LogicalFace.UP
        for move in UP_MOVES
    )


def test_down_moves():
    assert all(
        move.face is LogicalFace.DOWN
        for move in DOWN_MOVES
    )


def test_front_moves():
    assert all(
        move.face is LogicalFace.FRONT
        for move in FRONT_MOVES
    )


def test_back_moves():
    assert all(
        move.face is LogicalFace.BACK
        for move in BACK_MOVES
    )


def test_left_moves():
    assert all(
        move.face is LogicalFace.LEFT
        for move in LEFT_MOVES
    )


def test_right_moves():
    assert all(
        move.face is LogicalFace.RIGHT
        for move in RIGHT_MOVES
    )


# ==============================================================================
# Canonical Moves
# ==============================================================================

def test_clockwise_moves():
    assert U.rotation is Rotation.CLOCKWISE
    assert D.rotation is Rotation.CLOCKWISE
    assert F.rotation is Rotation.CLOCKWISE
    assert B.rotation is Rotation.CLOCKWISE
    assert L.rotation is Rotation.CLOCKWISE
    assert R.rotation is Rotation.CLOCKWISE


# ==============================================================================
# Contract
# ==============================================================================

def test_canonical_move_contract():
    for move in ALL_MOVES:
        assert move.face
        assert move.rotation
        assert move.notation

        assert move.inverse.inverse == move