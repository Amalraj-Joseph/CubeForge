from __future__ import annotations

from dataclasses import dataclass

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
from cube.internal.orientation_rules import (
    B as B_RULE,
    D as D_RULE,
    F as F_RULE,
    L as L_RULE,
    OrientationRule,
    R as R_RULE,
    U as U_RULE,
)
from cube.move.move import Move


@dataclass(frozen=True, slots=True)
class MoveTransformation:
    """
    Immutable transformation produced by a clockwise face turn.

    A MoveTransformation consists of

    - edge PositionCycle
    - corner PositionCycle
    - OrientationRule
    """

    edge_cycle: PositionCycle
    corner_cycle: PositionCycle
    orientation_rule: OrientationRule


U_TRANSFORMATION = MoveTransformation(
    edge_cycle=U_EDGE,
    corner_cycle=U_CORNER,
    orientation_rule=U_RULE,
)

D_TRANSFORMATION = MoveTransformation(
    edge_cycle=D_EDGE,
    corner_cycle=D_CORNER,
    orientation_rule=D_RULE,
)

F_TRANSFORMATION = MoveTransformation(
    edge_cycle=F_EDGE,
    corner_cycle=F_CORNER,
    orientation_rule=F_RULE,
)

B_TRANSFORMATION = MoveTransformation(
    edge_cycle=B_EDGE,
    corner_cycle=B_CORNER,
    orientation_rule=B_RULE,
)

L_TRANSFORMATION = MoveTransformation(
    edge_cycle=L_EDGE,
    corner_cycle=L_CORNER,
    orientation_rule=L_RULE,
)

R_TRANSFORMATION = MoveTransformation(
    edge_cycle=R_EDGE,
    corner_cycle=R_CORNER,
    orientation_rule=R_RULE,
)


MOVE_TRANSFORMATIONS: dict[Move, MoveTransformation] = {
    U: U_TRANSFORMATION,
    D: D_TRANSFORMATION,
    F: F_TRANSFORMATION,
    B: B_TRANSFORMATION,
    L: L_TRANSFORMATION,
    R: R_TRANSFORMATION,
}