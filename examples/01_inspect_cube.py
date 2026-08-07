"""
Examples - Inspect Cube

Demonstrates the basic CubeCore domain model by
creating the canonical solved cube and printing
its contents.
"""

from cube import Cube


def main() -> None:
    cube = Cube.canonical()

    print("=" * 60)
    print("CubeCore - Cube Inspection")
    print("=" * 60)
    print()

    print(f"Cube Type : {type(cube.state).__name__}")
    print(f"Piece Count: {len(cube.state)}")
    print()

    print("-" * 60)
    print("Piece States")
    print("-" * 60)

    for piece_state in cube.state:
        print(
            f"{str(piece_state.piece):<32}"
            f"Position={str(piece_state.position):<4}"
            f"Orientation={piece_state.orientation.value}"
        )


if __name__ == "__main__":
    main()