from __future__ import annotations

from cube.color.color import Color
from cube.cube_state import CubeState
from cube.face.logical_face import LogicalFace
from cube.internal.canonical_face_layouts import (
    FACE_LAYOUTS,
)

# ==============================================================================
# ANSI Colours
# ==============================================================================

_RESET = "\033[0m"

_BACKGROUND = {
    # Slightly off-white so it remains visible on bright terminals.
    Color.WHITE: "48;5;255",

    # Bright lemon yellow.
    Color.YELLOW: "48;5;226",

    Color.GREEN: "42",
    Color.BLUE: "44",
    Color.RED: "41",

    # Deep cube orange.
    Color.ORANGE: "48;5;202",
}

# ==============================================================================
# Layout
# ==============================================================================

_STICKER_WIDTH = 3

_FACE_GAP = "   "

_TOP_INDENT = " " * 18


# ==============================================================================
# Public API
# ==============================================================================

def render(
    cube: CubeState,
) -> str:
    """
    Returns an ANSI-rendered cube net.
    """
    rendered_faces = {
        face: _render_face(
            cube,
            face,
        )
        for face in LogicalFace
    }

    lines: list[str] = []

    # --------------------------------------------------------------------------
    # Up
    # --------------------------------------------------------------------------

    for row in rendered_faces[
        LogicalFace.UP
    ]:
        lines.append(
            f"{_TOP_INDENT}{row}"
        )

    lines.append("")

    # --------------------------------------------------------------------------
    # Middle
    # --------------------------------------------------------------------------

    for row in range(7):
        lines.append(
            _FACE_GAP.join(
                (
                    rendered_faces[
                        LogicalFace.LEFT
                    ][row],
                    rendered_faces[
                        LogicalFace.FRONT
                    ][row],
                    rendered_faces[
                        LogicalFace.RIGHT
                    ][row],
                    rendered_faces[
                        LogicalFace.BACK
                    ][row],
                )
            )
        )

    lines.append("")

    # --------------------------------------------------------------------------
    # Down
    # --------------------------------------------------------------------------

    for row in rendered_faces[
        LogicalFace.DOWN
    ]:
        lines.append(
            f"{_TOP_INDENT}{row}"
        )

    return "\n".join(lines)


# ==============================================================================
# Helpers
# ==============================================================================

def _render_face(
    cube: CubeState,
    face: LogicalFace,
) -> tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
]:
    """
    Renders a single cube face.
    """
    stickers = [
        _render_sticker(
            cube
            .piece_at(position)
            .color_on(face)
        )
        for position in FACE_LAYOUTS[face]
    ]

    top = "┌───┬───┬───┐"

    separator = "├───┼───┼───┤"

    bottom = "└───┴───┴───┘"

    row_0 = (
        "│"
        + "│".join(stickers[0:3])
        + "│"
    )

    row_1 = (
        "│"
        + "│".join(stickers[3:6])
        + "│"
    )

    row_2 = (
        "│"
        + "│".join(stickers[6:9])
        + "│"
    )

    return (
        top,
        row_0,
        separator,
        row_1,
        separator,
        row_2,
        bottom,
    )


def _render_sticker(
    color: Color,
) -> str:
    """
    Renders a single coloured sticker.
    """
    return (
        f"\033[{_BACKGROUND[color]}m"
        + (" " * _STICKER_WIDTH)
        + _RESET
    )