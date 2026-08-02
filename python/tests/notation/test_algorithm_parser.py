import pytest

from cube.algorithm.algorithm import Algorithm
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
from cube.notation.algorithm_parser import (
    MOVE_LOOKUP,
    parse_algorithm,
)


# ==============================================================================
# Construction
# ==============================================================================

def test_parse_empty_algorithm():
    assert parse_algorithm("") == Algorithm()


def test_parse_single_move():
    assert parse_algorithm("R") == Algorithm(R)


def test_parse_multiple_moves():
    assert parse_algorithm(
        "R U R' U'"
    ) == Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )


# ==============================================================================
# Whitespace
# ==============================================================================

def test_parse_leading_and_trailing_whitespace():
    assert parse_algorithm(
        "   R U   "
    ) == Algorithm(
        R,
        U,
    )


def test_parse_multiple_spaces():
    assert parse_algorithm(
        "R   U   R'"
    ) == Algorithm(
        R,
        U,
        R_PRIME,
    )


# ==============================================================================
# Move Types
# ==============================================================================

@pytest.mark.parametrize(
    ("notation", "move"),
    [
        ("U", U),
        ("U2", U2),
        ("U'", U_PRIME),

        ("D", D),
        ("D2", D2),
        ("D'", D_PRIME),

        ("F", F),
        ("F2", F2),
        ("F'", F_PRIME),

        ("B", B),
        ("B2", B2),
        ("B'", B_PRIME),

        ("L", L),
        ("L2", L2),
        ("L'", L_PRIME),

        ("R", R),
        ("R2", R2),
        ("R'", R_PRIME),
    ],
)
def test_parse_all_moves(
    notation,
    move,
):
    assert parse_algorithm(
        notation
    ) == Algorithm(move)


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    "notation",
    [
        "X",
        "R3",
        "RR",
        "R''",
        "U3",
        "M",
        "Rw",
        "x",
    ],
)
def test_invalid_move(
    notation,
):
    with pytest.raises(ValueError):
        parse_algorithm(notation)


# ==============================================================================
# Lookup Table
# ==============================================================================

def test_lookup_contains_all_moves():
    assert len(MOVE_LOOKUP) == 18


def test_lookup_values_are_unique():
    assert len(
        set(MOVE_LOOKUP.values())
    ) == 18


# ==============================================================================
# Contract
# ==============================================================================

def test_parser_contract():
    algorithm = parse_algorithm(
        "R U R' U'"
    )

    assert isinstance(
        algorithm,
        Algorithm,
    )

    assert algorithm.notation == (
        "R U R' U'"
    )

    assert len(algorithm) == 4