from cube import Cube, SPECIFICATION_VERSION
from cube.internal.canonical_moves import R
from cube.transformation import ROTATE_UP


def test_constructs_a_canonical_cube():
    cube = Cube.canonical()

    assert cube.solved
    assert len(cube.state) == 26
    assert SPECIFICATION_VERSION == "v1"


def test_cube_facade_applies_moves_and_transformations():
    moved = Cube.canonical().apply(R)
    transformed = moved.apply_transformation(ROTATE_UP)

    assert not moved.solved
    assert not transformed.solved
    assert transformed.orientation.top.name == "BLUE"


def test_cube_and_piece_state_descriptions_are_human_readable():
    cube = Cube.canonical()

    assert "Orientation:" in cube.describe()
    assert "Piece=" in cube.describe()
