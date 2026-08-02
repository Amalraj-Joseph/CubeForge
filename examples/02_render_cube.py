"""
Examples - Render Cube

Demonstrates rendering the cube before and after
performing moves.
"""

from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)
from cube.internal.canonical_moves import (
    R,
    R_PRIME,
)

from common.ascii_renderer import render


def print_heading(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print()


def main() -> None:
    cube = CANONICAL_CUBE_STATE

    print_heading("Solved Cube")

    print(render(cube))

    cube = CubeTransformer.apply(
        cube,
        R,
    )

    print_heading("After R")

    print(render(cube))

    cube = CubeTransformer.apply(
        cube,
        R_PRIME,
    )

    print_heading("After R R'")

    print(render(cube))


if __name__ == "__main__":
    main()