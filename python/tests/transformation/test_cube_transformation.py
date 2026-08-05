from collections import deque

from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import R
from cube.internal.canonical_positions import F, U
from cube.transformation import (
    ROLL_CLOCKWISE,
    ROLL_COUNTERCLOCKWISE,
    ROTATE_DOWN,
    ROTATE_LEFT,
    ROTATE_RIGHT,
    ROTATE_UP,
)


PRIMITIVES = (
    ROTATE_LEFT,
    ROTATE_RIGHT,
    ROTATE_UP,
    ROTATE_DOWN,
    ROLL_CLOCKWISE,
    ROLL_COUNTERCLOCKWISE,
)


INVERSES = (
    (ROTATE_LEFT, ROTATE_RIGHT),
    (ROTATE_UP, ROTATE_DOWN),
    (ROLL_CLOCKWISE, ROLL_COUNTERCLOCKWISE),
)


def test_rotate_up_updates_orientation_as_specified():
    transformed = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROTATE_UP,
    )

    assert transformed.orientation.top.name == "BLUE"
    assert transformed.orientation.front.name == "WHITE"


def test_rotate_up_rewrites_piece_positions():
    transformed = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROTATE_UP,
    )

    assert transformed.piece_at(F).piece is CANONICAL_CUBE_STATE.piece_at(U).piece


def test_every_primitive_preserves_solvedness_and_piece_identity():
    for transformation in PRIMITIVES:
        transformed = CubeTransformer.apply_transformation(
            CANONICAL_CUBE_STATE,
            transformation,
        )

        assert transformed.solved
        assert len(transformed) == 26
        assert len({state.position for state in transformed}) == 26
        assert {
            state.piece.signature
            for state in transformed
        } == {
            state.piece.signature
            for state in CANONICAL_CUBE_STATE
        }
        assert {
            state.piece_type
            for state in transformed
        } == {
            state.piece_type
            for state in CANONICAL_CUBE_STATE
        }


def test_transformation_preserves_an_unsolved_cube():
    scrambled = CubeTransformer.apply(CANONICAL_CUBE_STATE, R)
    transformed = CubeTransformer.apply_transformation(
        scrambled,
        ROTATE_RIGHT,
    )

    assert not scrambled.solved
    assert not transformed.solved


def test_each_primitive_inverse_restores_the_original_cube_state():
    for transformation, inverse in INVERSES:
        transformed = CubeTransformer.apply_transformations(
            CANONICAL_CUBE_STATE,
            transformation,
            inverse,
        )

        assert transformation.inverse() == inverse
        assert transformed == CANONICAL_CUBE_STATE


def test_composition_is_sequential_from_left_to_right():
    composed = ROTATE_LEFT.then(ROTATE_UP)

    sequential = CubeTransformer.apply_transformations(
        CANONICAL_CUBE_STATE,
        ROTATE_LEFT,
        ROTATE_UP,
    )
    transformed = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        composed,
    )

    assert transformed == sequential


def test_primitive_transformations_reach_all_twenty_four_orientations():
    queue = deque([CANONICAL_CUBE_STATE])
    orientations = set()

    while queue:
        cube = queue.popleft()

        if cube.orientation in orientations:
            continue

        orientations.add(cube.orientation)

        for transformation in PRIMITIVES:
            queue.append(
                CubeTransformer.apply_transformation(cube, transformation)
            )

    assert len(orientations) == 24


def test_transformation_application_is_deterministic():
    first = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROLL_CLOCKWISE,
    )
    second = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROLL_CLOCKWISE,
    )

    assert first == second
