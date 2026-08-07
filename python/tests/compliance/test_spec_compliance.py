"""
Per-requirement compliance audit.

One test function per mandatory ("shall") bullet in specs/v1/11-api.md and
specs/v1/12-compliance.md. Every assertion goes through the real public
API (`cube.Cube`, `cube.CubeState`, `cube.algorithm.Algorithm`,
`cube.move.Move`, `cube.transformation.CubeTransformation`,
`cube.orientation.CubeOrientation`, `cube.validation.*`) - never internals -
except for fixtures used to build known inputs.

This is the permanent regression gate referenced by
specs/v1.1/plan.md's v1.0 phase: every future language port should be able
to re-derive this same list of assertions from the spec alone.
"""

import dataclasses

import pytest

from cube import Cube, CubeAnalyzer, CubeState, SPECIFICATION_VERSION
from cube.algorithm.algorithm import Algorithm
from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import (
    ALL_MOVES,
    F,
    F_PRIME,
    R,
    R2,
    R_PRIME,
    U,
    U_PRIME,
)
from cube.internal.canonical_piece_layouts import WHITE_CENTER_LAYOUT
from cube.internal.canonical_pieces import ALL_PIECES, WHITE_CENTER
from cube.internal.canonical_positions import ALL_POSITIONS, UF
from cube.internal.canonical_positions import U as U_POSITION
from cube.notation.algorithm_formatter import format_algorithm
from cube.notation.algorithm_parser import parse_algorithm
from cube.orientation.cube_orientation import CANONICAL_ORIENTATION, CubeOrientation
from cube.piece.piece import Piece
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType
from cube.position.position import Position
from cube.position.position_type import PositionType
from cube.transformation import (
    ROLL_CLOCKWISE,
    ROLL_COUNTERCLOCKWISE,
    ROTATE_DOWN,
    ROTATE_LEFT,
    ROTATE_RIGHT,
    ROTATE_UP,
)
from cube.transformation.cube_transformation import CubeTransformation
from cube.validation import CubeOrientationValidator, CubeStateValidator, PieceValidator

ALL_TRANSFORMATIONS = (
    ROTATE_LEFT,
    ROTATE_RIGHT,
    ROTATE_UP,
    ROTATE_DOWN,
    ROLL_CLOCKWISE,
    ROLL_COUNTERCLOCKWISE,
)


def create_piece_states():
    """Fresh, mutable list of canonical PieceStates for building variants."""
    from cube.internal.canonical_cube import CANONICAL_CUBE

    return [
        PieceState(piece, position, PieceOrientation(piece.piece_type, 0))
        for piece, position in CANONICAL_CUBE.items()
    ]


# ==============================================================================
# 11-api.md - Cube Construction
# ==============================================================================

def test_construct_cube_in_canonical_state():
    cube = Cube.canonical()

    assert cube.solved
    assert cube.state == CANONICAL_CUBE_STATE


def test_construct_cube_from_valid_cube_state():
    cube = Cube(CANONICAL_CUBE_STATE)

    assert cube.state == CANONICAL_CUBE_STATE


def test_construct_cube_from_serialized_representation():
    text = Cube.canonical().to_json()
    cube = Cube.from_json(text)

    assert cube == Cube.canonical()


# ==============================================================================
# 11-api.md - Cube Inspection
# ==============================================================================

def test_inspect_cube_state():
    assert isinstance(Cube.canonical().state, CubeState)


def test_inspect_cube_orientation():
    assert isinstance(Cube.canonical().orientation, CubeOrientation)


def test_inspect_piece_states():
    cube = Cube.canonical()

    assert len(cube.state) == 26
    assert all(isinstance(state, PieceState) for state in cube.state)


def test_inspect_piece_signatures():
    piece_state = Cube.canonical().state.piece_at(U_POSITION)

    assert isinstance(piece_state.piece.signature, PieceSignature)


def test_inspect_piece_positions():
    piece_state = Cube.canonical().state.piece_at(U_POSITION)

    assert isinstance(piece_state.position, Position)
    assert piece_state.position == U_POSITION


def test_inspect_piece_orientations():
    piece_state = Cube.canonical().state.piece_at(U_POSITION)

    assert isinstance(piece_state.orientation, PieceOrientation)


def test_inspect_solved_property():
    assert Cube.canonical().solved is True
    assert Cube.canonical().apply(R).solved is False


# ==============================================================================
# 11-api.md - Move Capabilities
# ==============================================================================

def test_represent_standard_moves():
    assert len(ALL_MOVES) == 18
    assert all(
        hasattr(move, "face") and hasattr(move, "rotation")
        for move in ALL_MOVES
    )


def test_interpret_move_notation():
    parsed = parse_algorithm("R")[0]

    assert parsed == R
    assert parsed.notation == "R"


def test_apply_a_move():
    moved = Cube.canonical().apply(R)

    assert not moved.solved
    assert CubeStateValidator.is_valid(moved.state)


def test_apply_multiple_moves_sequentially():
    sequential = Cube.canonical().apply(R).apply(U)
    algorithmic = Cube.canonical().apply_algorithm(Algorithm(R, U))

    assert sequential == algorithmic


def test_determine_move_equality():
    from cube.move.move import Move
    from cube.move.rotation import Rotation

    reconstructed = Move(LogicalFace.RIGHT, Rotation.CLOCKWISE)

    assert reconstructed == R
    assert R != U


def test_compute_inverse_of_a_move():
    assert R.inverse == R_PRIME
    assert R.inverse.inverse == R


def test_applying_a_move_updates_cube_state_per_specification():
    solved_again = Cube.canonical().apply(R).apply(R).apply(R).apply(R)

    assert solved_again.solved


# ==============================================================================
# 11-api.md - Algorithm Capabilities
# ==============================================================================

def test_represent_algorithms():
    algorithm = Algorithm(R, U, R_PRIME, U_PRIME)

    assert isinstance(algorithm, Algorithm)
    assert tuple(algorithm) == (R, U, R_PRIME, U_PRIME)


def test_interpret_algorithm_notation():
    assert parse_algorithm("R U R' U'") == Algorithm(R, U, R_PRIME, U_PRIME)
    assert format_algorithm(Algorithm(R, U, R_PRIME, U_PRIME)) == "R U R' U'"


def test_apply_an_algorithm():
    applied = Cube.canonical().apply_algorithm(Algorithm(R, U, R_PRIME, U_PRIME))
    sequential = (
        Cube.canonical().apply(R).apply(U).apply(R_PRIME).apply(U_PRIME)
    )

    assert applied == sequential


def test_compose_algorithms():
    composed = Algorithm(R, U).compose(Algorithm(R_PRIME, U_PRIME))

    assert composed == Algorithm(R, U, R_PRIME, U_PRIME)


def test_compute_inverse_of_an_algorithm():
    algorithm = Algorithm(R, U, R_PRIME)

    restored = Cube.canonical().apply_algorithm(algorithm).apply_algorithm(
        algorithm.inverse
    )

    assert restored.solved
    assert algorithm.inverse == Algorithm(R, U_PRIME, R_PRIME)


def test_determine_algorithm_equality():
    assert Algorithm(R, U) == Algorithm(R, U)
    assert Algorithm(R, U) != Algorithm(U, R)


# ==============================================================================
# 11-api.md - Cube Transformation Capabilities
# ==============================================================================

def test_represent_cube_transformations():
    assert isinstance(ROTATE_UP, CubeTransformation)
    assert len(ALL_TRANSFORMATIONS) == 6


def test_apply_a_cube_transformation():
    transformed = Cube.canonical().apply_transformation(ROTATE_UP)

    assert transformed.orientation != CANONICAL_ORIENTATION
    assert CubeStateValidator.is_valid(transformed.state)


def test_compose_cube_transformations():
    identity = ROTATE_UP.then(ROTATE_UP.inverse())

    assert all(identity.map_face(face) is face for face in LogicalFace)


def test_compute_inverse_of_a_cube_transformation():
    restored = Cube.canonical().apply_transformation(ROTATE_UP).apply_transformation(
        ROTATE_UP.inverse()
    )

    assert restored.orientation == CANONICAL_ORIENTATION


def test_determine_cube_transformation_equality():
    reconstructed = CubeTransformation({
        LogicalFace.UP: ROTATE_UP.map_face(LogicalFace.UP),
        LogicalFace.DOWN: ROTATE_UP.map_face(LogicalFace.DOWN),
        LogicalFace.FRONT: ROTATE_UP.map_face(LogicalFace.FRONT),
        LogicalFace.BACK: ROTATE_UP.map_face(LogicalFace.BACK),
        LogicalFace.LEFT: ROTATE_UP.map_face(LogicalFace.LEFT),
        LogicalFace.RIGHT: ROTATE_UP.map_face(LogicalFace.RIGHT),
    })

    assert reconstructed == ROTATE_UP
    assert ROTATE_UP != ROTATE_DOWN


@pytest.mark.parametrize("transformation", ALL_TRANSFORMATIONS)
def test_applying_a_cube_transformation_preserves_solved_property(transformation):
    assert Cube.canonical().apply_transformation(transformation).solved


# ==============================================================================
# 11-api.md - Equality
# ==============================================================================

def test_color_equality():
    assert Color.WHITE == Color.WHITE
    assert Color.WHITE != Color.YELLOW


def test_piece_equality():
    reconstructed = Piece(WHITE_CENTER.signature, WHITE_CENTER_LAYOUT)

    assert reconstructed == WHITE_CENTER


def test_position_equality_is_independent_of_face_ordering():
    forward = Position(PositionType.EDGE, LogicalFace.UP, LogicalFace.FRONT)
    reversed_faces = Position(PositionType.EDGE, LogicalFace.FRONT, LogicalFace.UP)

    assert forward == reversed_faces


def test_piece_state_equality():
    first = PieceState(WHITE_CENTER, U_POSITION, PieceOrientation(PieceType.CENTER, 0))
    second = PieceState(WHITE_CENTER, U_POSITION, PieceOrientation(PieceType.CENTER, 0))

    assert first == second


def test_cube_orientation_equality():
    assert CubeOrientation.from_top_front(
        Color.WHITE, Color.GREEN
    ) == CANONICAL_ORIENTATION
    assert CubeOrientation.from_top_front(
        Color.WHITE, Color.RED
    ) != CANONICAL_ORIENTATION


def test_cube_state_equality():
    reconstructed = CubeState(CANONICAL_ORIENTATION, *create_piece_states())

    assert reconstructed == CANONICAL_CUBE_STATE


def test_move_equality_for_equality_section():
    assert R == R
    assert R != R2


def test_algorithm_equality_for_equality_section():
    assert Algorithm(R) == Algorithm(R)
    assert Algorithm(R) != Algorithm(R2)


def test_cube_transformation_equality_for_equality_section():
    assert ROTATE_UP == ROTATE_UP
    assert ROTATE_UP != ROLL_CLOCKWISE


# ==============================================================================
# 11-api.md - Validation
# ==============================================================================

def test_determine_piece_validity():
    assert PieceValidator.is_valid(WHITE_CENTER)
    assert not PieceValidator.is_valid("not a piece")


def test_determine_cube_orientation_validity():
    assert CubeOrientationValidator.is_valid(CANONICAL_ORIENTATION)
    assert not CubeOrientationValidator.is_valid("not an orientation")


def test_determine_cube_state_validity():
    assert CubeStateValidator.is_valid(CANONICAL_CUBE_STATE)
    assert not CubeStateValidator.is_valid("not a cube state")


# ==============================================================================
# 11-api.md - Description
# ==============================================================================

def test_describe_colors():
    assert Color.WHITE.describe() == "White"


def test_describe_pieces():
    assert "Center" in WHITE_CENTER.describe()


def test_describe_positions():
    assert U_POSITION.describe() == "U"


def test_describe_piece_states():
    piece_state = Cube.canonical().state.piece_at(U_POSITION)

    assert "Piece=" in piece_state.describe()
    assert "Position=" in piece_state.describe()


def test_describe_cube_orientation():
    assert "Top=" in CANONICAL_ORIENTATION.describe()


def test_describe_cube_state():
    assert "Orientation:" in Cube.canonical().describe()


def test_describe_moves():
    # Move exposes no separate describe(); its Singmaster notation is its
    # implementation-defined human-readable description (11-api.md does not
    # prescribe method names).
    assert isinstance(R.notation, str) and R.notation


def test_describe_algorithms():
    assert Algorithm(R, U).describe() == "Algorithm(R U)"


def test_describe_cube_transformations():
    assert ROTATE_UP.describe() == "Rotate Up"


# ==============================================================================
# 11-api.md - Serialization (supported, therefore mandatory bullets apply)
# ==============================================================================

def test_serialize_a_cube_state():
    text = Cube.canonical().to_json()

    assert '"format_version"' in text


def test_deserialize_a_cube_state():
    text = Cube.canonical().to_json()
    restored = Cube.from_json(text)

    assert restored == Cube.canonical()


# ==============================================================================
# 12-compliance.md - Mandatory Requirements
# ==============================================================================

def test_represent_all_six_colors():
    assert len(list(Color)) == 6


def test_represent_all_twenty_six_pieces():
    assert len(ALL_PIECES) == 26
    assert len({piece.signature for piece in ALL_PIECES}) == 26


def test_represent_all_six_logical_faces():
    assert len(list(LogicalFace)) == 6


def test_represent_all_twenty_four_legal_cube_orientations():
    legal_pairs = [
        (top, front)
        for top in Color
        for front in Color
        if front is not top and front is not top.opposite
    ]

    assert len(legal_pairs) == 24

    for top, front in legal_pairs:
        orientation = CubeOrientation.from_top_front(top, front)
        assert CubeOrientationValidator.is_valid(orientation)


def test_represent_all_twenty_six_positions():
    assert len(ALL_POSITIONS) == 26
    assert len(set(ALL_POSITIONS)) == 26


def test_represent_piece_states():
    assert isinstance(Cube.canonical().state.piece_at(U_POSITION), PieceState)


def test_represent_cube_states():
    assert isinstance(CANONICAL_CUBE_STATE, CubeState)


def test_support_all_eighteen_standard_moves():
    for move in ALL_MOVES:
        moved = Cube.canonical().apply(move)

        assert CubeStateValidator.is_valid(moved.state)


def test_support_algorithms():
    assert Cube.canonical().apply_algorithm(Algorithm(R, U)).state is not None


def test_support_cube_transformations():
    for transformation in ALL_TRANSFORMATIONS:
        assert CubeStateValidator.is_valid(
            Cube.canonical().apply_transformation(transformation).state
        )


# ==============================================================================
# 12-compliance.md - Behavioural Requirements
# ==============================================================================

@pytest.mark.parametrize("move", ALL_MOVES)
def test_correctly_apply_every_move(move):
    restored = Cube.canonical().apply(move).apply(move.inverse)

    assert restored.solved


def test_correctly_apply_every_algorithm():
    algorithm = Algorithm(R, U, R_PRIME, F, U_PRIME, F_PRIME)

    restored = Cube.canonical().apply_algorithm(algorithm).apply_algorithm(
        algorithm.inverse
    )

    assert restored.solved


@pytest.mark.parametrize("transformation", ALL_TRANSFORMATIONS)
def test_correctly_apply_every_cube_transformation(transformation):
    restored = Cube.canonical().apply_transformation(
        transformation
    ).apply_transformation(transformation.inverse())

    assert restored == Cube.canonical()


def test_correctly_determine_equality():
    assert Cube.canonical() == Cube(CANONICAL_CUBE_STATE)
    assert Cube.canonical() != Cube.canonical().apply(R)


def test_correctly_derive_the_solved_property():
    assert Cube.canonical().solved
    assert not Cube.canonical().apply(R).solved
    assert CubeAnalyzer.is_solved(Cube.canonical().state)


def test_correctly_identify_the_canonical_cube_state():
    assert Cube.canonical().state == CANONICAL_CUBE_STATE
    assert Cube.canonical().orientation == CANONICAL_ORIENTATION


def test_preserve_piece_signatures():
    scrambled = Cube.canonical().apply_algorithm(Algorithm(R, U, R_PRIME, U_PRIME, F))

    before = {state.piece.signature for state in CANONICAL_CUBE_STATE}
    after = {state.piece.signature for state in scrambled.state}

    assert before == after


def test_preserve_cube_validity_after_every_operation():
    scrambled = (
        Cube.canonical()
        .apply(R)
        .apply_algorithm(Algorithm(U, R_PRIME))
        .apply_transformation(ROTATE_UP)
    )

    assert CubeStateValidator.is_valid(scrambled.state)


# ==============================================================================
# 12-compliance.md - Invariant Preservation
# ==============================================================================

def test_piece_signatures_are_immutable():
    with pytest.raises(dataclasses.FrozenInstanceError):
        WHITE_CENTER.signature.piece_type = PieceType.EDGE


def test_positions_are_immutable():
    with pytest.raises(dataclasses.FrozenInstanceError):
        U_POSITION.position_type = PositionType.EDGE


def test_cube_orientation_remains_valid_after_operations():
    scrambled = Cube.canonical().apply_algorithm(
        Algorithm(R, U, R_PRIME)
    ).apply_transformation(ROTATE_UP)

    assert CubeOrientationValidator.is_valid(scrambled.orientation)


def test_piece_types_remain_compatible_with_their_positions():
    assert all(
        state.position.position_type.face_count == state.piece_type.color_count
        for state in CANONICAL_CUBE_STATE
    )


def test_every_position_contains_exactly_one_piece():
    positions = {state.position for state in CANONICAL_CUBE_STATE}

    assert len(positions) == 26


def test_every_piece_occupies_exactly_one_position():
    pieces = {state.piece for state in CANONICAL_CUBE_STATE}

    assert len(pieces) == 26


# ==============================================================================
# 12-compliance.md - Determinism
# ==============================================================================

def test_constructing_a_cube_is_deterministic():
    assert Cube.canonical() == Cube.canonical()


def test_applying_a_move_is_deterministic():
    assert Cube.canonical().apply(R) == Cube.canonical().apply(R)


def test_applying_an_algorithm_is_deterministic():
    algorithm = Algorithm(R, U, R_PRIME)

    assert (
        Cube.canonical().apply_algorithm(algorithm)
        == Cube.canonical().apply_algorithm(algorithm)
    )


def test_applying_a_cube_transformation_is_deterministic():
    assert (
        Cube.canonical().apply_transformation(ROTATE_UP)
        == Cube.canonical().apply_transformation(ROTATE_UP)
    )


# ==============================================================================
# 12-compliance.md - Validation (reject or prevent)
# ==============================================================================

def test_reject_illegal_piece_definitions():
    with pytest.raises(ValueError):
        PieceSignature(PieceType.EDGE, Color.WHITE, Color.YELLOW)

    with pytest.raises(ValueError):
        PieceSignature(PieceType.EDGE, Color.WHITE)


def test_reject_illegal_cube_orientations():
    with pytest.raises(ValueError):
        CubeOrientation(
            up=Color.WHITE,
            down=Color.YELLOW,
            front=Color.GREEN,
            back=Color.BLUE,
            left=Color.RED,
            right=Color.ORANGE,
        )


def test_reject_incompatible_piece_and_position_assignments():
    with pytest.raises(ValueError):
        PieceState(WHITE_CENTER, UF, PieceOrientation(PieceType.CENTER, 0))


def test_reject_duplicate_piece_signatures():
    piece_states = create_piece_states()
    piece_states[1] = PieceState(
        piece_states[0].piece,
        piece_states[1].position,
        piece_states[1].orientation,
    )

    with pytest.raises(ValueError, match="Duplicate Piece"):
        CubeState(CANONICAL_ORIENTATION, *piece_states)


def test_reject_duplicate_position_occupancy():
    piece_states = create_piece_states()
    piece_states[1] = PieceState(
        piece_states[1].piece,
        piece_states[0].position,
        piece_states[1].orientation,
    )

    with pytest.raises(ValueError, match="Duplicate Position"):
        CubeState(CANONICAL_ORIENTATION, *piece_states)


def test_reject_invalid_cube_states():
    assert not CubeStateValidator.is_valid("not a cube state")
    assert CubeStateValidator.validate(CANONICAL_CUBE_STATE) == ()


# ==============================================================================
# 14-validity-and-parity.md - center placement rule
# ==============================================================================

def test_reject_center_placement_inconsistent_with_orientation():
    piece_states = create_piece_states()
    centers = [
        state for state in piece_states
        if state.piece_type is PieceType.CENTER
    ]
    first, second = centers[:2]

    piece_states[piece_states.index(first)] = PieceState(
        first.piece, second.position, first.orientation,
    )
    piece_states[piece_states.index(second)] = PieceState(
        second.piece, first.position, second.orientation,
    )

    with pytest.raises(ValueError, match="center placement"):
        CubeState(CANONICAL_ORIENTATION, *piece_states)


# ==============================================================================
# 12-compliance.md - Versioning
# ==============================================================================

def test_identifies_specification_version():
    assert SPECIFICATION_VERSION == "v1"


# ==============================================================================
# 12-compliance.md - Compliance Principles
#
# These five overarching principles (preserve the mathematical model,
# preserve invariants, deterministic behaviour, expose mandatory
# capabilities, reject/prevent invalid states) are exercised concretely by
# every section above; there is no separate observable behaviour to assert
# for them beyond what those tests already cover.
# ==============================================================================
