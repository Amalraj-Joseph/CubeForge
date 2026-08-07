from cube.color.color import Color
from cube.internal.canonical_piece_layouts import (
    BLUE_CENTER_LAYOUT,
    BLUE_ORANGE_EDGE_LAYOUT,
    BLUE_RED_EDGE_LAYOUT,
    GREEN_CENTER_LAYOUT,
    GREEN_ORANGE_EDGE_LAYOUT,
    GREEN_RED_EDGE_LAYOUT,
    ORANGE_CENTER_LAYOUT,
    RED_CENTER_LAYOUT,
    WHITE_BLUE_EDGE_LAYOUT,
    WHITE_BLUE_ORANGE_CORNER_LAYOUT,
    WHITE_CENTER_LAYOUT,
    WHITE_GREEN_EDGE_LAYOUT,
    WHITE_GREEN_RED_CORNER_LAYOUT,
    WHITE_ORANGE_EDGE_LAYOUT,
    WHITE_ORANGE_GREEN_CORNER_LAYOUT,
    WHITE_RED_BLUE_CORNER_LAYOUT,
    WHITE_RED_EDGE_LAYOUT,
    YELLOW_BLUE_EDGE_LAYOUT,
    YELLOW_BLUE_RED_CORNER_LAYOUT,
    YELLOW_CENTER_LAYOUT,
    YELLOW_GREEN_EDGE_LAYOUT,
    YELLOW_GREEN_ORANGE_CORNER_LAYOUT,
    YELLOW_ORANGE_BLUE_CORNER_LAYOUT,
    YELLOW_ORANGE_EDGE_LAYOUT,
    YELLOW_RED_EDGE_LAYOUT,
    YELLOW_RED_GREEN_CORNER_LAYOUT,
)
from cube.piece.piece import Piece
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_type import PieceType

# ==============================================================================
# Centers
# ==============================================================================

WHITE_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    ),
    WHITE_CENTER_LAYOUT,
)

YELLOW_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.YELLOW,
    ),
    YELLOW_CENTER_LAYOUT,
)

GREEN_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.GREEN,
    ),
    GREEN_CENTER_LAYOUT,
)

BLUE_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.BLUE,
    ),
    BLUE_CENTER_LAYOUT,
)

RED_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.RED,
    ),
    RED_CENTER_LAYOUT,
)

ORANGE_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.ORANGE,
    ),
    ORANGE_CENTER_LAYOUT,
)


# ==============================================================================
# Edges
# ==============================================================================

WHITE_GREEN_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    ),
    WHITE_GREEN_EDGE_LAYOUT,
)

WHITE_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.RED,
    ),
    WHITE_RED_EDGE_LAYOUT,
)

WHITE_BLUE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.BLUE,
    ),
    WHITE_BLUE_EDGE_LAYOUT,
)

WHITE_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.ORANGE,
    ),
    WHITE_ORANGE_EDGE_LAYOUT,
)

GREEN_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.GREEN,
        Color.RED,
    ),
    GREEN_RED_EDGE_LAYOUT,
)

GREEN_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.GREEN,
        Color.ORANGE,
    ),
    GREEN_ORANGE_EDGE_LAYOUT,
)

BLUE_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.BLUE,
        Color.RED,
    ),
    BLUE_RED_EDGE_LAYOUT,
)

BLUE_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.BLUE,
        Color.ORANGE,
    ),
    BLUE_ORANGE_EDGE_LAYOUT,
)

YELLOW_GREEN_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.GREEN,
    ),
    YELLOW_GREEN_EDGE_LAYOUT,
)

YELLOW_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.RED,
    ),
    YELLOW_RED_EDGE_LAYOUT,
)

YELLOW_BLUE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.BLUE,
    ),
    YELLOW_BLUE_EDGE_LAYOUT,
)

YELLOW_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.ORANGE,
    ),
    YELLOW_ORANGE_EDGE_LAYOUT,
)


# ==============================================================================
# Corners
# ==============================================================================

WHITE_GREEN_RED_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    ),
    WHITE_GREEN_RED_CORNER_LAYOUT,
)

WHITE_RED_BLUE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.RED,
        Color.BLUE,
    ),
    WHITE_RED_BLUE_CORNER_LAYOUT,
)

WHITE_BLUE_ORANGE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.BLUE,
        Color.ORANGE,
    ),
    WHITE_BLUE_ORANGE_CORNER_LAYOUT,
)

WHITE_ORANGE_GREEN_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.ORANGE,
        Color.GREEN,
    ),
    WHITE_ORANGE_GREEN_CORNER_LAYOUT,
)

YELLOW_GREEN_ORANGE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.GREEN,
        Color.ORANGE,
    ),
    YELLOW_GREEN_ORANGE_CORNER_LAYOUT,
)

YELLOW_RED_GREEN_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.RED,
        Color.GREEN,
    ),
    YELLOW_RED_GREEN_CORNER_LAYOUT,
)

YELLOW_BLUE_RED_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.BLUE,
        Color.RED,
    ),
    YELLOW_BLUE_RED_CORNER_LAYOUT,
)

YELLOW_ORANGE_BLUE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.ORANGE,
        Color.BLUE,
    ),
    YELLOW_ORANGE_BLUE_CORNER_LAYOUT,
)


# ==============================================================================
# Collections
# ==============================================================================

CENTER_PIECES = (
    WHITE_CENTER,
    YELLOW_CENTER,
    GREEN_CENTER,
    BLUE_CENTER,
    RED_CENTER,
    ORANGE_CENTER,
)

EDGE_PIECES = (
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
)

CORNER_PIECES = (
    WHITE_GREEN_RED_CORNER,
    WHITE_RED_BLUE_CORNER,
    WHITE_BLUE_ORANGE_CORNER,
    WHITE_ORANGE_GREEN_CORNER,
    YELLOW_GREEN_ORANGE_CORNER,
    YELLOW_RED_GREEN_CORNER,
    YELLOW_BLUE_RED_CORNER,
    YELLOW_ORANGE_BLUE_CORNER,
)

ALL_PIECES = (
    *CENTER_PIECES,
    *EDGE_PIECES,
    *CORNER_PIECES,
)
