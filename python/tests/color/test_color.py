import pytest

from cube.color.color import Color


# ==============================================================================
# Enumeration
# ==============================================================================

def test_contains_exactly_six_colors():
    assert list(Color) == [
        Color.WHITE,
        Color.YELLOW,
        Color.GREEN,
        Color.BLUE,
        Color.RED,
        Color.ORANGE,
    ]


# ==============================================================================
# Masks
# ==============================================================================

def test_masks_are_unique_single_bits():
    masks = set()

    for color in Color:
        mask = color.mask

        # Unique
        assert mask not in masks
        masks.add(mask)

        # Exactly one bit set
        assert mask > 0
        assert mask & (mask - 1) == 0

    assert masks == {
        0b000001,
        0b000010,
        0b000100,
        0b001000,
        0b010000,
        0b100000,
    }


# ==============================================================================
# Bit Index
# ==============================================================================

def test_bit_index_matches_mask():
    for color in Color:
        assert color.mask == (1 << color.bit_index)


# ==============================================================================
# Display
# ==============================================================================

@pytest.mark.parametrize(
    ("color", "display"),
    [
        (Color.WHITE, "White"),
        (Color.YELLOW, "Yellow"),
        (Color.GREEN, "Green"),
        (Color.BLUE, "Blue"),
        (Color.RED, "Red"),
        (Color.ORANGE, "Orange"),
    ],
)
def test_display_name_and_description(color, display):
    assert color.display_name == display
    assert color.describe() == display


# ==============================================================================
# Opposites
# ==============================================================================

@pytest.mark.parametrize(
    ("color", "opposite"),
    [
        (Color.WHITE, Color.YELLOW),
        (Color.GREEN, Color.BLUE),
        (Color.RED, Color.ORANGE),
    ],
)
def test_opposite_colors(color, opposite):
    assert color.opposite is opposite
    assert opposite.opposite is color


# ==============================================================================
# Lookup
# ==============================================================================

def test_lookup_round_trip():
    for color in Color:
        assert Color.from_mask(color.mask) is color


@pytest.mark.parametrize(
    "mask",
    [
        0,
        0b000011,
        0b000101,
        0b001100,
        0b111111,
        64,
        -1,
    ],
)
def test_lookup_rejects_invalid_masks(mask):
    with pytest.raises(ValueError):
        Color.from_mask(mask)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_enum_identity_and_hashing():
    assert Color.WHITE is Color.WHITE
    assert Color.WHITE == Color.WHITE
    assert Color.WHITE != Color.YELLOW

    colors = {Color.WHITE, Color.GREEN}

    assert Color.WHITE in colors
    assert Color.GREEN in colors


# ==============================================================================
# Representation
# ==============================================================================

def test_string_representation():
    assert str(Color.WHITE) == "WHITE"
    assert str(Color.ORANGE) == "ORANGE"


# ==============================================================================
# Immutability
# ==============================================================================

def test_color_is_immutable():
    with pytest.raises(AttributeError):
        Color.WHITE.mask = 123


# ==============================================================================
# Contract
# ==============================================================================

def test_color_contract():
    combined_mask = 0

    for color in Color:
        assert isinstance(color.mask, int)
        assert isinstance(color.bit_index, int)
        assert isinstance(color.display_name, str)

        combined_mask |= color.mask

    # Every bit is represented exactly once.
    assert combined_mask == 0b111111
