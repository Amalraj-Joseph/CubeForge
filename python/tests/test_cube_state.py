import pytest

from cube.cube_state import CubeState
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_state import PieceState


def create_piece_states():
    return [
        PieceState(
            piece,
            position,
            PieceOrientation(
                piece.signature.piece_type,
                0,
            ),
        )
        for piece, position in CANONICAL_CUBE.items()
    ]


# ==============================================================================
# Construction
# ==============================================================================

def test_create_cube_state():
    cube = CubeState(
        *create_piece_states(),
    )

    assert len(cube) == 26


# ==============================================================================
# Validation
# ==============================================================================

def test_requires_exactly_26_piece_states():
    with pytest.raises(ValueError):
        CubeState()


def test_duplicate_piece_not_allowed():
    piece_states = create_piece_states()

    piece_states[-1] = piece_states[0]

    with pytest.raises(ValueError):
        CubeState(
            *piece_states,
        )


def test_duplicate_position_not_allowed():
    piece_states = create_piece_states()

    first = next(
        state for state in piece_states
        if state.piece_type.color_count == 2
    )

    second = next(
        state
        for state in piece_states
        if (
            state is not first
            and state.piece_type.color_count == 2
        )
    )

    piece_states[piece_states.index(second)] = PieceState(
        second.piece,
        first.position,
        second.orientation,
    )

    with pytest.raises(ValueError):
        CubeState(*piece_states)


# ==============================================================================
# Lookup
# ==============================================================================

def test_contains():
    cube = CubeState(
        *create_piece_states(),
    )

    first = next(iter(cube))

    assert first.piece in cube


def test_piece_lookup():
    cube = CubeState(
        *create_piece_states(),
    )

    first = next(iter(cube))

    assert cube[first.piece] is first


def test_piece_at_lookup():
    cube = CubeState(
        *create_piece_states(),
    )

    first = next(iter(cube))

    assert cube.piece_at(first.position) is first


# ==============================================================================
# Collection Protocol
# ==============================================================================

def test_length():
    cube = CubeState(
        *create_piece_states(),
    )

    assert len(cube) == 26


def test_iteration():
    cube = CubeState(
        *create_piece_states(),
    )

    assert len(tuple(cube)) == len(cube)


# ==============================================================================
# Contract
# ==============================================================================

def test_cube_state_contract():
    cube = CubeState(
        *create_piece_states(),
    )

    assert len(cube) == 26

    assert len(tuple(cube)) == len(cube)

    assert len({
        state.piece
        for state in cube
    }) == len(cube)

    assert len({
        state.position
        for state in cube
    }) == len(cube)