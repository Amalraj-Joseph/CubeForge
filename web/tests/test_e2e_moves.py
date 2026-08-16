"""
Browser-level end-to-end tests for the CubeForge Web UI.

These drive a real Flask server (see conftest.live_server_url) with a real
headless browser via Playwright, clicking the actual move buttons in
index.html. Expected face-color grids are computed by calling the same
`get_face_colors`/`MOVE_MAP` the app itself uses, applied to `Cube`
directly - not a second, hand-maintained copy of reference colors. This
also reuses the same CubeForge move semantics the backend regression
tests in core/tests/integration/test_sticker_visibility.py check, so a
regression like the original B_CORNER bug would fail both here and there.

The 3D scene is rendered with WebGL/Three.js, which isn't reliably
readable pixel-by-pixel across environments/GPUs. Instead, these tests
capture the exact JSON response the page receives and immediately renders
(`buildCube(data.faces)` in app.js) - that response IS what gets drawn,
so asserting on it is equivalent to asserting on the rendered grids
without the flakiness of screen-space pixel sampling.
"""

import app as app_module
import pytest
from cube import Cube

ALL_MOVE_NAMES = list(app_module.MOVE_MAP.keys())


@pytest.mark.parametrize("move_name", ALL_MOVE_NAMES)
def test_move_button_produces_expected_face_colors(
    cube_page,
    live_server_url,
    move_name,
):
    expected_faces = app_module.get_face_colors(
        Cube.canonical().apply(app_module.MOVE_MAP[move_name]).state
    )

    with cube_page.expect_response(f"{live_server_url}/api/move") as response_info:
        cube_page.click(f'[data-move="{move_name}"]')

    data = response_info.value.json()

    assert data["success"] is True
    assert data["faces"] == expected_faces


def _apply_algorithm(page, live_server_url, notation):
    page.fill("#algorithm-input", notation)
    with page.expect_response(f"{live_server_url}/api/algorithm") as response_info:
        page.click("#apply-alg-btn")
    return response_info.value.json()


def test_b2_matches_two_b_moves(cube_page, live_server_url):
    b2_data = _apply_algorithm(cube_page, live_server_url, "B2")

    cube_page.request.post(f"{live_server_url}/api/reset")
    bb_data = _apply_algorithm(cube_page, live_server_url, "B B")

    assert b2_data["success"] is True
    assert b2_data["faces"] == bb_data["faces"]


def test_b_b_prime_b_matches_a_single_b(cube_page, live_server_url):
    triple_data = _apply_algorithm(cube_page, live_server_url, "B B' B")

    cube_page.request.post(f"{live_server_url}/api/reset")
    with cube_page.expect_response(f"{live_server_url}/api/move") as response_info:
        cube_page.click('[data-move="B"]')
    single_data = response_info.value.json()

    assert triple_data["success"] is True
    assert triple_data["faces"] == single_data["faces"]


def test_repeated_sexy_move_returns_to_solved(cube_page, live_server_url):
    algorithm = " ".join(["R", "U", "R'", "U'"] * 6)

    data = _apply_algorithm(cube_page, live_server_url, algorithm)

    assert data["success"] is True
    assert data["is_solved"] is True
    assert cube_page.text_content("#solved-status").strip() == "Solved"
