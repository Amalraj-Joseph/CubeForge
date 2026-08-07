import pytest

from cube import Cube, SPECIFICATION_VERSION
from cube.internal.canonical_moves import F, R, U
from cube.transformation import ROTATE_UP


def test_constructs_a_canonical_cube():
    cube = Cube.canonical()

    assert cube.solved
    assert len(cube.state) == 26
    assert SPECIFICATION_VERSION == "v1"


def test_cube_facade_applies_moves_and_transformations():
    moved = Cube.canonical().apply(R)
    transformed = moved.apply_transformation(ROTATE_UP)

    assert not moved.solved
    assert not transformed.solved
    assert transformed.orientation.top.name == "BLUE"


def test_cube_and_piece_state_descriptions_are_human_readable():
    cube = Cube.canonical()

    assert "Orientation:" in cube.describe()
    assert "Piece=" in cube.describe()


def test_cube_string_representation_matches_describe():
    cube = Cube.canonical()

    assert str(cube) == cube.describe()


def test_cube_rejects_a_non_cube_state():
    with pytest.raises((ValueError, TypeError)):
        Cube("not a CubeState")


# ----------------------------------------------------------------------
# Analysis delegation
# ----------------------------------------------------------------------

def scrambled_cube() -> Cube:
    return Cube.canonical().apply(R).apply(U).apply(F)


def test_canonical_cube_has_no_analysis_errors():
    cube = Cube.canonical()

    assert cube.misplaced_pieces() == ()
    assert cube.misplaced_edges() == ()
    assert cube.misplaced_corners() == ()
    assert cube.edge_orientation_errors() == ()
    assert cube.corner_orientation_errors() == ()


def test_scrambled_cube_reports_analysis_errors_matching_analyzer():
    from cube.analysis import CubeAnalyzer

    cube = scrambled_cube()

    assert cube.misplaced_pieces() == CubeAnalyzer.misplaced_pieces(cube.state)
    assert cube.misplaced_edges() == CubeAnalyzer.misplaced_edges(cube.state)
    assert cube.misplaced_corners() == CubeAnalyzer.misplaced_corners(cube.state)
    assert cube.edge_orientation_errors() == (
        CubeAnalyzer.edge_orientation_errors(cube.state)
    )
    assert cube.corner_orientation_errors() == (
        CubeAnalyzer.corner_orientation_errors(cube.state)
    )
    assert len(cube.misplaced_pieces()) > 0


# ----------------------------------------------------------------------
# Serialization delegation
# ----------------------------------------------------------------------

ROUND_TRIP_FORMATS = (
    (Cube.to_dict, Cube.from_dict),
    (Cube.to_json, Cube.from_json),
    (Cube.to_compact_string, Cube.from_compact_string),
)


@pytest.mark.parametrize("to_fn,from_fn", ROUND_TRIP_FORMATS)
def test_cube_facade_round_trips_through_every_format(to_fn, from_fn):
    cube = scrambled_cube()

    restored = from_fn(to_fn(cube))

    assert restored == cube
    assert restored.state == cube.state


def test_cube_from_json_rejects_malformed_input():
    with pytest.raises(ValueError):
        Cube.from_json("not json at all {{{")
