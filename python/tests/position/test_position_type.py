import pytest

from cube.position.position_type import PositionType


# ==============================================================================
# Enumeration
# ==============================================================================

def test_contains_exactly_three_position_types():
    assert list(PositionType) == [
        PositionType.CENTER,
        PositionType.EDGE,
        PositionType.CORNER,
    ]


# ==============================================================================
# Properties
# ==============================================================================

@pytest.mark.parametrize(
    ("position_type", "color_count"),
    [
        (PositionType.CENTER, 1),
        (PositionType.EDGE, 2),
        (PositionType.CORNER, 3),
    ],
)
def test_color_count(position_type, color_count):
    assert position_type.color_count == color_count


@pytest.mark.parametrize(
    ("position_type", "display"),
    [
        (PositionType.CENTER, "Center"),
        (PositionType.EDGE, "Edge"),
        (PositionType.CORNER, "Corner"),
    ],
)
def test_display(position_type, display):
    assert position_type.display_name == display
    assert position_type.describe() == display


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_identity_and_hashing():
    assert PositionType.CENTER is PositionType.CENTER
    assert PositionType.CENTER == PositionType.CENTER
    assert PositionType.CENTER != PositionType.EDGE

    position_types = {
        PositionType.CENTER,
        PositionType.EDGE,
    }

    assert PositionType.CENTER in position_types
    assert PositionType.EDGE in position_types


# ==============================================================================
# Representation
# ==============================================================================

def test_string_representation():
    assert str(PositionType.CENTER) == "CENTER"
    assert str(PositionType.EDGE) == "EDGE"
    assert str(PositionType.CORNER) == "CORNER"


# ==============================================================================
# Immutability
# ==============================================================================

def test_position_type_is_immutable():
    with pytest.raises(AttributeError):
        PositionType.CENTER.color_count = 99


# ==============================================================================
# Contract
# ==============================================================================

def test_position_type_contract():
    for position_type in PositionType:
        assert isinstance(position_type.color_count, int)
        assert isinstance(position_type.display_name, str)

        assert position_type.color_count in {1, 2, 3}
        assert position_type.display_name