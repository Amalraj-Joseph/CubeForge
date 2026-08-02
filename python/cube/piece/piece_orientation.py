from __future__ import annotations

from dataclasses import dataclass

from cube.piece.piece_type import PieceType


@dataclass(frozen=True, slots=True)
class PieceOrientation:
    """
    Represents the orientation of a physical piece.

    Orientation is encoded as an integer.

    Center
        0

    Edge
        0, 1

    Corner
        0, 1, 2
    """

    piece_type: PieceType
    value: int

    def __post_init__(self) -> None:
        maximum = self.piece_type.color_count

        if not 0 <= self.value < maximum:
            raise ValueError(
                f"{self.piece_type.display_name} orientation "
                f"must be in the range "
                f"[0, {maximum - 1}], "
                f"got {self.value}."
            )

    @property
    def modulus(self) -> int:
        """
        Returns the orientation modulus.
        """
        return self.piece_type.color_count

    def rotate(
        self,
        amount: int,
    ) -> "PieceOrientation":
        """
        Returns the rotated orientation.
        """
        return PieceOrientation(
            self.piece_type,
            (self.value + amount) % self.modulus,
        )

    def describe(self) -> str:
        """
        Returns a human-readable description.
        """
        return (
            f"{self.piece_type.display_name}"
            f"Orientation({self.value})"
        )

    def __str__(self) -> str:
        return self.describe()