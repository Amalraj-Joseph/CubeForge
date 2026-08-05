from cube import Cube, SPECIFICATION_VERSION
from cube.algorithm.algorithm import Algorithm
from cube.internal.canonical_moves import R
from cube.transformation import ROTATE_UP
from cube.validation import CubeStateValidator


def test_public_api_supports_required_cube_operations():
    cube = Cube.canonical()
    moved = cube.apply(R)
    transformed = cube.apply_algorithm(Algorithm(R)).apply_transformation(
        ROTATE_UP,
    )

    assert SPECIFICATION_VERSION == "v1"
    assert cube.solved
    assert not moved.solved
    assert CubeStateValidator.is_valid(transformed.state)
