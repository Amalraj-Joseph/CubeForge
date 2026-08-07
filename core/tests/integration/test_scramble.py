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
from cube.scramble.scramble_generator import (
    ScrambleGenerator,
)

# ==============================================================================
# Execute
# ==============================================================================

def test_generated_scramble_is_executable():
    scramble = ScrambleGenerator.generate()

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            scramble,
        )
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
# Format -> Parse
# ==============================================================================

def test_generated_scramble_round_trip():
    scramble = ScrambleGenerator.generate()

    notation = format_algorithm(
        scramble,
    )

    parsed = parse_algorithm(
        notation,
    )

    assert parsed == scramble


# ==============================================================================
# Parse -> Execute
# ==============================================================================

def test_parsed_scramble_is_executable():
    scramble = ScrambleGenerator.generate()

    parsed = parse_algorithm(
        format_algorithm(scramble),
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            parsed,
        )
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
# End-to-End
# ==============================================================================

def test_complete_scramble_workflow():
    scramble = ScrambleGenerator.generate()

    notation = format_algorithm(
        scramble,
    )

    parsed = parse_algorithm(
        notation,
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            parsed,
        )
    )

    assert parsed == scramble

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
# Contract
# ==============================================================================

def test_scramble_workflow_contract():
    scramble = ScrambleGenerator.generate()

    notation = format_algorithm(
        scramble,
    )

    parsed = parse_algorithm(
        notation,
    )

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            parsed,
        )
    )

    assert format_algorithm(
        parsed,
    ) == notation

    assert len(parsed) == len(scramble)

    assert len(transformed) == 26

    assert all(
        state.piece in transformed
        for state in transformed
    )

    assert len({
        state.position
        for state in transformed
    }) == 26
