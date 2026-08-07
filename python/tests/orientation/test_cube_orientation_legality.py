import pytest

from cube.color.color import Color
from cube.orientation.cube_orientation import CubeOrientation

LEGAL_TOP_FRONT_PAIRS = [
    (top, front)
    for top in Color
    for front in Color
    if front is not top and front is not top.opposite
]


def test_contains_exactly_twenty_four_legal_top_front_pairs():
    assert len(LEGAL_TOP_FRONT_PAIRS) == 24


@pytest.mark.parametrize(("top", "front"), LEGAL_TOP_FRONT_PAIRS)
def test_constructs_every_legal_orientation(top, front):
    orientation = CubeOrientation.from_top_front(top, front)

    assert orientation.top is top
    assert orientation.front is front
    assert orientation.bottom is top.opposite
    assert orientation.back is front.opposite


@pytest.mark.parametrize("top", Color)
def test_rejects_opposite_top_and_front_colors(top):
    with pytest.raises(ValueError):
        CubeOrientation.from_top_front(top, top.opposite)


def test_rejects_an_incorrect_left_right_completion():
    with pytest.raises(ValueError):
        CubeOrientation(
            up=Color.WHITE,
            down=Color.YELLOW,
            front=Color.GREEN,
            back=Color.BLUE,
            left=Color.RED,
            right=Color.ORANGE,
        )
