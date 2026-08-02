from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from cube.move.move import Move


@dataclass(frozen=True, slots=True)
class Algorithm:
    """
    Immutable sequence of Moves.
    """

    moves: tuple[Move, ...]

    def __init__(
        self,
        *moves: Move,
    ) -> None:
        for move in moves:
            if not isinstance(
                move,
                Move,
            ):
                raise TypeError(
                    "Algorithm accepts only Move instances."
                )

        object.__setattr__(
            self,
            "moves",
            tuple(moves),
        )

    @property
    def notation(self) -> str:
        """
        Returns the Singmaster notation.
        """
        return " ".join(
            move.notation
            for move in self.moves
        )

    @property
    def description(self) -> str:
        """
        Returns a human-readable description.
        """
        return (
            f"Algorithm({self.notation})"
        )

    def __len__(
        self,
    ) -> int:
        return len(self.moves)

    def __iter__(
        self,
    ) -> Iterator[Move]:
        return iter(self.moves)

    def __getitem__(
        self,
        index,
    ):
        return self.moves[index]

    def __contains__(
        self,
        move: Move,
    ) -> bool:
        return move in self.moves

    def describe(self) -> str:
        """
        Returns a human-readable description.
        """
        return self.description

    def __str__(self) -> str:
        return self.description