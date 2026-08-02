import pytest

from cube.move.rotation import Rotation


# ==============================================================================
# Enumeration
# ==============================================================================

def test_contains_exactly_three_rotations():
    assert list(Rotation) == [
        Rotation.CLOCKWISE,
        Rotation.HALF_TURN,
        Rotation.COUNTERCLOCKWISE,
    ]


# ==============================================================================
# Properties
# ==============================================================================

@pytest.mark.parametrize(
    ("rotation", "notation"),
    [
        (Rotation.CLOCKWISE, ""),
        (Rotation.HALF_TURN, "2"),
        (Rotation.COUNTERCLOCKWISE, "'"),
    ],
)
def test_notation(rotation, notation):
    assert rotation.notation == notation


@pytest.mark.parametrize(
    ("rotation", "turns"),
    [
        (Rotation.CLOCKWISE, 1),
        (Rotation.HALF_TURN, 2),
        (Rotation.COUNTERCLOCKWISE, 3),
    ],
)
def test_quarter_turns(rotation, turns):
    assert rotation.quarter_turns == turns


def test_inverse():
    assert (
        Rotation.CLOCKWISE.inverse
        is Rotation.COUNTERCLOCKWISE
    )

    assert (
        Rotation.COUNTERCLOCKWISE.inverse
        is Rotation.CLOCKWISE
    )

    assert (
        Rotation.HALF_TURN.inverse
        is Rotation.HALF_TURN
    )


# ==============================================================================
# Display
# ==============================================================================

@pytest.mark.parametrize(
    ("rotation", "display"),
    [
        (
            Rotation.CLOCKWISE,
            "Clockwise",
        ),
        (
            Rotation.HALF_TURN,
            "Half Turn",
        ),
        (
            Rotation.COUNTERCLOCKWISE,
            "Counterclockwise",
        ),
    ],
)
def test_display(rotation, display):
    assert rotation.display_name == display
    assert rotation.describe() == display


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_and_hashing():
    assert (
        Rotation.CLOCKWISE
        is Rotation.CLOCKWISE
    )

    assert (
        Rotation.CLOCKWISE
        != Rotation.HALF_TURN
    )

    rotations = {
        Rotation.CLOCKWISE,
        Rotation.HALF_TURN,
    }

    assert Rotation.CLOCKWISE in rotations
    assert Rotation.HALF_TURN in rotations


# ==============================================================================
# Representation
# ==============================================================================

def test_string_representation():
    assert str(Rotation.CLOCKWISE) == "CLOCKWISE"
    assert str(Rotation.HALF_TURN) == "HALF_TURN"
    assert (
        str(Rotation.COUNTERCLOCKWISE)
        == "COUNTERCLOCKWISE"
    )


# ==============================================================================
# Contract
# ==============================================================================

def test_rotation_contract():
    assert {
        rotation.quarter_turns
        for rotation in Rotation
    } == {1, 2, 3}

    assert {
        rotation.notation
        for rotation in Rotation
    } == {"", "2", "'"}

    for rotation in Rotation:
        assert isinstance(
            rotation.notation,
            str,
        )

        assert isinstance(
            rotation.quarter_turns,
            int,
        )

        assert (
            rotation.inverse.inverse
            is rotation
        )