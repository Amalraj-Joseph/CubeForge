import pytest

from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)
from cube.internal.canonical_moves import (
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
from cube.notation.algorithm_parser import (
    parse_algorithm,
)


# ==============================================================================
# Move Inverses
# ==============================================================================

@pytest.mark.parametrize(
    ("move", "inverse"),
    [
        (U, U_PRIME),
        (D, D_PRIME),
        (F, F_PRIME),
        (B, B_PRIME),
        (L, L_PRIME),
        (R, R_PRIME),
    ],
)
def test_move_then_inverse_returns_solved(
    move,
    inverse,
):
    cube = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        move,
    )

    cube = CubeTransformer.apply(
        cube,
        inverse,
    )

    assert cube == CANONICAL_CUBE_STATE


@pytest.mark.parametrize(
    ("move", "inverse"),
    [
        (U_PRIME, U),
        (D_PRIME, D),
        (F_PRIME, F),
        (B_PRIME, B),
        (L_PRIME, L),
        (R_PRIME, R),
    ],
)
def test_inverse_then_move_returns_solved(
    move,
    inverse,
):
    cube = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        move,
    )

    cube = CubeTransformer.apply(
        cube,
        inverse,
    )

    assert cube == CANONICAL_CUBE_STATE


# ==============================================================================
# Quarter Turns
# ==============================================================================

@pytest.mark.parametrize(
    "move",
    [
        U,
        D,
        F,
        B,
        L,
        R,
    ],
)
def test_four_quarter_turns_are_identity(
    move,
):
    cube = CANONICAL_CUBE_STATE

    for _ in range(4):
        cube = CubeTransformer.apply(
            cube,
            move,
        )

    assert cube == CANONICAL_CUBE_STATE


# ==============================================================================
# Half Turns
# ==============================================================================

@pytest.mark.parametrize(
    "move",
    [
        U2,
        D2,
        F2,
        B2,
        L2,
        R2,
    ],
)
def test_two_half_turns_are_identity(
    move,
):
    cube = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        move,
    )

    cube = CubeTransformer.apply(
        cube,
        move,
    )

    assert cube == CANONICAL_CUBE_STATE


# ==============================================================================
# Algorithms
# ==============================================================================

def test_scramble_and_inverse_returns_solved():
    scramble = parse_algorithm(
        (
            "R F' U D' L U2 D' U2 R' U' "
            "R2 D2 R' D R' B D R F2 R "
            "U2 D2 L2 D' U2"
        )
    )

    inverse = parse_algorithm(
        (
            "U2 D L2 D2 U2 R' F2 R' D' "
            "B' R D' R D2 R2 U R U2 "
            "D U2 L' D U' F R'"
        )
    )

    cube = CubeTransformer.apply_algorithm(
        CANONICAL_CUBE_STATE,
        scramble,
    )

    cube = CubeTransformer.apply_algorithm(
        cube,
        inverse,
    )

    assert cube == CANONICAL_CUBE_STATE


def test_algorithm_then_inverse_sequence():
    algorithm = parse_algorithm(
        "R U R' U'"
    )

    inverse = parse_algorithm(
        "U R U' R'"
    )

    cube = CubeTransformer.apply_algorithm(
        CANONICAL_CUBE_STATE,
        algorithm,
    )

    cube = CubeTransformer.apply_algorithm(
        cube,
        inverse,
    )

    assert cube == CANONICAL_CUBE_STATE


# ==============================================================================
# CubeState
# ==============================================================================

def test_solved_cube_equals_canonical():
    assert (
        CANONICAL_CUBE_STATE
        == CANONICAL_CUBE_STATE
    )


def test_move_changes_cube():
    moved = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R,
    )

    assert moved != CANONICAL_CUBE_STATE