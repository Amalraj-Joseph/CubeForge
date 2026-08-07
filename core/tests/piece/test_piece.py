import pytest

from cube.color.color import Color
from cube.face.logical_face import LogicalFace
from cube.internal.canonical_pieces import (
    WHITE_CENTER,
    WHITE_GREEN_EDGE,
    WHITE_GREEN_RED_CORNER,
)
from cube.piece.piece import Piece
from cube.piece.piece_layout import PieceLayout
from cube.piece.piece_signature import PieceSignature
from cube.piece.piece_type import PieceType

# ==============================================================================
# Validation
# ==============================================================================

def test_piece_type_must_match():
    with pytest.raises(ValueError):
        Piece(
            PieceSignature(
                PieceType.CENTER,
                Color.WHITE,
            ),
            PieceLayout(
                PieceType.EDGE,
                (
                    LogicalFace.UP,
                    Color.WHITE,
                ),
                (
                    LogicalFace.FRONT,
                    Color.GREEN,
                ),
            ),
        )


def test_colors_must_match():
    with pytest.raises(ValueError):
        Piece(
            PieceSignature(
                PieceType.EDGE,
                Color.WHITE,
                Color.RED,
            ),
            PieceLayout(
                PieceType.EDGE,
                (
                    LogicalFace.UP,
                    Color.WHITE,
                ),
                (
                    LogicalFace.FRONT,
                    Color.GREEN,
                ),
            ),
        )


# ==============================================================================
# Delegation
# ==============================================================================

def test_piece_type():
    assert WHITE_GREEN_EDGE.piece_type is PieceType.EDGE


def test_colors():
    assert WHITE_GREEN_RED_CORNER.colors == frozenset({
        Color.WHITE,
        Color.GREEN,
        Color.RED,
    })


def test_contains():
    assert WHITE_GREEN_RED_CORNER.contains(Color.WHITE)
    assert WHITE_GREEN_RED_CORNER.contains(Color.GREEN)
    assert WHITE_GREEN_RED_CORNER.contains(Color.RED)

    assert not WHITE_GREEN_RED_CORNER.contains(Color.BLUE)


# ==============================================================================
# Equality & Hashing
# ==============================================================================

def test_equal_pieces():
    first = WHITE_GREEN_EDGE

    second = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.GREEN,
            Color.WHITE,
        ),
        PieceLayout(
            PieceType.EDGE,
            (
                LogicalFace.UP,
                Color.WHITE,
            ),
            (
                LogicalFace.FRONT,
                Color.GREEN,
            ),
        ),
    )

    assert first == second
    assert hash(first) == hash(second)


def test_pieces_with_equal_signatures_are_equal_despite_layout_difference():
    first = WHITE_GREEN_EDGE

    second = Piece(
        PieceSignature(
            PieceType.EDGE,
            Color.WHITE,
            Color.GREEN,
        ),
        PieceLayout(
            PieceType.EDGE,
            (
                LogicalFace.FRONT,
                Color.GREEN,
            ),
            (
                LogicalFace.UP,
                Color.WHITE,
            ),
        ),
    )

    assert first == second


def test_different_pieces():
    assert WHITE_CENTER != WHITE_GREEN_EDGE


def test_piece_is_not_equal_to_a_non_piece():
    assert WHITE_CENTER != "not a piece"
    assert WHITE_CENTER != 42


# ==============================================================================
# Representation
# ==============================================================================

def test_description():
    assert (
        WHITE_CENTER.describe()
        == "Center(White)"
    )


def test_string_representation():
    assert (
        str(WHITE_CENTER)
        == WHITE_CENTER.describe()
    )


# ==============================================================================
# Immutability
# ==============================================================================

def test_piece_is_immutable():
    with pytest.raises(AttributeError):
        WHITE_CENTER.signature = None

    with pytest.raises(AttributeError):
        WHITE_CENTER.layout = None


# ==============================================================================
# Contract
# ==============================================================================

def test_piece_contract():
    assert (
        WHITE_GREEN_RED_CORNER.piece_type
        is PieceType.CORNER
    )

    assert len(
        WHITE_GREEN_RED_CORNER.colors
    ) == 3

    assert (
        WHITE_GREEN_RED_CORNER.layout.piece_type
        is PieceType.CORNER
    )

    assert (
        WHITE_GREEN_RED_CORNER.layout.colors
        == WHITE_GREEN_RED_CORNER.colors
    )

    assert isinstance(
        WHITE_GREEN_RED_CORNER.describe(),
        str,
    )
