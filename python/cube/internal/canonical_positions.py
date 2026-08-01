from cube.face.logical_face import LogicalFace
from cube.position.position import Position
from cube.position.position_type import PositionType


# ==============================================================================
# Centers
# ==============================================================================

U = Position(
    PositionType.CENTER,
    LogicalFace.UP,
)

D = Position(
    PositionType.CENTER,
    LogicalFace.DOWN,
)

F = Position(
    PositionType.CENTER,
    LogicalFace.FRONT,
)

B = Position(
    PositionType.CENTER,
    LogicalFace.BACK,
)

L = Position(
    PositionType.CENTER,
    LogicalFace.LEFT,
)

R = Position(
    PositionType.CENTER,
    LogicalFace.RIGHT,
)


# ==============================================================================
# Edges
# ==============================================================================

UF = Position(
    PositionType.EDGE,
    LogicalFace.UP,
    LogicalFace.FRONT,
)

UR = Position(
    PositionType.EDGE,
    LogicalFace.UP,
    LogicalFace.RIGHT,
)

UB = Position(
    PositionType.EDGE,
    LogicalFace.UP,
    LogicalFace.BACK,
)

UL = Position(
    PositionType.EDGE,
    LogicalFace.UP,
    LogicalFace.LEFT,
)

FR = Position(
    PositionType.EDGE,
    LogicalFace.FRONT,
    LogicalFace.RIGHT,
)

FL = Position(
    PositionType.EDGE,
    LogicalFace.FRONT,
    LogicalFace.LEFT,
)

BR = Position(
    PositionType.EDGE,
    LogicalFace.BACK,
    LogicalFace.RIGHT,
)

BL = Position(
    PositionType.EDGE,
    LogicalFace.BACK,
    LogicalFace.LEFT,
)

DF = Position(
    PositionType.EDGE,
    LogicalFace.DOWN,
    LogicalFace.FRONT,
)

DR = Position(
    PositionType.EDGE,
    LogicalFace.DOWN,
    LogicalFace.RIGHT,
)

DB = Position(
    PositionType.EDGE,
    LogicalFace.DOWN,
    LogicalFace.BACK,
)

DL = Position(
    PositionType.EDGE,
    LogicalFace.DOWN,
    LogicalFace.LEFT,
)


# ==============================================================================
# Corners
# ==============================================================================

UFR = Position(
    PositionType.CORNER,
    LogicalFace.UP,
    LogicalFace.FRONT,
    LogicalFace.RIGHT,
)

URB = Position(
    PositionType.CORNER,
    LogicalFace.UP,
    LogicalFace.RIGHT,
    LogicalFace.BACK,
)

UBL = Position(
    PositionType.CORNER,
    LogicalFace.UP,
    LogicalFace.BACK,
    LogicalFace.LEFT,
)

ULF = Position(
    PositionType.CORNER,
    LogicalFace.UP,
    LogicalFace.LEFT,
    LogicalFace.FRONT,
)

DFL = Position(
    PositionType.CORNER,
    LogicalFace.DOWN,
    LogicalFace.FRONT,
    LogicalFace.LEFT,
)

DRF = Position(
    PositionType.CORNER,
    LogicalFace.DOWN,
    LogicalFace.RIGHT,
    LogicalFace.FRONT,
)

DBR = Position(
    PositionType.CORNER,
    LogicalFace.DOWN,
    LogicalFace.BACK,
    LogicalFace.RIGHT,
)

DLB = Position(
    PositionType.CORNER,
    LogicalFace.DOWN,
    LogicalFace.LEFT,
    LogicalFace.BACK,
)


# ==============================================================================
# Collections
# ==============================================================================

CENTER_POSITIONS = (
    U,
    D,
    F,
    B,
    L,
    R,
)

EDGE_POSITIONS = (
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
)

CORNER_POSITIONS = (
    UFR,
    URB,
    UBL,
    ULF,
    DFL,
    DRF,
    DBR,
    DLB,
)

ALL_POSITIONS = (
    *CENTER_POSITIONS,
    *EDGE_POSITIONS,
    *CORNER_POSITIONS,
)