from cube.internal.canonical_pieces import (
    ALL_PIECES,
    CENTER_PIECES,
    CORNER_PIECES,
    EDGE_PIECES,
)
from cube.piece.piece_type import PieceType


# ==============================================================================
# Counts
# ==============================================================================

def test_piece_counts():
    assert len(CENTER_PIECES) == 6
    assert len(EDGE_PIECES) == 12
    assert len(CORNER_PIECES) == 8
    assert len(ALL_PIECES) == 26


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_all_pieces_are_unique():
    assert len(set(ALL_PIECES)) == 26


def test_all_piece_signatures_are_unique():
    signatures = {
        piece.signature
        for piece in ALL_PIECES
    }

    assert len(signatures) == 26


# ==============================================================================
# Collections
# ==============================================================================

def test_all_pieces_collection():
    assert ALL_PIECES == (
        *CENTER_PIECES,
        *EDGE_PIECES,
        *CORNER_PIECES,
    )


# ==============================================================================
# Piece Types
# ==============================================================================

def test_center_pieces():
    assert all(
        piece.signature.piece_type is PieceType.CENTER
        for piece in CENTER_PIECES
    )


def test_edge_pieces():
    assert all(
        piece.signature.piece_type is PieceType.EDGE
        for piece in EDGE_PIECES
    )


def test_corner_pieces():
    assert all(
        piece.signature.piece_type is PieceType.CORNER
        for piece in CORNER_PIECES
    )


# ==============================================================================
# Contract
# ==============================================================================

def test_canonical_piece_contract():
    for piece in ALL_PIECES:
        signature = piece.signature

        assert len(signature.colors) == signature.piece_type.color_count