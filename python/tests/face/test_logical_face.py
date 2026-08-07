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
# Symbols
# ==============================================================================

@pytest.mark.parametrize(
    ("face", "symbol"),
    [
        (LogicalFace.UP, "U"),
        (LogicalFace.DOWN, "D"),
        (LogicalFace.FRONT, "F"),
        (LogicalFace.BACK, "B"),
        (LogicalFace.LEFT, "L"),
        (LogicalFace.RIGHT, "R"),
    ],
)
def test_symbol(face, symbol):
    assert face.symbol == symbol
    assert str(face) == symbol


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
# Ordering
# ==============================================================================

def test_bit_indices():
    assert LogicalFace.UP.bit_index == 0
    assert LogicalFace.DOWN.bit_index == 1
    assert LogicalFace.FRONT.bit_index == 2
    assert LogicalFace.BACK.bit_index == 3
    assert LogicalFace.LEFT.bit_index == 4
    assert LogicalFace.RIGHT.bit_index == 5


def test_bit_indices_are_unique():
    indices = {
        face.bit_index
        for face in LogicalFace
    }

    assert indices == {0, 1, 2, 3, 4, 5}


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


def test_opposites_are_symmetric():
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
        assert LogicalFace.from_symbol(face.symbol) is face


@pytest.mark.parametrize(
    "symbol",
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
def test_lookup_rejects_invalid_symbol(symbol):
    with pytest.raises((ValueError, TypeError)):
        LogicalFace.from_symbol(symbol)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality_and_hashing():
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
# Contract
# ==============================================================================

def test_logical_face_contract():
    symbols = set()
    indices = set()

    for face in LogicalFace:
        assert isinstance(face.symbol, str)
        assert isinstance(face.display_name, str)
        assert isinstance(face.axis, str)
        assert isinstance(face.bit_index, int)

        assert len(face.symbol) == 1
        assert face.display_name
        assert face.axis in {"X", "Y", "Z"}

        symbols.add(face.symbol)
        indices.add(face.bit_index)

    assert symbols == {"U", "D", "F", "B", "L", "R"}
    assert indices == {0, 1, 2, 3, 4, 5}
