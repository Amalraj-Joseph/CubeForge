from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

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

    @classmethod
    def parse(cls, notation: str) -> Algorithm:
        """
        Parses Singmaster notation (e.g. "R U R' U'") into an Algorithm.

        Raises:
            ValueError: If any token is not a valid Move.
        """
        # Deferred to break a genuine import cycle: algorithm_parser
        # imports Algorithm to build its return value.
        from cube.notation.algorithm_parser import parse_algorithm

        return parse_algorithm(notation)

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

    @property
    def inverse(self) -> Algorithm:
        """
        Returns the Algorithm that undoes this Algorithm: each Move
        inverted, in reverse order.
        """
        return Algorithm(
            *(move.inverse for move in reversed(self.moves))
        )

    def compose(
        self,
        other: Algorithm,
    ) -> Algorithm:
        """
        Returns the Algorithm obtained by applying self then other.
        """
        return Algorithm(*self.moves, *other.moves)

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
