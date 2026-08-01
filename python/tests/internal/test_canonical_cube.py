from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.internal.canonical_pieces import (
    ALL_PIECES,
    CENTER_PIECES,
    CORNER_PIECES,
    EDGE_PIECES,
)
from cube.internal.canonical_positions import (
    ALL_POSITIONS,
)
from cube.piece.piece_type import PieceType
from cube.position.position_type import PositionType


# ==============================================================================
# Counts
# ==============================================================================

def test_cube_contains_26_piece_mappings():
    assert len(CANONICAL_CUBE) == 26


# ==============================================================================
# Coverage
# ==============================================================================

def test_every_piece_is_present():
    assert set(CANONICAL_CUBE.keys()) == set(ALL_PIECES)


def test_every_position_is_present():
    assert set(CANONICAL_CUBE.values()) == set(ALL_POSITIONS)


# ==============================================================================
# Piece Type Mapping
# ==============================================================================

def test_centers_map_to_center_positions():
    for piece in CENTER_PIECES:
        position = CANONICAL_CUBE[piece]

        assert piece.signature.piece_type is PieceType.CENTER
        assert position.position_type is PositionType.CENTER


def test_edges_map_to_edge_positions():
    for piece in EDGE_PIECES:
        position = CANONICAL_CUBE[piece]

        assert piece.signature.piece_type is PieceType.EDGE
        assert position.position_type is PositionType.EDGE


def test_corners_map_to_corner_positions():
    for piece in CORNER_PIECES:
        position = CANONICAL_CUBE[piece]

        assert piece.signature.piece_type is PieceType.CORNER
        assert position.position_type is PositionType.CORNER


# ==============================================================================
# Contract
# ==============================================================================

def test_canonical_cube_contract():
    for piece, position in CANONICAL_CUBE.items():
        assert (
            piece.signature.piece_type.color_count
            ==
            position.position_type.face_count
        )