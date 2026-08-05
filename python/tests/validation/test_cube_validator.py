import pytest

from cube.cube_state import CubeState
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import R
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType
from cube.transformation import ROTATE_UP
from cube.validation import (
    CubeOrientationValidator,
    CubeStateValidator,
    PieceValidator,
)


def create_piece_states():
    return [
        PieceState(
            piece,
            position,
            PieceOrientation(piece.piece_type, 0),
        )
        for piece, position in CANONICAL_CUBE.items()
    ]


def test_canonical_cube_is_valid():
    assert CubeStateValidator.is_valid(CANONICAL_CUBE_STATE)
    assert CubeStateValidator.validate(CANONICAL_CUBE_STATE) == ()
    assert CubeOrientationValidator.is_valid(CANONICAL_CUBE_STATE.orientation)
    assert all(PieceValidator.is_valid(state.piece) for state in CANONICAL_CUBE_STATE)


def test_reachable_move_and_transformation_states_are_valid():
    moved = CubeTransformer.apply(CANONICAL_CUBE_STATE, R)
    transformed = CubeTransformer.apply_transformation(moved, ROTATE_UP)

    assert CubeStateValidator.is_valid(moved)
    assert CubeStateValidator.is_valid(transformed)


def test_rejects_single_flipped_edge():
    piece_states = create_piece_states()
    edge = next(
        state for state in piece_states
        if state.piece_type is PieceType.EDGE
    )
    piece_states[piece_states.index(edge)] = PieceState(
        edge.piece,
        edge.position,
        PieceOrientation(PieceType.EDGE, 1),
    )

    with pytest.raises(ValueError, match="edge orientation"):
        CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)


def test_rejects_single_twisted_corner():
    piece_states = create_piece_states()
    corner = next(
        state for state in piece_states
        if state.piece_type is PieceType.CORNER
    )
    piece_states[piece_states.index(corner)] = PieceState(
        corner.piece,
        corner.position,
        PieceOrientation(PieceType.CORNER, 1),
    )

    with pytest.raises(ValueError, match="corner orientation"):
        CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)


def test_rejects_mismatched_permutation_parity():
    piece_states = create_piece_states()
    edges = [
        state for state in piece_states
        if state.piece_type is PieceType.EDGE
    ]
    first, second = edges[:2]

    piece_states[piece_states.index(first)] = PieceState(
        first.piece,
        second.position,
        first.orientation,
    )
    piece_states[piece_states.index(second)] = PieceState(
        second.piece,
        first.position,
        second.orientation,
    )

    with pytest.raises(ValueError, match="permutation parity"):
        CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)
