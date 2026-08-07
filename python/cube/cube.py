from __future__ import annotations

from dataclasses import dataclass

from cube.algorithm.algorithm import Algorithm
from cube.analysis.cube_analyzer import CubeAnalyzer
from cube.cube_state import CubeState
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.move.move import Move
from cube.piece.piece_state import PieceState
from cube.serialization.cube_serializer import CubeSerializer
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

    @classmethod
    def from_json(cls, text: str) -> "Cube":
        """Constructs a Cube from a JSON string produced by `to_json`."""
        return cls(CubeSerializer.from_json(text))

    @classmethod
    def from_dict(cls, data: dict) -> "Cube":
        """Constructs a Cube from a dict produced by `to_dict`."""
        return cls(CubeSerializer.from_dict(data))

    @classmethod
    def from_compact_string(cls, text: str) -> "Cube":
        """Constructs a Cube from a string produced by `to_compact_string`."""
        return cls(CubeSerializer.from_compact_string(text))

    @property
    def orientation(self):
        return self.state.orientation

    @property
    def solved(self) -> bool:
        return self.state.solved

    def misplaced_pieces(self) -> tuple[PieceState, ...]:
        return CubeAnalyzer.misplaced_pieces(self.state)

    def misplaced_edges(self) -> tuple[PieceState, ...]:
        return CubeAnalyzer.misplaced_edges(self.state)

    def misplaced_corners(self) -> tuple[PieceState, ...]:
        return CubeAnalyzer.misplaced_corners(self.state)

    def edge_orientation_errors(self) -> tuple[PieceState, ...]:
        return CubeAnalyzer.edge_orientation_errors(self.state)

    def corner_orientation_errors(self) -> tuple[PieceState, ...]:
        return CubeAnalyzer.corner_orientation_errors(self.state)

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

    def to_json(self) -> str:
        return CubeSerializer.to_json(self.state)

    def to_dict(self) -> dict:
        return CubeSerializer.to_dict(self.state)

    def to_compact_string(self) -> str:
        return CubeSerializer.to_compact_string(self.state)

    def __str__(self) -> str:
        return self.describe()
