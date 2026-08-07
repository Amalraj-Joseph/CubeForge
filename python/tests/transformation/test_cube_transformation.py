from collections import deque

import pytest

from cube.cube_transformer import CubeTransformer
from cube.face.logical_face import LogicalFace
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
from cube.transformation.cube_transformation import CubeTransformation

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


# ==============================================================================
# Construction validation
# ==============================================================================

def test_rejects_a_mapping_missing_a_face():
    incomplete = {
        face: face
        for face in LogicalFace
        if face is not LogicalFace.UP
    }

    with pytest.raises(ValueError, match="every LogicalFace exactly once"):
        CubeTransformation(incomplete)


def test_rejects_a_non_bijective_mapping():
    not_bijective = {face: LogicalFace.UP for face in LogicalFace}

    with pytest.raises(ValueError, match="bijective"):
        CubeTransformation(not_bijective)


def test_rejects_a_mapping_that_does_not_preserve_opposite_faces():
    breaks_opposites = {
        LogicalFace.UP: LogicalFace.RIGHT,
        LogicalFace.RIGHT: LogicalFace.UP,
        LogicalFace.DOWN: LogicalFace.DOWN,
        LogicalFace.LEFT: LogicalFace.LEFT,
        LogicalFace.FRONT: LogicalFace.FRONT,
        LogicalFace.BACK: LogicalFace.BACK,
    }

    with pytest.raises(ValueError, match="preserve opposite faces"):
        CubeTransformation(breaks_opposites)


def test_rejects_a_mapping_that_does_not_preserve_handedness():
    mirror_reflection = {
        LogicalFace.UP: LogicalFace.UP,
        LogicalFace.DOWN: LogicalFace.DOWN,
        LogicalFace.FRONT: LogicalFace.FRONT,
        LogicalFace.BACK: LogicalFace.BACK,
        LogicalFace.LEFT: LogicalFace.RIGHT,
        LogicalFace.RIGHT: LogicalFace.LEFT,
    }

    with pytest.raises(ValueError, match="handedness"):
        CubeTransformation(mirror_reflection)


# ==============================================================================
# Name & Description
# ==============================================================================

def test_named_transformation_exposes_its_name():
    assert ROTATE_UP.name == "rotate_up"


def test_unnamed_transformation_describes_its_face_mapping():
    identity = CubeTransformation({face: face for face in LogicalFace})

    assert identity.name is None
    assert identity.describe().startswith("Cube Transformation(")
    assert "U->U" in identity.describe()


def test_unnamed_transformation_string_representation_matches_describe():
    identity = CubeTransformation({face: face for face in LogicalFace})

    assert str(identity) == identity.describe()
