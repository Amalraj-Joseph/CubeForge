from __future__ import annotations

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


MOVE_LOOKUP = {
    "U": U,
    "U2": U2,
    "U'": U_PRIME,

    "D": D,
    "D2": D2,
    "D'": D_PRIME,

    "F": F,
    "F2": F2,
    "F'": F_PRIME,

    "B": B,
    "B2": B2,
    "B'": B_PRIME,

    "L": L,
    "L2": L2,
    "L'": L_PRIME,

    "R": R,
    "R2": R2,
    "R'": R_PRIME,
}


def parse_algorithm(
    notation: str,
) -> Algorithm:
    """
    Parses Singmaster notation into an Algorithm.
    """
    notation = notation.strip()

    if not notation:
        return Algorithm()

    moves = []

    for token in notation.split():
        try:
            moves.append(
                MOVE_LOOKUP[token]
            )

        except KeyError as error:
            raise ValueError(
                f"Invalid move: {token}"
            ) from error

    return Algorithm(*moves)