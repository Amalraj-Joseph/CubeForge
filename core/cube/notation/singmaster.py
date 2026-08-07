from cube.internal import canonical_positions as cp
from cube.position.position import Position

_POSITION_TO_NOTATION = {
    cp.U: "U",
    cp.D: "D",
    cp.F: "F",
    cp.B: "B",
    cp.L: "L",
    cp.R: "R",

    cp.UF: "UF",
    cp.UR: "UR",
    cp.UB: "UB",
    cp.UL: "UL",

    cp.FR: "FR",
    cp.FL: "FL",
    cp.BR: "BR",
    cp.BL: "BL",

    cp.DF: "DF",
    cp.DR: "DR",
    cp.DB: "DB",
    cp.DL: "DL",

    cp.UFR: "UFR",
    cp.URB: "URB",
    cp.UBL: "UBL",
    cp.ULF: "ULF",

    cp.DFL: "DFL",
    cp.DRF: "DRF",
    cp.DBR: "DBR",
    cp.DLB: "DLB",
}

_NOTATION_TO_POSITION = {
    notation: position
    for position, notation in _POSITION_TO_NOTATION.items()
}


def to_position_notation(position: Position) -> str:
    """
    Returns the canonical Singmaster notation for a Position.
    """
    try:
        return _POSITION_TO_NOTATION[position]
    except KeyError as ex:
        raise ValueError(
            f"Unknown canonical position: {position!r}"
        ) from ex


def from_position_notation(notation: str) -> Position:
    """
    Returns the Position represented by the given
    Singmaster notation.
    """
    try:
        return _NOTATION_TO_POSITION[notation]
    except KeyError as ex:
        raise ValueError(
            f"Unknown position notation: {notation}"
        ) from ex
