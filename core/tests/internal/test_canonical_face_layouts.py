from cube.face.logical_face import LogicalFace
from cube.internal.canonical_face_layouts import (
    FACE_LAYOUTS,
)
from cube.internal.canonical_positions import (
    ALL_POSITIONS,
    B,
    BL,
    BR,
    D,
    DB,
    DBR,
    DF,
    DFL,
    DL,
    DLB,
    DR,
    DRF,
    F,
    FL,
    FR,
    L,
    R,
    U,
    UB,
    UBL,
    UF,
    UFR,
    UL,
    ULF,
    UR,
    URB,
)

# ==============================================================================
# Counts
# ==============================================================================

def test_contains_six_face_layouts():
    assert len(FACE_LAYOUTS) == 6


def test_each_face_contains_nine_positions():
    assert all(
        len(layout) == 9
        for layout in FACE_LAYOUTS.values()
    )


# ==============================================================================
# Canonical Layouts
# ==============================================================================

def test_up_face_layout():
    assert FACE_LAYOUTS[
        LogicalFace.UP
    ] == (
        ULF,
        UF,
        UFR,
        UL,
        U,
        UR,
        UBL,
        UB,
        URB,
    )


def test_down_face_layout():
    assert FACE_LAYOUTS[
        LogicalFace.DOWN
    ] == (
        DFL,
        DF,
        DRF,
        DL,
        D,
        DR,
        DLB,
        DB,
        DBR,
    )


def test_front_face_layout():
    assert FACE_LAYOUTS[
        LogicalFace.FRONT
    ] == (
        ULF,
        UF,
        UFR,
        FL,
        F,
        FR,
        DFL,
        DF,
        DRF,
    )


def test_back_face_layout():
    assert FACE_LAYOUTS[
        LogicalFace.BACK
    ] == (
        URB,
        UB,
        UBL,
        BR,
        B,
        BL,
        DBR,
        DB,
        DLB,
    )


def test_left_face_layout():
    assert FACE_LAYOUTS[
        LogicalFace.LEFT
    ] == (
        UBL,
        UL,
        ULF,
        BL,
        L,
        FL,
        DLB,
        DL,
        DFL,
    )


def test_right_face_layout():
    assert FACE_LAYOUTS[
        LogicalFace.RIGHT
    ] == (
        UFR,
        UR,
        URB,
        FR,
        R,
        BR,
        DRF,
        DR,
        DBR,
    )


# ==============================================================================
# Uniqueness
# ==============================================================================

def test_each_face_has_unique_positions():
    for layout in FACE_LAYOUTS.values():
        assert len(layout) == len(set(layout))


# ==============================================================================
# Lookup
# ==============================================================================

def test_lookup():
    assert (
        FACE_LAYOUTS[LogicalFace.UP][4]
        is U
    )

    assert (
        FACE_LAYOUTS[LogicalFace.FRONT][4]
        is F
    )

    assert (
        FACE_LAYOUTS[LogicalFace.RIGHT][4]
        is R
    )


# ==============================================================================
# Contract
# ==============================================================================

def test_face_layout_contract():
    for face, layout in FACE_LAYOUTS.items():
        assert face in LogicalFace

        assert len(layout) == 9

        assert len(set(layout)) == 9

        assert all(
            position in ALL_POSITIONS
            for position in layout
        )
