import pytest

from cube.face.logical_face import LogicalFace


# ==============================================================================
# Enumeration
# ==============================================================================

def test_contains_exactly_six_faces():
    assert list(LogicalFace) == [
        LogicalFace.UP,
        LogicalFace.DOWN,
        LogicalFace.FRONT,
        LogicalFace.BACK,
        LogicalFace.LEFT,
        LogicalFace.RIGHT,
    ]


# ==============================================================================
# Notation
# ==============================================================================

@pytest.mark.parametrize(
    ("face", "notation"),
    [
        (LogicalFace.UP, "U"),
        (LogicalFace.DOWN, "D"),
        (LogicalFace.FRONT, "F"),
        (LogicalFace.BACK, "B"),
        (LogicalFace.LEFT, "L"),
        (LogicalFace.RIGHT, "R"),
    ],
)
def test_notation(face, notation):
    assert face.notation == notation
    assert str(face) == notation


# ==============================================================================
# Display
# ==============================================================================

@pytest.mark.parametrize(
    ("face", "display_name"),
    [
        (LogicalFace.UP, "Up"),
        (LogicalFace.DOWN, "Down"),
        (LogicalFace.FRONT, "Front"),
        (LogicalFace.BACK, "Back"),
        (LogicalFace.LEFT, "Left"),
        (LogicalFace.RIGHT, "Right"),
    ],
)
def test_display_name_and_description(face, display_name):
    assert face.display_name == display_name
    assert face.describe() == display_name


# ==============================================================================
# Opposites
# ==============================================================================

@pytest.mark.parametrize(
    ("face", "opposite"),
    [
        (LogicalFace.UP, LogicalFace.DOWN),
        (LogicalFace.DOWN, LogicalFace.UP),
        (LogicalFace.FRONT, LogicalFace.BACK),
        (LogicalFace.BACK, LogicalFace.FRONT),
        (LogicalFace.LEFT, LogicalFace.RIGHT),
        (LogicalFace.RIGHT, LogicalFace.LEFT),
    ],
)
def test_opposite(face, opposite):
    assert face.opposite is opposite


def test_opposite_is_symmetric():
    for face in LogicalFace:
        assert face.opposite.opposite is face


# ==============================================================================
# Axes
# ==============================================================================

@pytest.mark.parametrize(
    ("face", "axis"),
    [
        (LogicalFace.UP, "Y"),
        (LogicalFace.DOWN, "Y"),
        (LogicalFace.FRONT, "Z"),
        (LogicalFace.BACK, "Z"),
        (LogicalFace.LEFT, "X"),
        (LogicalFace.RIGHT, "X"),
    ],
)
def test_axis(face, axis):
    assert face.axis == axis


# ==============================================================================
# Lookup
# ==============================================================================

def test_lookup_round_trip():
    for face in LogicalFace:
        assert LogicalFace.from_notation(face.notation) is face


@pytest.mark.parametrize(
    "notation",
    [
        "",
        "A",
        "X",
        "u",
        "f",
        "UP",
        "Front",
        "1",
        None,
    ],
)
def test_lookup_rejects_invalid_notation(notation):
    with pytest.raises((ValueError, TypeError)):
        LogicalFace.from_notation(notation)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_identity_and_hashing():
    assert LogicalFace.UP is LogicalFace.UP
    assert LogicalFace.UP == LogicalFace.UP
    assert LogicalFace.UP != LogicalFace.DOWN

    faces = {
        LogicalFace.UP,
        LogicalFace.FRONT,
        LogicalFace.LEFT,
    }

    assert LogicalFace.UP in faces
    assert LogicalFace.FRONT in faces
    assert LogicalFace.LEFT in faces


# ==============================================================================
# Immutability
# ==============================================================================

def test_logical_face_is_immutable():
    with pytest.raises(AttributeError):
        LogicalFace.UP.notation = "TOP"


# ==============================================================================
# Contract
# ==============================================================================

def test_logical_face_contract():
    notations = set()

    for face in LogicalFace:
        assert isinstance(face.notation, str)
        assert isinstance(face.display_name, str)
        assert isinstance(face.axis, str)

        assert len(face.notation) == 1
        assert face.display_name
        assert face.axis in {"X", "Y", "Z"}

        notations.add(face.notation)

    assert notations == {"U", "D", "F", "B", "L", "R"}