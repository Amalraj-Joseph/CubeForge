import pytest

from cube.algorithm.algorithm import Algorithm
from cube.move.move import Move
from cube.scramble.scramble_generator import (
    ScrambleGenerator,
)

# ==============================================================================
# Construction
# ==============================================================================

def test_default_scramble():
    scramble = ScrambleGenerator.generate()

    assert isinstance(
        scramble,
        Algorithm,
    )

    assert (
        len(scramble)
        == ScrambleGenerator.DEFAULT_LENGTH
    )


def test_custom_length():
    scramble = ScrambleGenerator.generate(
        10,
    )

    assert len(scramble) == 10


def test_zero_length():
    scramble = ScrambleGenerator.generate(
        0,
    )

    assert scramble == Algorithm()


# ==============================================================================
# Validation
# ==============================================================================

def test_negative_length():
    with pytest.raises(ValueError):
        ScrambleGenerator.generate(
            -1,
        )


# ==============================================================================
# Moves
# ==============================================================================

def test_all_elements_are_moves():
    scramble = ScrambleGenerator.generate()

    assert all(
        isinstance(
            move,
            Move,
        )
        for move in scramble
    )


def test_no_consecutive_same_face():
    scramble = ScrambleGenerator.generate(
        100,
    )

    for previous, current in zip(
        scramble,
        scramble[1:],
        strict=False,
    ):
        assert (
            previous.face
            is not current.face
        )


# ==============================================================================
# Randomness Properties
# ==============================================================================

def test_generates_new_algorithm():
    first = ScrambleGenerator.generate()

    second = ScrambleGenerator.generate()

    assert first is not second


def test_generated_scramble_is_executable():
    from cube.cube_transformer import (
        CubeTransformer,
    )
    from cube.internal.canonical_cube_state import (
        CANONICAL_CUBE_STATE,
    )

    scramble = ScrambleGenerator.generate()

    transformed = (
        CubeTransformer.apply_algorithm(
            CANONICAL_CUBE_STATE,
            scramble,
        )
    )

    assert len(transformed) == 26


# ==============================================================================
# Contract
# ==============================================================================

def test_scramble_generator_contract():
    scramble = ScrambleGenerator.generate()

    assert isinstance(
        scramble,
        Algorithm,
    )

    assert len(scramble) == (
        ScrambleGenerator.DEFAULT_LENGTH
    )

    assert all(
        isinstance(
            move,
            Move,
        )
        for move in scramble
    )

    for previous, current in zip(
        scramble,
        scramble[1:],
        strict=False,
    ):
        assert (
            previous.face
            is not current.face
        )
