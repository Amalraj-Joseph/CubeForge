from cube.face.logical_face import LogicalFace
from cube.move.move import Move
from cube.move.rotation import Rotation

# ==============================================================================
# Up
# ==============================================================================

U = Move(
    LogicalFace.UP,
    Rotation.CLOCKWISE,
)

U2 = Move(
    LogicalFace.UP,
    Rotation.HALF_TURN,
)

U_PRIME = Move(
    LogicalFace.UP,
    Rotation.COUNTERCLOCKWISE,
)


# ==============================================================================
# Down
# ==============================================================================

D = Move(
    LogicalFace.DOWN,
    Rotation.CLOCKWISE,
)

D2 = Move(
    LogicalFace.DOWN,
    Rotation.HALF_TURN,
)

D_PRIME = Move(
    LogicalFace.DOWN,
    Rotation.COUNTERCLOCKWISE,
)


# ==============================================================================
# Front
# ==============================================================================

F = Move(
    LogicalFace.FRONT,
    Rotation.CLOCKWISE,
)

F2 = Move(
    LogicalFace.FRONT,
    Rotation.HALF_TURN,
)

F_PRIME = Move(
    LogicalFace.FRONT,
    Rotation.COUNTERCLOCKWISE,
)


# ==============================================================================
# Back
# ==============================================================================

B = Move(
    LogicalFace.BACK,
    Rotation.CLOCKWISE,
)

B2 = Move(
    LogicalFace.BACK,
    Rotation.HALF_TURN,
)

B_PRIME = Move(
    LogicalFace.BACK,
    Rotation.COUNTERCLOCKWISE,
)


# ==============================================================================
# Left
# ==============================================================================

L = Move(
    LogicalFace.LEFT,
    Rotation.CLOCKWISE,
)

L2 = Move(
    LogicalFace.LEFT,
    Rotation.HALF_TURN,
)

L_PRIME = Move(
    LogicalFace.LEFT,
    Rotation.COUNTERCLOCKWISE,
)


# ==============================================================================
# Right
# ==============================================================================

R = Move(
    LogicalFace.RIGHT,
    Rotation.CLOCKWISE,
)

R2 = Move(
    LogicalFace.RIGHT,
    Rotation.HALF_TURN,
)

R_PRIME = Move(
    LogicalFace.RIGHT,
    Rotation.COUNTERCLOCKWISE,
)


# ==============================================================================
# Collections
# ==============================================================================

UP_MOVES = (
    U,
    U2,
    U_PRIME,
)

DOWN_MOVES = (
    D,
    D2,
    D_PRIME,
)

FRONT_MOVES = (
    F,
    F2,
    F_PRIME,
)

BACK_MOVES = (
    B,
    B2,
    B_PRIME,
)

LEFT_MOVES = (
    L,
    L2,
    L_PRIME,
)

RIGHT_MOVES = (
    R,
    R2,
    R_PRIME,
)

ALL_MOVES = (
    *UP_MOVES,
    *DOWN_MOVES,
    *FRONT_MOVES,
    *BACK_MOVES,
    *LEFT_MOVES,
    *RIGHT_MOVES,
)
