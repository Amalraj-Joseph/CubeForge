import pytest

from cube.internal.move_cycles import (
    B_CORNER,
    B_EDGE,
    D_CORNER,
    D_EDGE,
    F_CORNER,
    F_EDGE,
    L_CORNER,
    L_EDGE,
    MOVE_CYCLES,
    PositionCycle,
    R_CORNER,
    R_EDGE,
    U_CORNER,
    U_EDGE,
)
from cube.position.position_type import PositionType

# ==============================================================================
# Counts
# ==============================================================================

def test_contains_twelve_cycles():
    assert len(MOVE_CYCLES) == 12


def test_each_cycle_contains_four_positions():
    for cycle in MOVE_CYCLES:
        assert len(cycle.positions) == 4


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_each_cycle_contains_unique_positions():
    for cycle in MOVE_CYCLES:
        assert len(set(cycle.positions)) == 4


# ==============================================================================
# Validation
# ==============================================================================

def test_rejects_a_cycle_with_a_duplicate_position():
    with pytest.raises(ValueError, match="four unique Positions"):
        PositionCycle((U_EDGE.positions[0],) * 4)


# ==============================================================================
# Types
# ==============================================================================

def test_edge_cycles_contain_only_edges():
    for cycle in (
        U_EDGE,
        D_EDGE,
        F_EDGE,
        B_EDGE,
        L_EDGE,
        R_EDGE,
    ):
        assert all(
            position.position_type
            is PositionType.EDGE
            for position in cycle.positions
        )


def test_corner_cycles_contain_only_corners():
    for cycle in (
        U_CORNER,
        D_CORNER,
        F_CORNER,
        B_CORNER,
        L_CORNER,
        R_CORNER,
    ):
        assert all(
            position.position_type
            is PositionType.CORNER
            for position in cycle.positions
        )


# ==============================================================================
# Construction
# ==============================================================================

def test_all_cycles_are_position_cycles():
    for cycle in MOVE_CYCLES:
        assert isinstance(
            cycle,
            PositionCycle,
        )


# ==============================================================================
# Contract
# ==============================================================================

def test_position_cycle_contract():
    for cycle in MOVE_CYCLES:
        assert isinstance(
            cycle.positions,
            tuple,
        )

        assert len(cycle.positions) == 4

        assert len(set(cycle.positions)) == 4
