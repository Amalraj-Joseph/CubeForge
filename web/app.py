"""
CubeForge Web - a Flask REST API + browser UI for an interactive,
CubeForge-backed Rubik's Cube.

This is a companion project, not part of the core engine: it consumes
CubeForge purely through its public API (see ../core/cube/__init__.py) and
carries its own dependencies (Flask, Flask-CORS) that the engine itself
never depends on.
"""

import logging
import traceback

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from cube import (
    Algorithm,
    B, B2, B_PRIME,
    Cube,
    D, D2, D_PRIME,
    F, F2, F_PRIME,
    FACE_LAYOUTS,
    L, L2, L_PRIME,
    LogicalFace,
    Move,
    R, R2, R_PRIME,
    ScrambleGenerator,
    U, U2, U_PRIME,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

MOVE_MAP = {
    'U': U, 'U2': U2, "U'": U_PRIME,
    'D': D, 'D2': D2, "D'": D_PRIME,
    'R': R, 'R2': R2, "R'": R_PRIME,
    'L': L, 'L2': L2, "L'": L_PRIME,
    'F': F, 'F2': F2, "F'": F_PRIME,
    'B': B, 'B2': B2, "B'": B_PRIME,
}

COLOR_MAP = {
    'WHITE': '#FFFFFF',
    'YELLOW': '#FFFF00',
    'GREEN': '#00FF00',
    'BLUE': '#0000FF',
    'RED': '#FF0000',
    'ORANGE': '#FF8C00',
}

# Global state - a single shared cube for this demo server. A real
# multi-user deployment would key this by session/room instead.
current_cube = Cube.canonical()
move_history: list[Move] = []


def get_face_colors(cube_state):
    """
    Extract colors for each face of the cube.

    Returns a dict with 3x3 grids for each face (U, D, F, B, L, R). Each
    cell contains a hex color string like '#FFFFFF'.

    Built directly from CubeForge's own FACE_LAYOUTS: for each face, that's
    the 9 Positions on it in raster order (row-major, top-left to
    bottom-right), so every cell is filled from a single, already-correct
    source of truth rather than a hand-maintained lookup table.
    """
    face_colors = {}

    for face in LogicalFace:
        grid = [[None, None, None] for _ in range(3)]

        for index, position in enumerate(FACE_LAYOUTS[face]):
            row, col = divmod(index, 3)
            piece_state = cube_state.piece_at(position)
            color = piece_state.color_on(face)
            grid[row][col] = COLOR_MAP.get(color.name, '#888888')

        face_colors[face.symbol] = grid

    return face_colors


def check_solved(cube_state):
    """Delegates to CubeState.solved - the library's own, correct answer."""
    return cube_state.solved


def cube_response(**extra):
    return jsonify({
        'success': True,
        'faces': get_face_colors(current_cube.state),
        'move_count': len(move_history),
        'move_history': ' '.join(m.notation for m in move_history),
        'is_solved': check_solved(current_cube.state),
        **extra,
    })


def error_response(message, status):
    return jsonify({'success': False, 'error': message}), status


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def get_state():
    try:
        return cube_response()
    except Exception as e:
        logger.error("Error: %s\n%s", e, traceback.format_exc())
        return error_response(str(e), 500)


@app.route('/api/move', methods=['POST'])
def apply_move():
    global current_cube

    try:
        data = request.get_json()
        move_name = data.get('move')

        if move_name not in MOVE_MAP:
            return error_response(f'Unknown move: {move_name}', 400)

        move = MOVE_MAP[move_name]
        current_cube = current_cube.apply(move)
        move_history.append(move)

        return cube_response()
    except Exception as e:
        logger.error("Error: %s\n%s", e, traceback.format_exc())
        return error_response(str(e), 500)


@app.route('/api/algorithm', methods=['POST'])
def apply_algorithm():
    global current_cube

    try:
        data = request.get_json()
        notation = data.get('notation', '')

        if not notation:
            return error_response('Empty algorithm', 400)

        try:
            algorithm = Algorithm.parse(notation)
        except ValueError as ex:
            return error_response(str(ex), 400)

        current_cube = current_cube.apply_algorithm(algorithm)
        move_history.extend(algorithm)

        return cube_response()
    except Exception as e:
        logger.error("Error: %s\n%s", e, traceback.format_exc())
        return error_response(str(e), 500)


@app.route('/api/scramble', methods=['POST'])
def apply_scramble():
    global current_cube

    try:
        data = request.get_json() or {}
        length = data.get('length', 20)

        scramble = ScrambleGenerator.generate(length)
        current_cube = current_cube.apply_algorithm(scramble)
        move_history.extend(scramble)

        return cube_response(scramble=scramble.notation)
    except Exception as e:
        logger.error("Error: %s\n%s", e, traceback.format_exc())
        return error_response(str(e), 500)


@app.route('/api/reset', methods=['POST'])
def reset_cube():
    global current_cube

    try:
        current_cube = Cube.canonical()
        move_history.clear()

        return cube_response()
    except Exception as e:
        logger.error("Error: %s\n%s", e, traceback.format_exc())
        return error_response(str(e), 500)


@app.route('/api/undo', methods=['POST'])
def undo_move():
    global current_cube

    try:
        if not move_history:
            return error_response('No moves to undo', 400)

        last_move = move_history.pop()
        current_cube = current_cube.apply(last_move.inverse)

        return cube_response()
    except Exception as e:
        logger.error("Error: %s\n%s", e, traceback.format_exc())
        return error_response(str(e), 500)


if __name__ == '__main__':
    print(
        "CubeForge Web\n"
        "=============\n\n"
        "Starting server at http://localhost:5000\n\n"
        "Controls: click face buttons or use the keyboard - U D F B L R\n"
        "(shift for inverse), Space to scramble, Z to undo, Shift+Z to reset.\n\n"
        "Press Ctrl+C to quit."
    )
    app.run(debug=True, host='0.0.0.0', port=5000)
