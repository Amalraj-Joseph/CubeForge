import pytest

from cube.algorithm.algorithm import Algorithm
from cube.cube_transformer import CubeTransformer
from cube.internal.canonical_cube_state import CANONICAL_CUBE_STATE
from cube.internal.canonical_moves import F, R, U
from cube.serialization import CubeSerializer, FORMAT_VERSION
from cube.transformation import ROTATE_UP


ROUND_TRIP_FORMATS = (
    (CubeSerializer.to_dict, CubeSerializer.from_dict),
    (CubeSerializer.to_json, CubeSerializer.from_json),
    (CubeSerializer.to_compact_string, CubeSerializer.from_compact_string),
)


def scrambled_cube():
    return CubeTransformer.apply_algorithm(
        CANONICAL_CUBE_STATE,
        Algorithm(R, U, F, R, U),
    )


def non_canonical_orientation_cube():
    return CubeTransformer.apply_transformation(
        CANONICAL_CUBE_STATE,
        ROTATE_UP,
    )


# ----------------------------------------------------------------------
# Round trips
# ----------------------------------------------------------------------

@pytest.mark.parametrize("to_fn,from_fn", ROUND_TRIP_FORMATS)
def test_round_trip_canonical_cube(to_fn, from_fn):
    assert from_fn(to_fn(CANONICAL_CUBE_STATE)) == CANONICAL_CUBE_STATE


@pytest.mark.parametrize("to_fn,from_fn", ROUND_TRIP_FORMATS)
def test_round_trip_scrambled_cube(to_fn, from_fn):
    cube = scrambled_cube()
    assert from_fn(to_fn(cube)) == cube


@pytest.mark.parametrize("to_fn,from_fn", ROUND_TRIP_FORMATS)
def test_round_trip_non_canonical_orientation(to_fn, from_fn):
    cube = non_canonical_orientation_cube()
    restored = from_fn(to_fn(cube))

    assert restored == cube
    assert restored.orientation == cube.orientation
    assert restored.orientation != CANONICAL_CUBE_STATE.orientation


# ----------------------------------------------------------------------
# Format version
# ----------------------------------------------------------------------

def test_to_dict_includes_format_version():
    data = CubeSerializer.to_dict(CANONICAL_CUBE_STATE)
    assert data["format_version"] == FORMAT_VERSION


def test_from_dict_rejects_unsupported_format_version():
    data = CubeSerializer.to_dict(CANONICAL_CUBE_STATE)
    data["format_version"] = "999"

    with pytest.raises(ValueError, match="format_version"):
        CubeSerializer.from_dict(data)


def test_from_compact_string_rejects_unsupported_format_version():
    with pytest.raises(ValueError, match="format_version"):
        CubeSerializer.from_compact_string("999:WG|U=W0")


# ----------------------------------------------------------------------
# Malformed input
# ----------------------------------------------------------------------

def test_from_json_rejects_invalid_json():
    with pytest.raises(ValueError, match="Invalid JSON"):
        CubeSerializer.from_json("not json at all {{{")


def test_from_dict_rejects_missing_fields():
    with pytest.raises(ValueError):
        CubeSerializer.from_dict({"format_version": FORMAT_VERSION})


def test_from_dict_rejects_non_dict_input():
    with pytest.raises(ValueError):
        CubeSerializer.from_dict(["not", "a", "dict"])


def test_from_compact_string_rejects_text_without_separator():
    with pytest.raises(ValueError):
        CubeSerializer.from_compact_string("garbage-no-pipe-or-colon")


def test_from_compact_string_rejects_unknown_color_initial():
    with pytest.raises(ValueError, match="color initial"):
        CubeSerializer.from_compact_string(f"{FORMAT_VERSION}:WG|U=Q0")


def test_from_compact_string_rejects_impossible_piece_colors():
    # W (White) and Y (Yellow) are opposite colors: no real edge has both.
    # PieceSignature itself rejects this before CubeSerializer's own
    # "unknown signature" check is ever reached - either way, malformed
    # color data must surface as a clear ValueError, not a crash.
    with pytest.raises(ValueError, match="not permitted"):
        CubeSerializer.from_compact_string(f"{FORMAT_VERSION}:WG|UF=WY0")


def test_from_compact_string_rejects_wrong_color_count_for_position():
    # "U" is a Center position (1 face) but two colors are given.
    with pytest.raises(ValueError):
        CubeSerializer.from_compact_string(f"{FORMAT_VERSION}:WG|U=WG0")


# ----------------------------------------------------------------------
# CubeState invariants are preserved through deserialization
# ----------------------------------------------------------------------

def test_deserialization_rejects_states_that_violate_parity():
    data = CubeSerializer.to_dict(CANONICAL_CUBE_STATE)

    for entry in data["pieces"]:
        if entry["position"] == "UF":
            entry["orientation"] = 1
            break

    with pytest.raises(ValueError, match="edge orientation"):
        CubeSerializer.from_dict(data)


def test_deserialization_rejects_duplicate_position_occupancy():
    data = CubeSerializer.to_dict(CANONICAL_CUBE_STATE)

    data["pieces"][1]["position"] = data["pieces"][0]["position"]

    with pytest.raises(ValueError):
        CubeSerializer.from_dict(data)