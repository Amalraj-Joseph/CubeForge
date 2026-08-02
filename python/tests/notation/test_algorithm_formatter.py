import pytest

from cube.algorithm.algorithm import Algorithm
from cube.internal.canonical_moves import (
    R,
    U,
    R_PRIME,
    U_PRIME,
)
from cube.notation.algorithm_formatter import (
    format_algorithm,
)


# ==============================================================================
# Formatting
# ==============================================================================

def test_format_empty_algorithm():
    assert (
        format_algorithm(
            Algorithm(),
        )
        == ""
    )


def test_format_single_move():
    assert (
        format_algorithm(
            Algorithm(R),
        )
        == "R"
    )


def test_format_multiple_moves():
    assert (
        format_algorithm(
            Algorithm(
                R,
                U,
                R_PRIME,
                U_PRIME,
            ),
        )
        == "R U R' U'"
    )


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "R U",
        [],
        (),
        42,
        object(),
    ],
)
def test_non_algorithm_not_allowed(
    value,
):
    with pytest.raises(TypeError):
        format_algorithm(value)


# ==============================================================================
# Contract
# ==============================================================================

def test_formatter_contract():
    algorithm = Algorithm(
        R,
        U,
        R_PRIME,
        U_PRIME,
    )

    notation = format_algorithm(
        algorithm,
    )

    assert isinstance(
        notation,
        str,
    )

    assert notation == (
        "R U R' U'"
    )

    assert notation == algorithm.notation