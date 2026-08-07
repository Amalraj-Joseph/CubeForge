from __future__ import annotations

from dataclasses import dataclass

from cube.face.logical_face import LogicalFace
from cube.move.rotation import Rotation


@dataclass(frozen=True, slots=True)
class Move:
    """
    Represents a single face turn.

    A Move consists of

    - LogicalFace
    - Rotation
    """

    face: LogicalFace
    rotation: Rotation

    @property
    def notation(self) -> str:
        """
        Returns the Singmaster notation.
        """
        return (
            self.face.symbol +
            self.rotation.notation
        )

    @property
    def inverse(self) -> Move:
        """
        Returns the inverse Move.
        """
        return Move(
            self.face,
            self.rotation.inverse,
        )

    @property
    def is_half_turn(self) -> bool:
        """
        Returns True if this Move is a half turn.
        """
        return (
            self.rotation
            is Rotation.HALF_TURN
        )
