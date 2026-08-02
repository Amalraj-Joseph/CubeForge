from cube.cube_transformer import CubeTransformer
from cube.piece.piece_type import PieceType
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


# ==============================================================================
# Immutability
# ==============================================================================

def test_returns_new_cube():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        U,
    )

    assert transformed is not CANONICAL_CUBE_STATE


# ==============================================================================
# Four Turns
# ==============================================================================

def test_four_clockwise_turns_restore_cube():
    cube = CANONICAL_CUBE_STATE

    for _ in range(4):
        cube = CubeTransformer.apply(
            cube,
            R,
        )

    assert cube == CANONICAL_CUBE_STATE


# ==============================================================================
# Half Turn
# ==============================================================================

def test_half_turn_equals_two_clockwise_turns():
    first = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R2,
    )

    second = CubeTransformer.apply(
        CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            R,
        ),
        R,
    )

    assert first == second


# ==============================================================================
# Inverse
# ==============================================================================

def test_move_then_inverse_restores_cube():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R,
    )

    restored = CubeTransformer.apply(
        transformed,
        R_PRIME,
    )

    assert restored == CANONICAL_CUBE_STATE


# ==============================================================================
# Piece Count
# ==============================================================================

def test_piece_count_preserved():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        U,
    )

    assert len(transformed) == 26


# ==============================================================================
# Position Uniqueness
# ==============================================================================

def test_positions_remain_unique():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        U,
    )

    assert len({
        state.position
        for state in transformed
    }) == 26


# ==============================================================================
# Orientation
# ==============================================================================

def test_u_preserves_orientations():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        U,
    )

    for state in transformed:
        assert (
            state.orientation
            == CANONICAL_CUBE_STATE[
                state.piece
            ].orientation
        )


def test_r_changes_corner_orientations():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R,
    )

    changed = [
        state
        for state in transformed
        if state.orientation.value != 0
    ]

    assert len(changed) == 4


def test_r_does_not_flip_edges():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R,
    )

    for state in transformed:
        if state.piece_type is PieceType.EDGE:
            assert state.orientation.value == 0


# ==============================================================================
# Contract
# ==============================================================================

def test_transformer_contract():
    transformed = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        U,
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

    assert all(
        state.piece in transformed
        for state in transformed
    )


# ==============================================================================
# Group Invariants
# ==============================================================================

def test_edge_flip_parity():
    """
    The sum of all edge orientations is always even.
    """
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


def test_corner_twist_sum():
    """
    The sum of all corner orientations is always divisible by 3.
    """
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