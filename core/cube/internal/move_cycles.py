from __future__ import annotations

from dataclasses import dataclass

from cube.internal.canonical_positions import (
    BL,
    BR,
    DB,
    DBR,
    DF,
    DFL,
    DL,
    DLB,
    DR,
    DRF,
    FL,
    FR,
    UB,
    UBL,
    UF,
    UFR,
    UL,
    ULF,
    UR,
    URB,
)
from cube.position.position import Position


@dataclass(frozen=True, slots=True)
class PositionCycle:
    """
    Immutable cyclic permutation of four Positions.
    """

    positions: tuple[Position, Position, Position, Position]

    def __post_init__(self) -> None:
        if len(set(self.positions)) != 4:
            raise ValueError(
                "A PositionCycle requires four unique Positions."
            )


# ==============================================================================
# U
# ==============================================================================

U_EDGE = PositionCycle(
    (
        UF,
        UR,
        UB,
        UL,
    )
)

U_CORNER = PositionCycle(
    (
        UFR,
        URB,
        UBL,
        ULF,
    )
)

# ==============================================================================
# D
# ==============================================================================

D_EDGE = PositionCycle(
    (
        DF,
        DR,
        DB,
        DL,
    )
)

D_CORNER = PositionCycle(
    (
        DFL,
        DRF,
        DBR,
        DLB,
    )
)

# ==============================================================================
# F
# ==============================================================================

F_EDGE = PositionCycle(
    (
        UF,
        FR,
        DF,
        FL,
    )
)

F_CORNER = PositionCycle(
    (
        UFR,
        DRF,
        DFL,
        ULF,
    )
)

# ==============================================================================
# B
# ==============================================================================

B_EDGE = PositionCycle(
    (
        UB,
        BL,
        DB,
        BR,
    )
)

B_CORNER = PositionCycle(
    (
        URB,
        UBL,
        DLB,
        DBR,
    )
)

# ==============================================================================
# L
# ==============================================================================

L_EDGE = PositionCycle(
    (
        UL,
        FL,
        DL,
        BL,
    )
)

L_CORNER = PositionCycle(
    (
        ULF,
        DFL,
        DLB,
        UBL,
    )
)

# ==============================================================================
# R
# ==============================================================================

R_EDGE = PositionCycle(
    (
        UR,
        BR,
        DR,
        FR,
    )
)

R_CORNER = PositionCycle(
    (
        UFR,
        URB,
        DBR,
        DRF,
    )
)

MOVE_CYCLES = (
    U_EDGE,
    U_CORNER,
    D_EDGE,
    D_CORNER,
    F_EDGE,
    F_CORNER,
    B_EDGE,
    B_CORNER,
    L_EDGE,
    L_CORNER,
    R_EDGE,
    R_CORNER,
)
