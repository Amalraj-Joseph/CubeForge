from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterator, Mapping

from cube.orientation.cube_orientation import CubeOrientation
from cube.piece.piece import Piece
from cube.piece.piece_state import PieceState
from cube.position.position import Position


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
