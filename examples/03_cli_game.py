"""
Examples - CLI Cube Game

Interactive command-line Rubik's Cube game.

Commands
--------

    R U R' U'
        Apply one or more moves.

    scramble
        Generate a new scramble.

    reset
        Reset to the solved cube.

    help
        Show this help.

    quit
    exit
        Exit the game.
"""

from cube import Algorithm, Cube, ScrambleGenerator

from common.ascii_renderer import render


# ==============================================================================
# UI
# ==============================================================================

def print_heading(
    title: str,
) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_help() -> None:
    print(
        """
Commands

  <algorithm>    Apply an algorithm
                 Example:
                     R U R' U'

  scramble       Generate a random scramble

  reset          Reset to the solved cube

  help           Show this help

  quit
  exit           Exit the game
"""
    )


# ==============================================================================
# Main
# ==============================================================================

def main() -> None:
    cube = Cube.canonical()

    move_count = 0

    won = False

    print_heading(
        "CubeForge CLI Game"
    )

    print_help()

    while True:
        print()
        print(render(cube.state))
        print()

        solved = cube.solved

        print(
            f"Status       : {'Solved' if solved else 'Scrambled'}"
        )

        print(
            f"Moves played : {move_count}"
        )

        command = input(
            "\nCubeForge> "
        ).strip()

        if not command:
            continue

        lower = command.lower()

        # ----------------------------------------------------------------------
        # Exit
        # ----------------------------------------------------------------------

        if lower in (
            "quit",
            "exit",
        ):
            print("\nGoodbye!")
            return

        # ----------------------------------------------------------------------
        # Help
        # ----------------------------------------------------------------------

        if lower == "help":
            print_help()
            continue

        # ----------------------------------------------------------------------
        # Reset
        # ----------------------------------------------------------------------

        if lower == "reset":
            cube = Cube.canonical()
            move_count = 0
            won = False
            continue

        # ----------------------------------------------------------------------
        # Scramble
        # ----------------------------------------------------------------------

        if lower == "scramble":
            scramble = ScrambleGenerator.generate()

            print()
            print(
                f"Scramble : {scramble}"
            )

            cube = Cube.canonical().apply_algorithm(scramble)

            move_count = 0
            won = False

            continue

        # ----------------------------------------------------------------------
        # Algorithm
        # ----------------------------------------------------------------------

        try:
            algorithm = Algorithm.parse(
                command,
            )

            cube = cube.apply_algorithm(
                algorithm,
            )

            move_count += len(
                tuple(algorithm)
            )

            if not won and cube.solved:
                won = True

                print()
                print("=" * 70)
                print("🎉 Congratulations!")
                print(
                    f"You solved the cube in {move_count} moves!"
                )
                print("=" * 70)

        except ValueError as ex:
            print()
            print(
                f"Invalid command: {ex}"
            )


if __name__ == "__main__":
    main()