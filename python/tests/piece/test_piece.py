import pytest

from cube.color.color import Color
from cube.piece.piece import Piece
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_type import PieceType


# ==============================================================================
# Construction
# ==============================================================================

def test_create_center_piece():
    signature = PieceSignature(
        PieceType.CENTER,
        Color.WHITE,
    )

    piece = Piece(signature)

    assert piece.signature is signature


def test_create_edge_piece():
    signature = PieceSignature(
        PieceType.EDGE,
        Color.WHITE,
        Color.GREEN,
    )

    piece = Piece(signature)

    assert piece.signature is signature


def test_create_corner_piece():
    signature = PieceSignature(
        PieceType.CORNER,
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    )

    piece = Piece(signature)

    assert piece.signature is signature


# ==============================================================================
# Delegation
# ==============================================================================

def test_piece_type():
    piece = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.GREEN,
        )
    )

    assert piece.piece_type is PieceType.EDGE


def test_colors():
    piece = Piece(
        PieceSignature(
            PieceType.CORNER,
            Color.WHITE,
            Color.GREEN,
            Color.RED,
        )
    )

    assert piece.colors == frozenset({
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    })


def test_contains():
    piece = Piece(
        PieceSignature(
            PieceType.CORNER,
            Color.WHITE,
            Color.GREEN,
            Color.RED,
        )
    )

    assert piece.contains(Color.WHITE)
    assert piece.contains(Color.GREEN)
    assert piece.contains(Color.RED)

    assert not piece.contains(Color.BLUE)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equal_pieces():
    first = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.GREEN,
        )
    )

    second = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.GREEN,
            Color.WHITE,
        )
    )

    assert first == second
    assert hash(first) == hash(second)


def test_different_pieces():
    first = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.GREEN,
        )
    )

    second = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.RED,
        )
    )

    assert first != second


# ==============================================================================
# Representation
# ==============================================================================

def test_description():
    piece = Piece(
        PieceSignature(
            PieceType.CENTER,
            Color.WHITE,
        )
    )

    assert piece.describe() == "Center(White)"


def test_string_representation():
    piece = Piece(
        PieceSignature(
            PieceType.CENTER,
            Color.WHITE,
        )
    )

    assert str(piece) == piece.describe()


# ==============================================================================
# Immutability
# ==============================================================================

def test_piece_is_immutable():
    piece = Piece(
        PieceSignature(
            PieceType.CENTER,
            Color.WHITE,
        )
    )

    with pytest.raises(AttributeError):
        piece.signature = None


# ==============================================================================
# Contract
# ==============================================================================

def test_piece_contract():
    piece = Piece(
        PieceSignature(
            PieceType.CORNER,
            Color.WHITE,
            Color.GREEN,
            Color.RED,
        )
    )

    assert piece.piece_type is PieceType.CORNER
    assert len(piece.colors) == 3
    assert piece.contains(Color.WHITE)
    assert isinstance(piece.describe(), str)