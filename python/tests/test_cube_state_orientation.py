from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import R
from cube.transformation import ROTATE_RIGHT


def test_transformed_cube_state_with_different_orientation_is_not_equal():
    rotated = CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROTATE_RIGHT,
    )

    assert rotated.orientation != CANONICAL_CUBE_STATE.orientation
    assert rotated != CANONICAL_CUBE_STATE


def test_move_preserves_cube_orientation():
    transformed = CubeTransformer.apply(CANONICAL_CUBE_STATE, R)

    assert transformed.orientation is CANONICAL_CUBE_STATE.orientation


def test_canonical_cube_state_is_solved():
    assert CANONICAL_CUBE_STATE.solved


def test_move_can_make_cube_unsolved():
    assert not CubeTransformer.apply(CANONICAL_CUBE_STATE, R).solved
