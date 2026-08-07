from __future__ import annotations

from dataclasses import dataclass

from cube.face.logical_face import LogicalFace


@dataclass(frozen=True, slots=True)
class OrientationRule:
    """
    Orientation changes produced by a clockwise face turn.

    edge_flip

        True  -> participating edges flip

        False -> participating edges do not flip

    corner_twists

        Orientation deltas for the four participating
        corners, in the same order as the corresponding
        PositionCycle.
    """

    edge_flip: bool

    corner_twists: tuple[
        int,
        int,
        int,
        int,
    ]

    def edge_rotation(self) -> int:
        """
        Returns the edge orientation delta.
        """
        return 1 if self.edge_flip else 0

    def corner_rotation(
        self,
        index: int,
    ) -> int:
        """
        Returns the corner orientation delta for the
        given PositionCycle index.
        """
        return self.corner_twists[index]


# ==============================================================================
# U
# ==============================================================================

U = OrientationRule(
    edge_flip=False,
    corner_twists=(0, 0, 0, 0),
)

# ==============================================================================
# D
# ==============================================================================

D = OrientationRule(
    edge_flip=False,
    corner_twists=(0, 0, 0, 0),
)

# ==============================================================================
# F
# ==============================================================================

F = OrientationRule(
    edge_flip=True,
    corner_twists=(1, 2, 1, 2),
)

# ==============================================================================
# B
# ==============================================================================

B = OrientationRule(
    edge_flip=True,
    corner_twists=(2, 1, 2, 1),
)

# ==============================================================================
# L
# ==============================================================================

L = OrientationRule(
    edge_flip=False,
    corner_twists=(1, 2, 1, 2),
)

# ==============================================================================
# R
# ==============================================================================

R = OrientationRule(
    edge_flip=False,
    corner_twists=(2, 1, 2, 1),
)


ORIENTATION_RULES = {
    LogicalFace.UP: U,
    LogicalFace.DOWN: D,
    LogicalFace.FRONT: F,
    LogicalFace.BACK: B,
    LogicalFace.LEFT: L,
    LogicalFace.RIGHT: R,
}
