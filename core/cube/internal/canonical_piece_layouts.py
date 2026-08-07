from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_type import PieceType

# ==============================================================================
# Centers
# ==============================================================================

WHITE_CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
)

YELLOW_CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
)

GREEN_CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
)

BLUE_CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
)

ORANGE_CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)

RED_CENTER_LAYOUT = PieceLayout(
    PieceType.CENTER,
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)


# ==============================================================================
# Edges
# ==============================================================================

WHITE_GREEN_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
)

WHITE_RED_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)

WHITE_BLUE_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
)

WHITE_ORANGE_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)

GREEN_RED_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)

GREEN_ORANGE_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)

BLUE_RED_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)

BLUE_ORANGE_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)

YELLOW_GREEN_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
)

YELLOW_RED_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)

YELLOW_BLUE_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
)

YELLOW_ORANGE_EDGE_LAYOUT = PieceLayout(
    PieceType.EDGE,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)


# ==============================================================================
# Corners
# ==============================================================================

WHITE_GREEN_RED_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)

WHITE_RED_BLUE_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
)

WHITE_BLUE_ORANGE_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)

WHITE_ORANGE_GREEN_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.UP,
        Color.WHITE,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
)

YELLOW_GREEN_ORANGE_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
)

YELLOW_RED_GREEN_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
    (
        LogicalFace.FRONT,
        Color.GREEN,
    ),
)

YELLOW_BLUE_RED_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
    (
        LogicalFace.RIGHT,
        Color.RED,
    ),
)

YELLOW_ORANGE_BLUE_CORNER_LAYOUT = PieceLayout(
    PieceType.CORNER,
    (
        LogicalFace.DOWN,
        Color.YELLOW,
    ),
    (
        LogicalFace.LEFT,
        Color.ORANGE,
    ),
    (
        LogicalFace.BACK,
        Color.BLUE,
    ),
)


# ==============================================================================
# Collections
# ==============================================================================

CENTER_LAYOUTS = (
    WHITE_CENTER_LAYOUT,
    YELLOW_CENTER_LAYOUT,
    GREEN_CENTER_LAYOUT,
    BLUE_CENTER_LAYOUT,
    ORANGE_CENTER_LAYOUT,
    RED_CENTER_LAYOUT,
)

EDGE_LAYOUTS = (
    WHITE_GREEN_EDGE_LAYOUT,
    WHITE_RED_EDGE_LAYOUT,
    WHITE_BLUE_EDGE_LAYOUT,
    WHITE_ORANGE_EDGE_LAYOUT,
    GREEN_RED_EDGE_LAYOUT,
    GREEN_ORANGE_EDGE_LAYOUT,
    BLUE_RED_EDGE_LAYOUT,
    BLUE_ORANGE_EDGE_LAYOUT,
    YELLOW_GREEN_EDGE_LAYOUT,
    YELLOW_RED_EDGE_LAYOUT,
    YELLOW_BLUE_EDGE_LAYOUT,
    YELLOW_ORANGE_EDGE_LAYOUT,
)

CORNER_LAYOUTS = (
    WHITE_GREEN_RED_CORNER_LAYOUT,
    WHITE_RED_BLUE_CORNER_LAYOUT,
    WHITE_BLUE_ORANGE_CORNER_LAYOUT,
    WHITE_ORANGE_GREEN_CORNER_LAYOUT,
    YELLOW_GREEN_ORANGE_CORNER_LAYOUT,
    YELLOW_RED_GREEN_CORNER_LAYOUT,
    YELLOW_BLUE_RED_CORNER_LAYOUT,
    YELLOW_ORANGE_BLUE_CORNER_LAYOUT,
)

ALL_LAYOUTS = (
    *CENTER_LAYOUTS,
    *EDGE_LAYOUTS,
    *CORNER_LAYOUTS,
)
