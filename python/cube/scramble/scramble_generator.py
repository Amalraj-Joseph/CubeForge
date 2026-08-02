from __future__ import annotations

import random

from cube.algorithm.algorithm import Algorithm
from cube.internal.canonical_moves import (
    B,
    B2,
    B_PRIME,
    D,
    D2,
    D_PRIME,
    F,
    F2,
    F_PRIME,
    L,
    L2,
    L_PRIME,
    R,
    R2,
    R_PRIME,
    U,
    U2,
    U_PRIME,
)
from cube.move.move import Move


_MOVES: tuple[Move, ...] = (
    U,
    U2,
    U_PRIME,
    D,
    D2,
    D_PRIME,
    F,
    F2,
    F_PRIME,
    B,
    B2,
    B_PRIME,
    L,
    L2,
    L_PRIME,
    R,
    R2,
    R_PRIME,
)


class ScrambleGenerator:
    """
    Generates random Rubik's Cube scramble Algorithms.
    """

    DEFAULT_LENGTH = 25

    @staticmethod
    def generate(
        length: int = DEFAULT_LENGTH,
    ) -> Algorithm:
        """
        Generates a random scramble Algorithm.

        Consecutive moves never turn the same face.
        """
        if length < 0:
            raise ValueError(
                "Scramble length must be non-negative."
            )

        moves: list[Move] = []

        previous_face = None

        while len(moves) < length:
            move = random.choice(
                _MOVES,
            )

            if move.face is previous_face:
                continue

            moves.append(move)
            previous_face = move.face

        return Algorithm(
            *moves,
        )