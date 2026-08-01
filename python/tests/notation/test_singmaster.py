import pytest

from cube.internal import canonical_positions as cp
from cube.notation.singmaster import (
    from_position_notation,
    to_position_notation,
)


# ==============================================================================
# Position → Notation
# ==============================================================================

@pytest.mark.parametrize(
    ("position", "notation"),
    [
        (cp.U, "U"),
        (cp.D, "D"),
        (cp.F, "F"),
        (cp.B, "B"),
        (cp.L, "L"),
        (cp.R, "R"),

        (cp.UF, "UF"),
        (cp.UR, "UR"),
        (cp.UB, "UB"),
        (cp.UL, "UL"),

        (cp.FR, "FR"),
        (cp.FL, "FL"),
        (cp.BR, "BR"),
        (cp.BL, "BL"),

        (cp.DF, "DF"),
        (cp.DR, "DR"),
        (cp.DB, "DB"),
        (cp.DL, "DL"),

        (cp.UFR, "UFR"),
        (cp.URB, "URB"),
        (cp.UBL, "UBL"),
        (cp.ULF, "ULF"),

        (cp.DFL, "DFL"),
        (cp.DRF, "DRF"),
        (cp.DBR, "DBR"),
        (cp.DLB, "DLB"),
    ],
)
def test_to_position_notation(position, notation):
    assert to_position_notation(position) == notation


# ==============================================================================
# Notation → Position
# ==============================================================================

@pytest.mark.parametrize(
    "position",
    cp.ALL_POSITIONS,
)
def test_round_trip(position):
    notation = to_position_notation(position)

    assert from_position_notation(notation) is position


# ==============================================================================
# Validation
# ==============================================================================

@pytest.mark.parametrize(
    "notation",
    [
        "",
        "XYZ",
        "UU",
        "URF",
        "XYZ",
        None,
    ],
)
def test_invalid_position_notation(notation):
    with pytest.raises((ValueError, TypeError)):
        from_position_notation(notation)