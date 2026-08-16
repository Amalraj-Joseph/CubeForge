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
    R_PRIME,
    U,
    U2,
    U_PRIME,
)
from cube.internal.canonical_pieces import (
    GREEN_RED_EDGE,
    WHITE_BLUE_ORANGE_CORNER,
    WHITE_ORANGE_GREEN_CORNER,
    WHITE_RED_BLUE_CORNER,
    YELLOW_BLUE_RED_CORNER,
    YELLOW_GREEN_ORANGE_CORNER,
    YELLOW_ORANGE_BLUE_CORNER,
    YELLOW_RED_GREEN_CORNER,
)
from cube.internal.canonical_positions import (
    DFL,
    ULF,
    UFR,
    UR,
    URB,
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


# ==============================================================================
# Concrete reference states - one clockwise, one prime, one double turn per
# face (U, D, F, B, L; R is covered above). Expected values were derived
# independently (a from-scratch 3D rotation model, not CubeTransformer) and
# cross-checked against this implementation before being hardcoded here.
# See specs/v1/conformance-tests.md's "Move Tests" section.
# ==============================================================================

def test_color_on_after_u_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, U)

    corner = cube.piece_at(UFR)

    assert corner.piece is WHITE_ORANGE_GREEN_CORNER
    assert corner.color_on(LogicalFace.UP) is Color.WHITE
    assert corner.color_on(LogicalFace.RIGHT) is Color.GREEN
    assert corner.color_on(LogicalFace.FRONT) is Color.ORANGE


def test_color_on_after_u_prime_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, U_PRIME)

    corner = cube.piece_at(UFR)

    assert corner.piece is WHITE_RED_BLUE_CORNER
    assert corner.color_on(LogicalFace.UP) is Color.WHITE
    assert corner.color_on(LogicalFace.RIGHT) is Color.BLUE
    assert corner.color_on(LogicalFace.FRONT) is Color.RED


def test_color_on_after_u2_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, U2)

    corner = cube.piece_at(UFR)

    assert corner.piece is WHITE_BLUE_ORANGE_CORNER
    assert corner.color_on(LogicalFace.UP) is Color.WHITE
    assert corner.color_on(LogicalFace.RIGHT) is Color.ORANGE
    assert corner.color_on(LogicalFace.FRONT) is Color.BLUE


def test_color_on_after_d_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, D)

    corner = cube.piece_at(DFL)

    assert corner.piece is YELLOW_ORANGE_BLUE_CORNER
    assert corner.color_on(LogicalFace.DOWN) is Color.YELLOW
    assert corner.color_on(LogicalFace.LEFT) is Color.BLUE
    assert corner.color_on(LogicalFace.FRONT) is Color.ORANGE


def test_color_on_after_d_prime_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, D_PRIME)

    corner = cube.piece_at(DFL)

    assert corner.piece is YELLOW_RED_GREEN_CORNER
    assert corner.color_on(LogicalFace.DOWN) is Color.YELLOW
    assert corner.color_on(LogicalFace.LEFT) is Color.GREEN
    assert corner.color_on(LogicalFace.FRONT) is Color.RED


def test_color_on_after_d2_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, D2)

    corner = cube.piece_at(DFL)

    assert corner.piece is YELLOW_BLUE_RED_CORNER
    assert corner.color_on(LogicalFace.DOWN) is Color.YELLOW
    assert corner.color_on(LogicalFace.LEFT) is Color.RED
    assert corner.color_on(LogicalFace.FRONT) is Color.BLUE


def test_color_on_after_f_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, F)

    corner = cube.piece_at(UFR)

    assert corner.piece is WHITE_ORANGE_GREEN_CORNER
    assert corner.color_on(LogicalFace.FRONT) is Color.GREEN
    assert corner.color_on(LogicalFace.RIGHT) is Color.WHITE
    assert corner.color_on(LogicalFace.UP) is Color.ORANGE


def test_color_on_after_f_prime_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, F_PRIME)

    corner = cube.piece_at(UFR)

    assert corner.piece is YELLOW_RED_GREEN_CORNER
    assert corner.color_on(LogicalFace.FRONT) is Color.GREEN
    assert corner.color_on(LogicalFace.RIGHT) is Color.YELLOW
    assert corner.color_on(LogicalFace.UP) is Color.RED


def test_color_on_after_f2_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, F2)

    corner = cube.piece_at(UFR)

    assert corner.piece is YELLOW_GREEN_ORANGE_CORNER
    assert corner.color_on(LogicalFace.FRONT) is Color.GREEN
    assert corner.color_on(LogicalFace.RIGHT) is Color.ORANGE
    assert corner.color_on(LogicalFace.UP) is Color.YELLOW


def test_color_on_after_b_move():
    """
    Regression test: B_CORNER previously cycled the back-layer corners in
    the opposite rotational direction from B_EDGE, placing the wrong
    corner piece (and wrong colors) at every B-layer corner position.
    """
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, B)

    corner = cube.piece_at(URB)

    assert corner.piece is YELLOW_BLUE_RED_CORNER
    assert corner.color_on(LogicalFace.RIGHT) is Color.YELLOW
    assert corner.color_on(LogicalFace.BACK) is Color.BLUE
    assert corner.color_on(LogicalFace.UP) is Color.RED


def test_color_on_after_b_prime_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, B_PRIME)

    corner = cube.piece_at(URB)

    assert corner.piece is WHITE_BLUE_ORANGE_CORNER
    assert corner.color_on(LogicalFace.RIGHT) is Color.WHITE
    assert corner.color_on(LogicalFace.BACK) is Color.BLUE
    assert corner.color_on(LogicalFace.UP) is Color.ORANGE


def test_color_on_after_b2_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, B2)

    corner = cube.piece_at(URB)

    assert corner.piece is YELLOW_ORANGE_BLUE_CORNER
    assert corner.color_on(LogicalFace.RIGHT) is Color.ORANGE
    assert corner.color_on(LogicalFace.BACK) is Color.BLUE
    assert corner.color_on(LogicalFace.UP) is Color.YELLOW


def test_color_on_after_l_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, L)

    corner = cube.piece_at(ULF)

    assert corner.piece is WHITE_BLUE_ORANGE_CORNER
    assert corner.color_on(LogicalFace.UP) is Color.BLUE
    assert corner.color_on(LogicalFace.LEFT) is Color.ORANGE
    assert corner.color_on(LogicalFace.FRONT) is Color.WHITE


def test_color_on_after_l_prime_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, L_PRIME)

    corner = cube.piece_at(ULF)

    assert corner.piece is YELLOW_GREEN_ORANGE_CORNER
    assert corner.color_on(LogicalFace.UP) is Color.GREEN
    assert corner.color_on(LogicalFace.LEFT) is Color.ORANGE
    assert corner.color_on(LogicalFace.FRONT) is Color.YELLOW


def test_color_on_after_l2_move():
    cube = CubeTransformer.apply(CANONICAL_CUBE_STATE, L2)

    corner = cube.piece_at(ULF)

    assert corner.piece is YELLOW_ORANGE_BLUE_CORNER
    assert corner.color_on(LogicalFace.UP) is Color.YELLOW
    assert corner.color_on(LogicalFace.LEFT) is Color.ORANGE
    assert corner.color_on(LogicalFace.FRONT) is Color.BLUE


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
