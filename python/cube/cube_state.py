from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterator, Mapping

from cube.orientation.cube_orientation import CubeOrientation
from cube.internal.canonical_cube import CANONICAL_CUBE
from cube.piece.piece import Piece
from cube.piece.piece_state import PieceState
from cube.piece.piece_type import PieceType
from cube.position.position import Position
from cube.internal.canonical_positions import (
    CORNER_POSITIONS,
    EDGE_POSITIONS,
)


_CANONICAL_SIGNATURES = frozenset(
    piece.signature
    for piece in CANONICAL_CUBE
)


@dataclass(frozen=True, slots=True, init=False)
class CubeState:
    """
    Immutable state of a Rubik's Cube.

    A CubeState consists of one CubeOrientation and exactly 26 PieceStates.
    """

    orientation: CubeOrientation
    _by_piece: Mapping[Piece, PieceState] = field(repr=False)
    _by_position: Mapping[Position, PieceState] = field(repr=False)

    def __init__(
        self,
        orientation: CubeOrientation,
        *piece_states: PieceState,
    ):
        if not isinstance(orientation, CubeOrientation):
            raise ValueError(
                "CubeState orientation must be a CubeOrientation."
            )

        if len(piece_states) != 26:
            raise ValueError(
                "CubeState must contain exactly 26 PieceStates."
            )

        by_piece: dict[Piece, PieceState] = {}
        by_position: dict[Position, PieceState] = {}

        for piece_state in piece_states:
            piece = piece_state.piece
            position = piece_state.position

            if piece in by_piece:
                raise ValueError(
                    "Duplicate Piece detected."
                )

            if position in by_position:
                raise ValueError(
                    "Duplicate Position detected."
                )

            by_piece[piece] = piece_state
            by_position[position] = piece_state

        if {
            piece_state.piece.signature
            for piece_state in piece_states
        } != _CANONICAL_SIGNATURES:
            raise ValueError(
                "CubeState must contain every canonical PieceSignature exactly once."
            )

        center_states = [
            piece_state
            for piece_state in piece_states
            if piece_state.piece_type is PieceType.CENTER
        ]
        edge_states = [
            piece_state
            for piece_state in piece_states
            if piece_state.piece_type is PieceType.EDGE
        ]
        corner_states = [
            piece_state
            for piece_state in piece_states
            if piece_state.piece_type is PieceType.CORNER
        ]

        for piece_state in center_states:
            face = piece_state.position.ordered_faces[0]

            if not piece_state.piece.signature.contains(
                orientation.color_at(face)
            ):
                raise ValueError(
                    "CubeState center placement does not agree with "
                    "CubeOrientation."
                )

        if sum(state.orientation.value for state in edge_states) % 2:
            raise ValueError("CubeState has an invalid edge orientation sum.")

        if sum(state.orientation.value for state in corner_states) % 3:
            raise ValueError("CubeState has an invalid corner orientation sum.")

        if _permutation_parity(
            tuple(
                by_position[position].piece.signature
                for position in EDGE_POSITIONS
            ),
            _expected_signatures(EDGE_POSITIONS, orientation),
        ) != _permutation_parity(
            tuple(
                by_position[position].piece.signature
                for position in CORNER_POSITIONS
            ),
            _expected_signatures(CORNER_POSITIONS, orientation),
        ):
            raise ValueError("CubeState has mismatched piece permutation parity.")

        object.__setattr__(
            self,
            "orientation",
            orientation,
        )

        object.__setattr__(
            self,
            "_by_piece",
            MappingProxyType(by_piece),
        )

        object.__setattr__(
            self,
            "_by_position",
            MappingProxyType(by_position),
        )

    def __hash__(self) -> int:
        return hash((
            self.orientation,
            frozenset(self._by_piece.items()),
        ))

    @property
    def solved(self) -> bool:
        """
        Returns whether every visible sticker matches its face center.
        """
        return all(
            piece_state.color_on(face)
            is self.orientation.color_at(face)
            for piece_state in self
            for face in piece_state.position.faces
        )

    def piece_at(
        self,
        position: Position,
    ) -> PieceState:
        """
        Returns the PieceState occupying the given Position.
        """
        return self._by_position[position]

    def __contains__(
        self,
        piece: Piece,
    ) -> bool:
        """
        Returns True if the Piece exists in this CubeState.
        """
        return piece in self._by_piece

    def __getitem__(
        self,
        piece: Piece,
    ) -> PieceState:
        """
        Returns the PieceState for the given Piece.
        """
        return self._by_piece[piece]

    def __iter__(
        self,
    ) -> Iterator[PieceState]:
        """
        Iterates over all PieceStates.
        """
        return iter(self._by_piece.values())

    def __len__(
        self,
    ) -> int:
        """
        Returns the number of PieceStates.
        """
        return len(self._by_piece)

    def describe(self) -> str:
        """
        Returns a human-readable description of the entire cube state.
        """
        piece_states = sorted(
            self,
            key=lambda state: state.position.notation,
        )

        return "\n".join((
            f"Orientation: {self.orientation.describe()}",
            *(state.describe() for state in piece_states),
        ))

    def __str__(self) -> str:
        return self.describe()


def _permutation_parity(
    signatures,
    canonical_signatures,
) -> int:
    indexes = [
        canonical_signatures.index(signature)
        for signature in signatures
    ]
    inversions = sum(
        left > right
        for index, left in enumerate(indexes)
        for right in indexes[index + 1:]
    )

    return inversions % 2


def _expected_signatures(
    positions,
    orientation: CubeOrientation,
):
    from cube.piece.piece_signature import PieceSignature

    return tuple(
        PieceSignature(
            PieceType(position.position_type.value),
            *(orientation.color_at(face) for face in position.ordered_faces),
        )
        for position in positions
    )
