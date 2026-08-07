from __future__ import annotations

from cube.algorithm.algorithm import Algorithm


def format_algorithm(
    algorithm: Algorithm,
) -> str:
    """
    Formats an Algorithm as canonical notation.
    """
    if not isinstance(
        algorithm,
        Algorithm,
    ):
        raise TypeError(
            "format_algorithm() requires an Algorithm."
        )

    return algorithm.notation
