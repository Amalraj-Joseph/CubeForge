from cube.color.color import Color
from cube.cube_state import CubeState
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import R
from cube.orientation.cube_orientation import (
    CANONICAL_ORIENTATION,
    CubeOrientation,
)
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_state import PieceState


def create_canonical_piece_states():
    return [
        PieceState(
            piece,
            position,
            PieceOrientation(piece.signature.piece_type, 0),
        )
        for piece, position in CANONICAL_CUBE.items()
    ]


def test_cube_states_with_different_orientations_are_not_equal():
    canonical = CubeState(
        CANONICAL_ORIENTATION,
        *create_canonical_piece_states(),
    )
    rotated = CubeState(
        CubeOrientation.from_top_front(Color.WHITE, Color.RED),
        *create_canonical_piece_states(),
    )

    assert canonical != rotated


def test_move_preserves_cube_orientation():
    transformed = CubeTransformer.apply(CANONICAL_CUBE_STATE, R)

    assert transformed.orientation is CANONICAL_CUBE_STATE.orientation
