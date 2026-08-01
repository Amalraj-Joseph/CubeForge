from types import MappingProxyType

from cube.internal.canonical_pieces import (
    WHITE_CENTER,
    YELLOW_CENTER,
    GREEN_CENTER,
    BLUE_CENTER,
    ORANGE_CENTER,
    RED_CENTER,

    WHITE_GREEN_EDGE,
    WHITE_RED_EDGE,
    WHITE_BLUE_EDGE,
    WHITE_ORANGE_EDGE,

    GREEN_RED_EDGE,
    GREEN_ORANGE_EDGE,

    BLUE_RED_EDGE,
    BLUE_ORANGE_EDGE,

    YELLOW_GREEN_EDGE,
    YELLOW_RED_EDGE,
    YELLOW_BLUE_EDGE,
    YELLOW_ORANGE_EDGE,

    WHITE_GREEN_RED_CORNER,
    WHITE_RED_BLUE_CORNER,
    WHITE_BLUE_ORANGE_CORNER,
    WHITE_ORANGE_GREEN_CORNER,

    YELLOW_GREEN_ORANGE_CORNER,
    YELLOW_RED_GREEN_CORNER,
    YELLOW_BLUE_RED_CORNER,
    YELLOW_ORANGE_BLUE_CORNER,
)
from cube.internal.canonical_positions import (
    U,
    D,
    F,
    B,
    L,
    R,

    UF,
    UR,
    UB,
    UL,

    FR,
    FL,
    BR,
    BL,

    DF,
    DR,
    DB,
    DL,

    UFR,
    URB,
    UBL,
    ULF,

    DFL,
    DRF,
    DBR,
    DLB,
)


_CANONICAL_CUBE = {
    # ==========================================================================
    # Centers
    # ==========================================================================

    WHITE_CENTER: U,
    YELLOW_CENTER: D,

    GREEN_CENTER: F,
    BLUE_CENTER: B,

    ORANGE_CENTER: L,
    RED_CENTER: R,

    # ==========================================================================
    # Edges
    # ==========================================================================

    WHITE_GREEN_EDGE: UF,
    WHITE_RED_EDGE: UR,
    WHITE_BLUE_EDGE: UB,
    WHITE_ORANGE_EDGE: UL,

    GREEN_RED_EDGE: FR,
    GREEN_ORANGE_EDGE: FL,

    BLUE_RED_EDGE: BR,
    BLUE_ORANGE_EDGE: BL,

    YELLOW_GREEN_EDGE: DF,
    YELLOW_RED_EDGE: DR,
    YELLOW_BLUE_EDGE: DB,
    YELLOW_ORANGE_EDGE: DL,

    # ==========================================================================
    # Corners
    # ==========================================================================

    WHITE_GREEN_RED_CORNER: UFR,
    WHITE_RED_BLUE_CORNER: URB,
    WHITE_BLUE_ORANGE_CORNER: UBL,
    WHITE_ORANGE_GREEN_CORNER: ULF,

    YELLOW_GREEN_ORANGE_CORNER: DFL,
    YELLOW_RED_GREEN_CORNER: DRF,
    YELLOW_BLUE_RED_CORNER: DBR,
    YELLOW_ORANGE_BLUE_CORNER: DLB,
}

CANONICAL_CUBE = MappingProxyType(_CANONICAL_CUBE)