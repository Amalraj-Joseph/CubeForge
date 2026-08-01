import pytest

from cube.color.color import Color
from cube.orientation.cube_orientation import CubeOrientation


# ==============================================================================
# Test Data
# ==============================================================================

CANONICAL_ORIENTATION = CubeOrientation(
    up=Color.WHITE,
    down=Color.YELLOW,
    front=Color.GREEN,
    back=Color.BLUE,
    left=Color.ORANGE,
    right=Color.RED,
)

LEGAL_ORIENTATIONS = [
    # White Up
    (Color.WHITE, Color.GREEN),
    (Color.WHITE, Color.RED),
    (Color.WHITE, Color.BLUE),
    (Color.WHITE, Color.ORANGE),

    # Yellow Up
    (Color.YELLOW, Color.GREEN),
    (Color.YELLOW, Color.ORANGE),
    (Color.YELLOW, Color.BLUE),
    (Color.YELLOW, Color.RED),

    # Green Up
    (Color.GREEN, Color.WHITE),
    (Color.GREEN, Color.ORANGE),
    (Color.GREEN, Color.YELLOW),
    (Color.GREEN, Color.RED),

    # Blue Up
    (Color.BLUE, Color.WHITE),
    (Color.BLUE, Color.RED),
    (Color.BLUE, Color.YELLOW),
    (Color.BLUE, Color.ORANGE),

    # Red Up
    (Color.RED, Color.WHITE),
    (Color.RED, Color.GREEN),
    (Color.RED, Color.YELLOW),
    (Color.RED, Color.BLUE),

    # Orange Up
    (Color.ORANGE, Color.WHITE),
    (Color.ORANGE, Color.BLUE),
    (Color.ORANGE, Color.YELLOW),
    (Color.ORANGE, Color.GREEN),
]


# ==============================================================================
# Construction
# ==============================================================================

def test_create_cube_orientation():
    orientation = CANONICAL_ORIENTATION

    assert orientation.up is Color.WHITE
    assert orientation.down is Color.YELLOW

    assert orientation.front is Color.GREEN
    assert orientation.back is Color.BLUE

    assert orientation.left is Color.ORANGE
    assert orientation.right is Color.RED


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    ("up", "down", "front", "back", "left", "right"),
    [
        (
            Color.WHITE,
            Color.WHITE,
            Color.GREEN,
            Color.BLUE,
            Color.ORANGE,
            Color.RED,
        ),
        (
            Color.WHITE,
            Color.YELLOW,
            Color.GREEN,
            Color.GREEN,
            Color.ORANGE,
            Color.RED,
        ),
        (
            Color.WHITE,
            Color.YELLOW,
            Color.GREEN,
            Color.BLUE,
            Color.RED,
            Color.RED,
        ),
    ],
)
def test_duplicate_colors_are_invalid(
    up,
    down,
    front,
    back,
    left,
    right,
):
    with pytest.raises(ValueError):
        CubeOrientation(
            up,
            down,
            front,
            back,
            left,
            right,
        )


# ==============================================================================
# Aliases
# ==============================================================================

def test_top_alias():
    assert CANONICAL_ORIENTATION.top is CANONICAL_ORIENTATION.up


def test_bottom_alias():
    assert CANONICAL_ORIENTATION.bottom is CANONICAL_ORIENTATION.down


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equal_orientations():
    first = CubeOrientation(
        Color.WHITE,
        Color.YELLOW,
        Color.GREEN,
        Color.BLUE,
        Color.ORANGE,
        Color.RED,
    )

    second = CubeOrientation(
        Color.WHITE,
        Color.YELLOW,
        Color.GREEN,
        Color.BLUE,
        Color.ORANGE,
        Color.RED,
    )

    assert first == second
    assert hash(first) == hash(second)


def test_different_orientations():
    first = CubeOrientation(
        Color.WHITE,
        Color.YELLOW,
        Color.GREEN,
        Color.BLUE,
        Color.ORANGE,
        Color.RED,
    )

    second = CubeOrientation(
        Color.WHITE,
        Color.YELLOW,
        Color.RED,
        Color.ORANGE,
        Color.GREEN,
        Color.BLUE,
    )

    assert first != second


# ==============================================================================
# Representation
# ==============================================================================

def test_description():
    assert (
        CANONICAL_ORIENTATION.describe()
        == "Top=White, Front=Green"
    )


def test_string_representation():
    assert str(CANONICAL_ORIENTATION) == CANONICAL_ORIENTATION.describe()


# ==============================================================================
# Immutability
# ==============================================================================

def test_orientation_is_immutable():
    with pytest.raises(AttributeError):
        CANONICAL_ORIENTATION.up = Color.RED


# ==============================================================================
# Contract
# ==============================================================================

def test_contains_all_six_colors():
    colors = {
        CANONICAL_ORIENTATION.up,
        CANONICAL_ORIENTATION.down,
        CANONICAL_ORIENTATION.front,
        CANONICAL_ORIENTATION.back,
        CANONICAL_ORIENTATION.left,
        CANONICAL_ORIENTATION.right,
    }

    assert len(colors) == 6


def test_all_faces_are_colors():
    assert isinstance(CANONICAL_ORIENTATION.up, Color)
    assert isinstance(CANONICAL_ORIENTATION.down, Color)
    assert isinstance(CANONICAL_ORIENTATION.front, Color)
    assert isinstance(CANONICAL_ORIENTATION.back, Color)
    assert isinstance(CANONICAL_ORIENTATION.left, Color)
    assert isinstance(CANONICAL_ORIENTATION.right, Color)


# ==============================================================================
# Orientation Space
# ==============================================================================

def test_exactly_twenty_four_legal_top_front_pairs_exist():
    assert len(LEGAL_ORIENTATIONS) == 24


def test_every_legal_top_front_pair_is_unique():
    assert len(LEGAL_ORIENTATIONS) == len(set(LEGAL_ORIENTATIONS))


@pytest.mark.parametrize(("top", "front"), LEGAL_ORIENTATIONS)
def test_every_legal_orientation_has_distinct_top_and_front(top, front):
    assert top is not front


@pytest.mark.parametrize(("top", "front"), LEGAL_ORIENTATIONS)
def test_every_top_has_four_possible_fronts(top, front):
    fronts = {
        f
        for t, f in LEGAL_ORIENTATIONS
        if t is top
    }

    assert len(fronts) == 4