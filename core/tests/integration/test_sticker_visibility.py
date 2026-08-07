from cube.color.color import Color
from cube.cube_transformer import CubeTransformer
from cube.face.logical_face import LogicalFace
from cube.internal.canonical_cube_state import (
    CANONICAL_CUBE_STATE,
)
from cube.internal.canonical_face_layouts import (
    FACE_LAYOUTS,
)
from cube.internal.canonical_moves import (
    ALL_MOVES,
    R,
    R_PRIME,
)
from cube.internal.canonical_pieces import (
    GREEN_RED_EDGE,
)
from cube.internal.canonical_positions import (
    UR,
)
from cube.piece.piece_type import PieceType


def test_color_on_after_r_move():
    cube = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R,
    )

    edge = cube.piece_at(UR)

    assert edge.piece is GREEN_RED_EDGE

    assert (
        edge.color_on(
            LogicalFace.UP,
        )
        is Color.GREEN
    )

    assert (
        edge.color_on(
            LogicalFace.RIGHT,
        )
        is Color.RED
    )


def test_color_on_all_face_positions_after_moves():
    for move in ALL_MOVES:
        cube = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            move,
        )

        for face in LogicalFace:
            for position in FACE_LAYOUTS[face]:
                piece_state = cube.piece_at(position)

                color = piece_state.color_on(face)

                assert color is not None


def test_centers_unchanged_after_moves():
    for move in ALL_MOVES:
        cube = CubeTransformer.apply(
            CANONICAL_CUBE_STATE,
            move,
        )

        for piece_state in cube:
            if (
                piece_state.piece_type
                is not PieceType.CENTER
            ):
                continue

            face = next(
                iter(
                    piece_state.position.faces,
                )
            )

            assert (
                piece_state.color_on(face)
                is next(
                    iter(
                        piece_state.piece.colors,
                    )
                )
            )


def test_move_inverse_restores_stickers():
    cube = CubeTransformer.apply(
        CANONICAL_CUBE_STATE,
        R,
    )

    cube = CubeTransformer.apply(
        cube,
        R_PRIME,
    )

    for face in LogicalFace:
        for position in FACE_LAYOUTS[face]:
            solved = (
                CANONICAL_CUBE_STATE
                .piece_at(position)
                .color_on(face)
            )

            restored = (
                cube
                .piece_at(position)
                .color_on(face)
            )

            assert restored is solved
