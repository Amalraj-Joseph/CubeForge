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
    ("position_type", "face_count"),
    [
        (PositionType.CENTER, 1),
        (PositionType.EDGE, 2),
        (PositionType.CORNER, 3),
    ],
)
def test_face_count(position_type, face_count):
    assert position_type.face_count == face_count


@pytest.mark.parametrize(
    ("position_type", "display_name"),
    [
        (PositionType.CENTER, "Center"),
        (PositionType.EDGE, "Edge"),
        (PositionType.CORNER, "Corner"),
    ],
)
def test_display_name_and_description(position_type, display_name):
    assert position_type.display_name == display_name
    assert position_type.describe() == display_name


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_and_hashing():
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
# Contract
# ==============================================================================

def test_position_type_contract():
    face_counts = set()

    for position_type in PositionType:
        assert isinstance(position_type.face_count, int)
        assert isinstance(position_type.display_name, str)

        assert position_type.face_count in {1, 2, 3}
        assert position_type.display_name

        face_counts.add(position_type.face_count)

    assert face_counts == {1, 2, 3}
