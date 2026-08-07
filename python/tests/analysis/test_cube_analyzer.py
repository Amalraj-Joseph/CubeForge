from cube.algorithm.algorithm import Algorithm
from cube.analysis import CubeAnalyzer
from cube.cube_state import CubeState
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import F, R, U
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType
from cube.transformation import ROTATE_UP


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


# ----------------------------------------------------------------------
# Canonical / solved cube
# ----------------------------------------------------------------------

def test_canonical_cube_has_no_errors():
    cube = CANONICAL_CUBE_STATE

    assert CubeAnalyzer.is_solved(cube)
    assert CubeAnalyzer.misplaced_pieces(cube) == ()
    assert CubeAnalyzer.misplaced_edges(cube) == ()
    assert CubeAnalyzer.misplaced_corners(cube) == ()
    assert CubeAnalyzer.edge_orientation_errors(cube) == ()
    assert CubeAnalyzer.corner_orientation_errors(cube) == ()


def test_analysis_is_orientation_independent():
    """
    A solved CubeState reports zero errors regardless of which of the
    twenty-four legal Cube Orientations it is expressed in.
    """
    rotated = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROTATE_UP,
    )

    assert rotated.orientation != CANONICAL_CUBE_STATE.orientation
    assert CubeAnalyzer.is_solved(rotated)
    assert CubeAnalyzer.misplaced_pieces(rotated) == ()
    assert CubeAnalyzer.edge_orientation_errors(rotated) == ()
    assert CubeAnalyzer.corner_orientation_errors(rotated) == ()


# ----------------------------------------------------------------------
# Reachable, scrambled states
# ----------------------------------------------------------------------

def test_single_move_produces_misplaced_edges_and_corners():
    moved = CubeTransformer.apply(CANONICAL_CUBE_STATE, R)

    assert not CubeAnalyzer.is_solved(moved)
    assert len(CubeAnalyzer.misplaced_edges(moved)) == 4
    assert len(CubeAnalyzer.misplaced_corners(moved)) == 4
    assert len(CubeAnalyzer.misplaced_pieces(moved)) == 8

    # A moved piece is reported as misplaced, not as an orientation error;
    # the two categories are mutually exclusive.
    misplaced = set(CubeAnalyzer.misplaced_pieces(moved))
    orientation_errors = set(
        CubeAnalyzer.edge_orientation_errors(moved)
        + CubeAnalyzer.corner_orientation_errors(moved)
    )
    assert misplaced.isdisjoint(orientation_errors)


def test_algorithm_of_moves_only_ever_produces_valid_analysis():
    scrambled = CubeTransformer.apply_algorithm(
        CANONICAL_CUBE_STATE,
        Algorithm(R, U, F, R, U),
    )

    # Every reported piece must genuinely differ from solved.
    for piece_state in CubeAnalyzer.misplaced_pieces(scrambled):
        assert not CubeAnalyzer.is_correctly_placed(scrambled, piece_state)

    for piece_state in (
        CubeAnalyzer.edge_orientation_errors(scrambled)
        + CubeAnalyzer.corner_orientation_errors(scrambled)
    ):
        assert CubeAnalyzer.is_correctly_placed(scrambled, piece_state)
        assert not CubeAnalyzer.is_correctly_oriented(scrambled, piece_state)


# ----------------------------------------------------------------------
# Constructed states isolating a single category of error
# ----------------------------------------------------------------------

def test_two_flipped_edges_are_orientation_errors_not_misplacements():
    piece_states = create_piece_states()
    first, second = by_type(piece_states, PieceType.EDGE)[:2]

    for state in (first, second):
        piece_states[piece_states.index(state)] = PieceState(
            state.piece,
            state.position,
            PieceOrientation(PieceType.EDGE, 1),
        )

    cube = CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)

    assert not CubeAnalyzer.is_solved(cube)
    assert CubeAnalyzer.misplaced_pieces(cube) == ()

    errors = CubeAnalyzer.edge_orientation_errors(cube)
    assert len(errors) == 2
    assert {state.piece for state in errors} == {first.piece, second.piece}
    assert CubeAnalyzer.corner_orientation_errors(cube) == ()


def test_two_twisted_corners_are_orientation_errors_not_misplacements():
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

    assert not CubeAnalyzer.is_solved(cube)
    assert CubeAnalyzer.misplaced_pieces(cube) == ()

    errors = CubeAnalyzer.corner_orientation_errors(cube)
    assert len(errors) == 2
    assert {state.piece for state in errors} == {first.piece, second.piece}
    assert CubeAnalyzer.edge_orientation_errors(cube) == ()


def test_swapped_edges_and_corners_are_misplacements_not_orientation_errors():
    piece_states = create_piece_states()

    e_first, e_second = by_type(piece_states, PieceType.EDGE)[:2]
    piece_states[piece_states.index(e_first)] = PieceState(
        e_first.piece, e_second.position, e_first.orientation,
    )
    piece_states[piece_states.index(e_second)] = PieceState(
        e_second.piece, e_first.position, e_second.orientation,
    )

    c_first, c_second = by_type(piece_states, PieceType.CORNER)[:2]
    piece_states[piece_states.index(c_first)] = PieceState(
        c_first.piece, c_second.position, c_first.orientation,
    )
    piece_states[piece_states.index(c_second)] = PieceState(
        c_second.piece, c_first.position, c_second.orientation,
    )

    cube = CubeState(CANONICAL_CUBE_STATE.orientation, *piece_states)

    assert not CubeAnalyzer.is_solved(cube)
    assert len(CubeAnalyzer.misplaced_edges(cube)) == 2
    assert len(CubeAnalyzer.misplaced_corners(cube)) == 2
    assert CubeAnalyzer.edge_orientation_errors(cube) == ()
    assert CubeAnalyzer.corner_orientation_errors(cube) == ()


# ----------------------------------------------------------------------
# Low-level predicates
# ----------------------------------------------------------------------

def test_is_correctly_placed_and_is_correctly_oriented_on_canonical_piece():
    piece_state = next(iter(CANONICAL_CUBE_STATE))

    assert CubeAnalyzer.is_correctly_placed(CANONICAL_CUBE_STATE, piece_state)
    assert CubeAnalyzer.is_correctly_oriented(CANONICAL_CUBE_STATE, piece_state)