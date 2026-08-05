from __future__ import annotations

from dataclasses import dataclass

from cube.algorithm.algorithm import Algorithm
from cube.cube_state import CubeState
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.move.move import Move
from cube.transformation.cube_transformation import CubeTransformation
from cube.validation.cube_validator import CubeStateValidator


@dataclass(frozen=True, slots=True)
class Cube:
    """Immutable public façade over a valid CubeState."""

    state: CubeState

    def __post_init__(self) -> None:
        if not CubeStateValidator.is_valid(self.state):
            raise ValueError("Cube requires a valid CubeState.")

    @classmethod
    def canonical(cls) -> "Cube":
        """Returns a cube in the canonical solved state."""
        return cls(CANONICAL_CUBE_STATE)

    @property
    def orientation(self):
        return self.state.orientation

    @property
    def solved(self) -> bool:
        return self.state.solved

    def apply(self, move: Move) -> "Cube":
        return Cube(CubeTransformer.apply(self.state, move))

    def apply_algorithm(self, algorithm: Algorithm) -> "Cube":
        return Cube(CubeTransformer.apply_algorithm(self.state, algorithm))

    def apply_transformation(
        self,
        transformation: CubeTransformation,
    ) -> "Cube":
        return Cube(
            CubeTransformer.apply_transformation(
                self.state,
                transformation,
            )
        )

    def describe(self) -> str:
        return self.state.describe()

    def __str__(self) -> str:
        return self.describe()
