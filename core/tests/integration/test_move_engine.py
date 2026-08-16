from cube.cube_transformer import CubeTransformer
from cube.face.logical_face import LogicalFace
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)
from cube.internal.canonical_moves import (
    B,
    B2,
    B_PRIME,
    D,
    D2,
    D_PRIME,
    F,
    F2,
    F_PRIME,
    L,
    L2,
    L_PRIME,
    R,
    R2,
    R_PRIME,
    U,
    U2,
    U_PRIME,
)
from cube.move.move import Move
from cube.move.rotation import Rotation
from cube.piece.piece_type import PieceType
from cube.transformation.cube_transformation import ROTATE_LEFT

ALL_MOVES = (
    U,
    U2,
    U_PRIME,
    D,
    D2,
    D_PRIME,
    F,
    F2,
    F_PRIME,
    B,
    B2,
    B_PRIME,
    L,
    L2,
    L_PRIME,
    R,
    R2,
    R_PRIME,
)


INVERSE_MOVES = (
    (U, U_PRIME),
    (D, D_PRIME),
    (F, F_PRIME),
    (B, B_PRIME),
    (L, L_PRIME),
    (R, R_PRIME),
)


HALF_TURNS = (
    (U, U2),
    (D, D2),
    (F, F2),
    (B, B2),
    (L, L2),
    (R, R2),
)


# ==============================================================================
# Move Inverses
# ==============================================================================

def test_every_move_has_an_inverse():
    for move, inverse in INVERSE_MOVES:
        transformed = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            move,
        )

        restored = CubeTransformer.apply(
            transformed,
            inverse,
        )

        assert restored == CANONICAL_CUBE_STATE


# ==============================================================================
# Half Turns
# ==============================================================================

def test_every_half_turn_equals_two_clockwise_turns():
    for clockwise, half_turn in HALF_TURNS:
        first = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            half_turn,
        )

        second = CubeTransformer.apply(
            CubeTransformer.apply(
                CANONICAL_CUBE_STATE,
                clockwise,
            ),
            clockwise,
        )

        assert first == second


# ==============================================================================
# Four Quarter Turns
# ==============================================================================

def test_every_face_restores_after_four_turns():
    for move in (
        U,
        D,
        F,
        B,
        L,
        R,
    ):
        cube = CANONICAL_CUBE_STATE

        for _ in range(4):
            cube = CubeTransformer.apply(
                cube,
                move,
            )

        assert cube == CANONICAL_CUBE_STATE


# ==============================================================================
# Piece Integrity
# ==============================================================================

def test_every_move_preserves_piece_integrity():
    for move in ALL_MOVES:
        transformed = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            move,
        )

        assert len(transformed) == 26

        assert len({
            state.piece
            for state in transformed
        }) == 26

        assert len({
            state.position
            for state in transformed
        }) == 26


# ==============================================================================
# Edge Orientation Invariant
# ==============================================================================

def test_every_move_preserves_edge_flip_parity():
    for move in ALL_MOVES:
        transformed = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            move,
        )

        total = sum(
            state.orientation.value
            for state in transformed
            if state.piece_type is PieceType.EDGE
        )

        assert total % 2 == 0


# ==============================================================================
# Corner Orientation Invariant
# ==============================================================================

def test_every_move_preserves_corner_twist_sum():
    for move in ALL_MOVES:
        transformed = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            move,
        )

        total = sum(
            state.orientation.value
            for state in transformed
            if state.piece_type is PieceType.CORNER
        )

        assert total % 3 == 0


# ==============================================================================
# Opposite-Face Mirror Symmetry
# ==============================================================================

# A 180-degree yaw (about the U/D axis) swaps F<->B and L<->R, leaving U/D
# fixed. Unlike a flip about the L/R or F/B axis, it never touches U or D,
# so it doesn't run into the fact that U's and D's clockwise conventions
# are each defined independently and aren't mirror images of each other
# under a physical flip (verified separately; not a bug, out of scope
# here). F/B and L/R, by contrast, share the same "viewed from the side,
# U stays up" framing, so their conventions ARE mirror-consistent.
_YAW_180 = ROTATE_LEFT.then(ROTATE_LEFT)  # F<->B, L<->R; U/D fixed


def test_moves_are_consistent_under_180_degree_reorientation():
    """
    Physically turning the whole cube 180 degrees around the U/D axis
    swaps F with B and L with R. Applying a move to a face in the
    reoriented frame, then reorienting back, must land on the same Cube
    State as applying the equivalent move directly to whichever face
    physically ended up there.

    This is a cheap symmetry check that would have caught B_CORNER's
    original bug (its corners cycled backwards relative to B_EDGE): a
    face whose corner cycle runs the wrong direction breaks this
    equivalence against its opposite face, not just against itself.
    """
    reoriented_solved = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        _YAW_180,
    )

    for face in (
        LogicalFace.FRONT,
        LogicalFace.BACK,
        LogicalFace.LEFT,
        LogicalFace.RIGHT,
    ):
        physical_face = _YAW_180.source_for(face)

        for rotation in (
            Rotation.CLOCKWISE,
            Rotation.COUNTERCLOCKWISE,
            Rotation.HALF_TURN,
        ):
            moved = CubeTransformer.apply(
                reoriented_solved,
                Move(face, rotation),
            )

            restored = CubeTransformer.apply_transformation(
                moved,
                _YAW_180.inverse(),
            )

            expected = CubeTransformer.apply(
                CANONICAL_CUBE_STATE,
                Move(physical_face, rotation),
            )

            assert restored == expected, (face, rotation)
