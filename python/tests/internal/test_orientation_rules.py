from cube.face.logical_face import LogicalFace
from cube.internal.orientation_rules import (
    B,
    D,
    F,
    L,
    ORIENTATION_RULES,
    OrientationRule,
    R,
    U,
)

# ==============================================================================
# Counts
# ==============================================================================

def test_contains_six_rules():
    assert len(ORIENTATION_RULES) == 6


# ==============================================================================
# Construction
# ==============================================================================

def test_all_are_orientation_rules():
    for rule in ORIENTATION_RULES.values():
        assert isinstance(
            rule,
            OrientationRule,
        )


# ==============================================================================
# Edge Rules
# ==============================================================================

def test_edge_flip_faces():
    assert F.edge_flip
    assert B.edge_flip

    assert not U.edge_flip
    assert not D.edge_flip
    assert not L.edge_flip
    assert not R.edge_flip


# ==============================================================================
# Corner Rules
# ==============================================================================

def test_corner_twist_lengths():
    for rule in ORIENTATION_RULES.values():
        assert len(rule.corner_twists) == 4


def test_corner_twists_are_mod3():
    for rule in ORIENTATION_RULES.values():
        assert set(rule.corner_twists) <= {
            0,
            1,
            2,
        }


# ==============================================================================
# Lookup
# ==============================================================================

def test_lookup():
    assert ORIENTATION_RULES[
        LogicalFace.UP
    ] is U

    assert ORIENTATION_RULES[
        LogicalFace.RIGHT
    ] is R


# ==============================================================================
# Contract
# ==============================================================================

def test_orientation_rule_contract():
    for rule in ORIENTATION_RULES.values():
        assert isinstance(
            rule.edge_flip,
            bool,
        )

        assert isinstance(
            rule.corner_twists,
            tuple,
        )

        assert len(rule.corner_twists) == 4

# ==============================================================================
# Behaviour
# ==============================================================================

def test_edge_rotation():
    assert U.edge_rotation() == 0
    assert D.edge_rotation() == 0
    assert L.edge_rotation() == 0
    assert R.edge_rotation() == 0

    assert F.edge_rotation() == 1
    assert B.edge_rotation() == 1


def test_corner_rotation():
    assert F.corner_rotation(0) == 1
    assert F.corner_rotation(1) == 2
    assert F.corner_rotation(2) == 1
    assert F.corner_rotation(3) == 2

    assert B.corner_rotation(0) == 2
    assert B.corner_rotation(1) == 1
    assert B.corner_rotation(2) == 2
    assert B.corner_rotation(3) == 1
