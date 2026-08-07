from cube.internal.canonical_positions import (
    ALL_POSITIONS,
    B,
    CENTER_POSITIONS,
    CORNER_POSITIONS,
    D,
    EDGE_POSITIONS,
    F,
    L,
    R,
    U,
)
from cube.position.position_type import PositionType

# ==============================================================================
# Counts
# ==============================================================================

def test_position_counts():
    assert len(CENTER_POSITIONS) == 6
    assert len(EDGE_POSITIONS) == 12
    assert len(CORNER_POSITIONS) == 8
    assert len(ALL_POSITIONS) == 26


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_all_positions_are_unique():
    assert len(set(ALL_POSITIONS)) == 26


# ==============================================================================
# Collections
# ==============================================================================

def test_all_positions_collection():
    assert (
        *CENTER_POSITIONS,
        *EDGE_POSITIONS,
        *CORNER_POSITIONS,
    ) == ALL_POSITIONS


# ==============================================================================
# Position Types
# ==============================================================================

def test_center_positions():
    assert all(
        position.position_type is PositionType.CENTER
        for position in CENTER_POSITIONS
    )


def test_edge_positions():
    assert all(
        position.position_type is PositionType.EDGE
        for position in EDGE_POSITIONS
    )


def test_corner_positions():
    assert all(
        position.position_type is PositionType.CORNER
        for position in CORNER_POSITIONS
    )


# ==============================================================================
# Canonical Positions
# ==============================================================================

def test_canonical_centers():
    assert U.position_type is PositionType.CENTER
    assert D.position_type is PositionType.CENTER
    assert F.position_type is PositionType.CENTER
    assert B.position_type is PositionType.CENTER
    assert L.position_type is PositionType.CENTER
    assert R.position_type is PositionType.CENTER


# ==============================================================================
# Contract
# ==============================================================================

def test_canonical_position_contract():
    for position in ALL_POSITIONS:
        assert len(position.faces) == position.position_type.face_count
