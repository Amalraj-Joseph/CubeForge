import pytest

from cube.algorithm.algorithm import Algorithm
from cube.internal.canonical_moves import (
    R,
    R2,
    R_PRIME,
    U,
    U_PRIME,
)
from cube.move.move import Move


# ==============================================================================
# Construction
# ==============================================================================

def test_create_empty_algorithm():
    algorithm = Algorithm()

    assert len(algorithm) == 0


def test_create_algorithm():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )

    assert tuple(algorithm) == (
        R,
        U,
        R_PRIME,
        U_PRIME,
    )


# ==============================================================================
# Size
# ==============================================================================

def test_length():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
    )

    assert len(algorithm) == 3


# ==============================================================================
# Iteration
# ==============================================================================

def test_iteration():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
    )

    assert list(algorithm) == [
        R,
        U,
        R_PRIME,
    ]


# ==============================================================================
# Indexing
# ==============================================================================

def test_indexing():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
    )

    assert algorithm[0] is R
    assert algorithm[1] is U
    assert algorithm[2] is R_PRIME


def test_negative_indexing():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
    )

    assert algorithm[-1] is R_PRIME
    assert algorithm[-2] is U


def test_index_out_of_range():
    algorithm = Algorithm(
        R,
    )

    with pytest.raises(IndexError):
        _ = algorithm[1]


# ==============================================================================
# Membership
# ==============================================================================

def test_contains():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
    )

    assert R in algorithm
    assert U in algorithm
    assert R2 not in algorithm


# ==============================================================================
# Notation
# ==============================================================================

def test_empty_notation():
    algorithm = Algorithm()

    assert algorithm.notation == ""


def test_notation():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )

    assert (
        algorithm.notation
        == "R U R' U'"
    )


# ==============================================================================
# Description
# ==============================================================================

def test_description():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )

    assert (
        algorithm.describe()
        == "Algorithm(R U R' U')"
    )


def test_string_representation():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )

    assert str(algorithm) == algorithm.describe()


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality():
    first = Algorithm(
        R,
        U,
        R_PRIME,
    )

    second = Algorithm(
        R,
        U,
        R_PRIME,
    )

    assert first == second
    assert hash(first) == hash(second)


def test_inequality():
    first = Algorithm(
        R,
        U,
    )

    second = Algorithm(
        U,
        R,
    )

    assert first != second


def test_hashable():
    algorithms = {
        Algorithm(R),
        Algorithm(U),
    }

    assert len(algorithms) == 2


# ==============================================================================
# Contract
# ==============================================================================

def test_algorithm_contract():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )

    assert isinstance(
        algorithm.moves,
        tuple,
    )

    assert all(
        isinstance(
            move,
            Move,
        )
        for move in algorithm
    )

    assert len(algorithm.moves) == len(algorithm)

    assert (
        algorithm.notation
        == "R U R' U'"
    )

    assert (
        algorithm.description
        == "Algorithm(R U R' U')"
    )


# ==============================================================================
# Validation
# ==============================================================================

def test_non_move_not_allowed():
    with pytest.raises(TypeError):
        Algorithm("R")


# ==============================================================================
# Inverse
# ==============================================================================

def test_inverse_reverses_order_and_inverts_each_move():
    algorithm = Algorithm(R, U, R_PRIME)

    assert algorithm.inverse == Algorithm(R, U_PRIME, R_PRIME)


def test_inverse_of_empty_algorithm_is_empty():
    assert Algorithm().inverse == Algorithm()


def test_algorithm_then_its_inverse_restores_cube_state():
    from cube.cube_transformer import CubeTransformer
    from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE

    algorithm = Algorithm(R, U, R_PRIME, U_PRIME)

    restored = CubeTransformer.apply_algorithm(
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            algorithm,
        ),
        algorithm.inverse,
    )

    assert restored == CANONICAL_CUBE_STATE


# ==============================================================================
# Compose
# ==============================================================================

def test_compose_concatenates_moves_in_order():
    first = Algorithm(R, U)
    second = Algorithm(R_PRIME, U_PRIME)

    assert first.compose(second) == Algorithm(R, U, R_PRIME, U_PRIME)


def test_compose_with_empty_algorithm_is_identity():
    algorithm = Algorithm(R, U)

    assert algorithm.compose(Algorithm()) == algorithm
    assert Algorithm().compose(algorithm) == algorithm


def test_compose_matches_sequential_application():
    from cube.cube_transformer import CubeTransformer
    from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE

    first = Algorithm(R, U)
    second = Algorithm(R_PRIME, U_PRIME)

    composed_result = CubeTransformer.apply_algorithm(
        CANONICAL_CUBE_STATE,
        first.compose(second),
    )

    sequential_result = CubeTransformer.apply_algorithm(
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            first,
        ),
        second,
    )

    assert composed_result == sequential_result