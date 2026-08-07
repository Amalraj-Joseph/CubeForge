from cube.algorithm.algorithm import Algorithm
from cube.analysis import CubeStatistics
from cube.cube_state import CubeState
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import F, R, U
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType


def create_piece_states():
    return [
        PieceState(
            piece,
            position,
            PieceOrientation(piece.piece_type, 0),
        )
        for piece, position in CANONICAL_CUBE.items()
    ]


def by_type(piece_states, piece_type):
    return [
        state for state in piece_states
        if state.piece_type is piece_type
    ]


def test_move_count():
    assert CubeStatistics.move_count(Algorithm()) == 0
    assert CubeStatistics.move_count(Algorithm(R)) == 1
    assert CubeStatistics.move_count(Algorithm(R, U, F, R, U)) == 5


def test_statistics_on_canonical_cube():
    cube = CANONICAL_CUBE_STATE

    assert CubeStatistics.solved_faces(cube) == 6
    assert CubeStatistics.solved_edges(cube) == 12
    assert CubeStatistics.solved_corners(cube) == 8


def test_statistics_after_single_move():
    moved = CubeTransformer.apply(CANONICAL_CUBE_STATE, R)

    # L and R remain uniform faces even though R permutes their stickers.
    assert CubeStatistics.solved_faces(moved) == 2
    assert CubeStatistics.solved_edges(moved) == 8
    assert CubeStatistics.solved_corners(moved) == 4


def test_solved_edges_drops_for_flipped_edges_but_not_solved_corners():
    piece_states = create_piece_states()
    first, second = by_type(piece_states, PieceType.EDGE)[:2]

    for state in (first, second):
        piece_states[piece_states.index(state)] = PieceState(
            state.piece,
            state.position,
            PieceOrientation(PieceType.EDGE, 1),
        )

    cube = CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)

    assert CubeStatistics.solved_edges(cube) == 10
    assert CubeStatistics.solved_corners(cube) == 8


def test_solved_corners_drops_for_twisted_corners_but_not_solved_edges():
    piece_states = create_piece_states()
    first, second = by_type(piece_states, PieceType.CORNER)[:2]

    piece_states[piece_states.index(first)] = PieceState(
        first.piece,
        first.position,
        PieceOrientation(PieceType.CORNER, 1),
    )
    piece_states[piece_states.index(second)] = PieceState(
        second.piece,
        second.position,
        PieceOrientation(PieceType.CORNER, 2),
    )

    cube = CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)

    assert CubeStatistics.solved_corners(cube) == 6
    assert CubeStatistics.solved_edges(cube) == 12