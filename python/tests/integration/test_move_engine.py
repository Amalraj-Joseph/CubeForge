from cube.cube_transformer import CubeTransformer
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
from cube.piece.piece_type import PieceType

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
