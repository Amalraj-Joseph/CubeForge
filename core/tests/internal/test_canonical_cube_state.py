from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)
from cube.orientation.cube_orientation import CANONICAL_ORIENTATION

# ==============================================================================
# Cube Orientation
# ==============================================================================

def test_uses_canonical_orientation():
    assert CANONICAL_CUBE_STATE.orientation == CANONICAL_ORIENTATION


# ==============================================================================
# Size
# ==============================================================================

def test_contains_26_piece_states():
    assert len(CANONICAL_CUBE_STATE) == 26


# ==============================================================================
# Canonical Mapping
# ==============================================================================

def test_piece_positions_are_canonical():
    for piece, position in CANONICAL_CUBE.items():
        assert (
            CANONICAL_CUBE_STATE[piece].position
            is position
        )


# ==============================================================================
# Orientation
# ==============================================================================

def test_all_piece_orientations_are_zero():
    for piece_state in CANONICAL_CUBE_STATE:
        assert piece_state.orientation.value == 0


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_all_pieces_are_unique():
    assert len({
        state.piece
        for state in CANONICAL_CUBE_STATE
    }) == 26


def test_all_positions_are_unique():
    assert len({
        state.position
        for state in CANONICAL_CUBE_STATE
    }) == 26


# ==============================================================================
# Lookup
# ==============================================================================

def test_piece_lookup():
    for piece, position in CANONICAL_CUBE.items():
        assert (
            CANONICAL_CUBE_STATE[piece].position
            is position
        )

        assert (
            CANONICAL_CUBE_STATE.piece_at(position).piece
            is piece
        )


# ==============================================================================
# Contract
# ==============================================================================

def test_canonical_cube_state_contract():
    assert len(CANONICAL_CUBE_STATE) == 26

    assert len(tuple(CANONICAL_CUBE_STATE)) == 26

    for piece_state in CANONICAL_CUBE_STATE:
        assert piece_state.orientation.value == 0
