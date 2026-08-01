from cube.color.color import Color
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
    )
)

YELLOW_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.YELLOW,
    )
)

GREEN_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.GREEN,
    )
)

BLUE_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.BLUE,
    )
)

RED_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.RED,
    )
)

ORANGE_CENTER = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.ORANGE,
    )
)


# ==============================================================================
# Edges
# ==============================================================================

WHITE_GREEN_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )
)

WHITE_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.RED,
    )
)

WHITE_BLUE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.BLUE,
    )
)

WHITE_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.ORANGE,
    )
)

GREEN_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.GREEN,
        Color.RED,
    )
)

GREEN_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.GREEN,
        Color.ORANGE,
    )
)

BLUE_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.BLUE,
        Color.RED,
    )
)

BLUE_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.BLUE,
        Color.ORANGE,
    )
)

YELLOW_GREEN_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.GREEN,
    )
)

YELLOW_RED_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.RED,
    )
)

YELLOW_BLUE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.BLUE,
    )
)

YELLOW_ORANGE_EDGE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.YELLOW,
        Color.ORANGE,
    )
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
    )
)

WHITE_RED_BLUE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.RED,
        Color.BLUE,
    )
)

WHITE_BLUE_ORANGE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.BLUE,
        Color.ORANGE,
    )
)

WHITE_ORANGE_GREEN_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.ORANGE,
        Color.GREEN,
    )
)

YELLOW_GREEN_ORANGE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.GREEN,
        Color.ORANGE,
    )
)

YELLOW_RED_GREEN_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.RED,
        Color.GREEN,
    )
)

YELLOW_BLUE_RED_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.BLUE,
        Color.RED,
    )
)

YELLOW_ORANGE_BLUE_CORNER = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.YELLOW,
        Color.ORANGE,
        Color.BLUE,
    )
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