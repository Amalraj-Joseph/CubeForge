from cube.internal.canonical_moves import (
    B,
    D,
    F,
    L,
    R,
    U,
)
from cube.internal.move_cycles import (
    B_CORNER,
    B_EDGE,
    D_CORNER,
    D_EDGE,
    F_CORNER,
    F_EDGE,
    L_CORNER,
    L_EDGE,
    PositionCycle,
    R_CORNER,
    R_EDGE,
    U_CORNER,
    U_EDGE,
)
from cube.internal.move_transformations import (
    B_TRANSFORMATION,
    D_TRANSFORMATION,
    F_TRANSFORMATION,
    L_TRANSFORMATION,
    MOVE_TRANSFORMATIONS,
    MoveTransformation,
    R_TRANSFORMATION,
    U_TRANSFORMATION,
)
from cube.internal.orientation_rules import (
    B as B_RULE,
)
from cube.internal.orientation_rules import (
    D as D_RULE,
)
from cube.internal.orientation_rules import (
    F as F_RULE,
)
from cube.internal.orientation_rules import (
    L as L_RULE,
)
from cube.internal.orientation_rules import (
    OrientationRule,
)
from cube.internal.orientation_rules import (
    R as R_RULE,
)
from cube.internal.orientation_rules import (
    U as U_RULE,
)

# ==============================================================================
# Counts
# ==============================================================================

def test_contains_six_move_transformations():
    assert len(MOVE_TRANSFORMATIONS) == 6


# ==============================================================================
# Construction
# ==============================================================================

def test_all_values_are_move_transformations():
    assert all(
        isinstance(
            transformation,
            MoveTransformation,
        )
        for transformation in MOVE_TRANSFORMATIONS.values()
    )


# ==============================================================================
# Lookup
# ==============================================================================

def test_lookup():
    assert MOVE_TRANSFORMATIONS[U] is U_TRANSFORMATION
    assert MOVE_TRANSFORMATIONS[D] is D_TRANSFORMATION
    assert MOVE_TRANSFORMATIONS[F] is F_TRANSFORMATION
    assert MOVE_TRANSFORMATIONS[B] is B_TRANSFORMATION
    assert MOVE_TRANSFORMATIONS[L] is L_TRANSFORMATION
    assert MOVE_TRANSFORMATIONS[R] is R_TRANSFORMATION


# ==============================================================================
# Edge Cycles
# ==============================================================================

def test_edge_cycles():
    assert U_TRANSFORMATION.edge_cycle is U_EDGE
    assert D_TRANSFORMATION.edge_cycle is D_EDGE
    assert F_TRANSFORMATION.edge_cycle is F_EDGE
    assert B_TRANSFORMATION.edge_cycle is B_EDGE
    assert L_TRANSFORMATION.edge_cycle is L_EDGE
    assert R_TRANSFORMATION.edge_cycle is R_EDGE


# ==============================================================================
# Corner Cycles
# ==============================================================================

def test_corner_cycles():
    assert U_TRANSFORMATION.corner_cycle is U_CORNER
    assert D_TRANSFORMATION.corner_cycle is D_CORNER
    assert F_TRANSFORMATION.corner_cycle is F_CORNER
    assert B_TRANSFORMATION.corner_cycle is B_CORNER
    assert L_TRANSFORMATION.corner_cycle is L_CORNER
    assert R_TRANSFORMATION.corner_cycle is R_CORNER


# ==============================================================================
# Orientation Rules
# ==============================================================================

def test_orientation_rules():
    assert U_TRANSFORMATION.orientation_rule is U_RULE
    assert D_TRANSFORMATION.orientation_rule is D_RULE
    assert F_TRANSFORMATION.orientation_rule is F_RULE
    assert B_TRANSFORMATION.orientation_rule is B_RULE
    assert L_TRANSFORMATION.orientation_rule is L_RULE
    assert R_TRANSFORMATION.orientation_rule is R_RULE


# ==============================================================================
# Contract
# ==============================================================================

def test_move_transformation_contract():
    for transformation in MOVE_TRANSFORMATIONS.values():
        assert isinstance(
            transformation.edge_cycle,
            PositionCycle,
        )

        assert isinstance(
            transformation.corner_cycle,
            PositionCycle,
        )

        assert isinstance(
            transformation.orientation_rule,
            OrientationRule,
        )
