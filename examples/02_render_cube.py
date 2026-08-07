"""
Examples - Render Cube

Demonstrates rendering the cube before and after
performing moves.
"""

from cube import Cube, R, R_PRIME

from common.ascii_renderer import render


def print_heading(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print()


def main() -> None:
    cube = Cube.canonical()

    print_heading("Solved Cube")

    print(render(cube.state))

    cube = cube.apply(R)

    print_heading("After R")

    print(render(cube.state))

    cube = cube.apply(R_PRIME)

    print_heading("After R R'")

    print(render(cube.state))


if __name__ == "__main__":
    main()