import pytest

from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.piece.piece import Piece
from cube.piece.piece_orientation import PieceOrientation
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType
from cube.position.position import Position
from cube.position.position_type import PositionType


# ==============================================================================
# Fixtures
# ==============================================================================

CENTER_PIECE = Piece(
    PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    )
)

EDGE_PIECE = Piece(
    PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )
)

CORNER_PIECE = Piece(
    PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )
)

CENTER_POSITION = Position(
    PositionType.CENTER,
    LogicalFace.UP,
)

EDGE_POSITION = Position(
    PositionType.EDGE,
    LogicalFace.UP,
    LogicalFace.FRONT,
)

CORNER_POSITION = Position(
    PositionType.CORNER,
    LogicalFace.UP,
    LogicalFace.FRONT,
    LogicalFace.RIGHT,
)


# ==============================================================================
# Construction
# ==============================================================================

def test_create_center_state():
    state = PieceState(
        CENTER_PIECE,
        CENTER_POSITION,
        PieceOrientation(
            PieceType.CENTER,
            0,
        ),
    )

    assert state.piece is CENTER_PIECE
    assert state.position is CENTER_POSITION
    assert state.orientation == PieceOrientation(
        PieceType.CENTER,
        0,
    )


def test_create_edge_state():
    state = PieceState(
        EDGE_PIECE,
        EDGE_POSITION,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
    )

    assert state.piece is EDGE_PIECE
    assert state.position is EDGE_POSITION
    assert state.orientation.value == 1


def test_create_corner_state():
    state = PieceState(
        CORNER_PIECE,
        CORNER_POSITION,
        PieceOrientation(
            PieceType.CORNER,
            2,
        ),
    )

    assert state.piece is CORNER_PIECE
    assert state.position is CORNER_POSITION
    assert state.orientation.value == 2


# ==============================================================================
# Validation
# ==============================================================================

def test_piece_and_position_type_must_match():
    with pytest.raises(ValueError):
        PieceState(
            CORNER_PIECE,
            EDGE_POSITION,
            PieceOrientation(
                PieceType.CORNER,
                0,
            ),
        )


def test_piece_and_orientation_type_must_match():
    with pytest.raises(ValueError):
        PieceState(
            EDGE_PIECE,
            EDGE_POSITION,
            PieceOrientation(
                PieceType.CORNER,
                0,
            ),
        )


# ==============================================================================
# Properties
# ==============================================================================

def test_piece_type():
    state = PieceState(
        EDGE_PIECE,
        EDGE_POSITION,
        PieceOrientation(
            PieceType.EDGE,
            0,
        ),
    )

    assert state.piece_type is PieceType.EDGE


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equality():
    first = PieceState(
        EDGE_PIECE,
        EDGE_POSITION,
        PieceOrientation(
            PieceType.EDGE,
            0,
        ),
    )

    second = PieceState(
        EDGE_PIECE,
        EDGE_POSITION,
        PieceOrientation(
            PieceType.EDGE,
            0,
        ),
    )

    assert first == second
    assert hash(first) == hash(second)


def test_different_orientation_not_equal():
    first = PieceState(
        EDGE_PIECE,
        EDGE_POSITION,
        PieceOrientation(
            PieceType.EDGE,
            0,
        ),
    )

    second = PieceState(
        EDGE_PIECE,
        EDGE_POSITION,
        PieceOrientation(
            PieceType.EDGE,
            1,
        ),
    )

    assert first != second


# ==============================================================================
# Immutability
# ==============================================================================

def test_piece_state_is_immutable():
    state = PieceState(
        CENTER_PIECE,
        CENTER_POSITION,
        PieceOrientation(
            PieceType.CENTER,
            0,
        ),
    )

    with pytest.raises(AttributeError):
        state.position = EDGE_POSITION


# ==============================================================================
# Contract
# ==============================================================================

def test_piece_state_contract():
    state = PieceState(
        CORNER_PIECE,
        CORNER_POSITION,
        PieceOrientation(
            PieceType.CORNER,
            1,
        ),
    )

    assert (
        state.piece.signature.piece_type.color_count
        ==
        state.position.position_type.face_count
    )

    assert (
        state.piece.signature.piece_type.color_count
        ==
        state.orientation.piece_type.color_count
    )