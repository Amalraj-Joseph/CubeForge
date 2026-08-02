from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)
from cube.notation.algorithm_formatter import (
    format_algorithm,
)
from cube.notation.algorithm_parser import (
    parse_algorithm,
)


# ==============================================================================
# Parse -> Format
# ==============================================================================

def test_parse_then_format():
    notation = "R U R' U'"

    algorithm = parse_algorithm(
        notation,
    )

    assert (
        format_algorithm(
            algorithm,
        )
        == notation
    )


# ==============================================================================
# Format -> Parse
# ==============================================================================

def test_format_then_parse():
    algorithm = parse_algorithm(
        "R U2 F' L",
    )

    formatted = format_algorithm(
        algorithm,
    )

    parsed = parse_algorithm(
        formatted,
    )

    assert parsed == algorithm


# ==============================================================================
# Parse -> Execute
# ==============================================================================

def test_parse_then_execute():
    algorithm = parse_algorithm(
        "R U R' U'",
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            algorithm,
        )
    )

    assert transformed != CANONICAL_CUBE_STATE


# ==============================================================================
# Execute -> Inverse
# ==============================================================================

def test_algorithm_then_inverse():
    algorithm = parse_algorithm(
        "R U R' U'",
    )

    inverse = parse_algorithm(
        "U R U' R'",
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            algorithm,
        )
    )

    restored = (
        CubeTransformer.apply_algorithm(
            transformed,
            inverse,
        )
    )

    assert restored == CANONICAL_CUBE_STATE


# ==============================================================================
# Round Trip
# ==============================================================================

def test_algorithm_round_trip():
    notation = (
        "R U2 F' L D2 B U' R2"
    )

    assert (
        format_algorithm(
            parse_algorithm(
                notation,
            ),
        )
        == notation
    )


# ==============================================================================
# Empty Algorithm
# ==============================================================================

def test_empty_algorithm():
    algorithm = parse_algorithm(
        "",
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            algorithm,
        )
    )

    assert transformed == CANONICAL_CUBE_STATE


# ==============================================================================
# Contract
# ==============================================================================

def test_algorithm_workflow_contract():
    notation = (
        "R U R' U'"
    )

    algorithm = parse_algorithm(
        notation,
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            algorithm,
        )
    )

    formatted = format_algorithm(
        algorithm,
    )

    assert (
        formatted == notation
    )

    assert (
        transformed
        != CANONICAL_CUBE_STATE
    )