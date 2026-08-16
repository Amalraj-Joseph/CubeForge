"""
Independent geometric verification of MOVE_CYCLES direction.

This module builds its own 3D coordinate model of every Position, directly
from LogicalFace semantics (UP=+y, RIGHT=+x, FRONT=+z) and a standard
right-hand-rule rotation matrix - it does not reuse CubeTransformer or any
other part of the move-application pipeline. That independence is the
point: a bug in move_cycles.py (or orientation_rules.py) cannot also be
present here, since this model is derived from first principles.

For each of the six faces, it checks that a SINGLE 90-degree rotation
(one specific direction, either clockwise or counter-clockwise as viewed
from outside that face) simultaneously reproduces both the face's EDGE
cycle and its CORNER cycle as recorded in move_cycles.py. If a face's EDGE
cycle only matches one rotation direction while its CORNER cycle only
matches the other, that face's corners and edges disagree about which way
the layer turns - exactly the bug this test guards against (see
B_CORNER's original definition, which cycled the back-layer corners
backwards relative to B_EDGE).
"""

import math

import pytest

from cube.face.logical_face import LogicalFace
from cube.internal.canonical_positions import ALL_POSITIONS
from cube.internal.move_cycles import MOVE_CYCLES
from cube.position.position_type import PositionType

# ==============================================================================
# Independent coordinate model
# ==============================================================================

AXIS_VECTOR = {
    LogicalFace.UP: (0, 1, 0),
    LogicalFace.DOWN: (0, -1, 0),
    LogicalFace.FRONT: (0, 0, 1),
    LogicalFace.BACK: (0, 0, -1),
    LogicalFace.LEFT: (-1, 0, 0),
    LogicalFace.RIGHT: (1, 0, 0),
}


def _coordinate_of(position):
    x = y = z = 0

    for face in position.faces:
        dx, dy, dz = AXIS_VECTOR[face]
        x += dx
        y += dy
        z += dz

    return (x, y, z)


_COORDINATE_TO_POSITION = {
    _coordinate_of(position): position
    for position in ALL_POSITIONS
}


def _rotation_matrix(axis, degrees):
    """
    Right-hand-rule rotation matrix for `degrees` about `axis`.
    """
    ax, ay, az = axis
    norm = math.sqrt(ax * ax + ay * ay + az * az)
    ax, ay, az = ax / norm, ay / norm, az / norm

    theta = math.radians(degrees)
    c = math.cos(theta)
    s = math.sin(theta)
    t = 1 - c

    return (
        (t * ax * ax + c, t * ax * ay - s * az, t * ax * az + s * ay),
        (t * ax * ay + s * az, t * ay * ay + c, t * ay * az - s * ax),
        (t * ax * az - s * ay, t * ay * az + s * ax, t * az * az + c),
    )


def _apply(matrix, vector):
    x, y, z = vector
    return tuple(
        round(matrix[row][0] * x + matrix[row][1] * y + matrix[row][2] * z)
        for row in range(3)
    )


def _geometric_cycle(face, position_type, degrees):
    """
    Returns the 4 positions of `position_type` touching `face`, rotated by
    `degrees` (right-hand rule) about that face's outward axis, expressed
    in the same convention move_cycles.py uses: index i is the position
    the piece currently at index (i - 1) moves to.
    """
    matrix = _rotation_matrix(AXIS_VECTOR[face], degrees)

    layer_positions = [
        position
        for position in ALL_POSITIONS
        if face in position.faces
        and position.position_type is position_type
    ]

    moves_to = {
        position: _COORDINATE_TO_POSITION[
            _apply(matrix, _coordinate_of(position))
        ]
        for position in layer_positions
    }

    start = layer_positions[0]
    ordered = [start]

    for _ in range(3):
        ordered.append(moves_to[ordered[-1]])

    assert moves_to[ordered[-1]] is start

    return tuple(ordered)


def _is_same_flow(code_positions, geometric_positions):
    """
    True if `code_positions` (a PositionCycle's .positions tuple) encodes
    the same cyclic piece-flow as `geometric_positions`, at any rotation
    offset.
    """
    n = len(geometric_positions)
    doubled = list(geometric_positions) * 2

    return any(
        list(code_positions) == doubled[offset : offset + n]
        for offset in range(n)
    )


def _matching_angles(face, position_type, code_cycle):
    return [
        degrees
        for degrees in (90, -90)
        if _is_same_flow(
            code_cycle.positions,
            _geometric_cycle(face, position_type, degrees),
        )
    ]


# ==============================================================================
# Per-face cycle lookup
# ==============================================================================

_FACES_IN_ORDER = (
    LogicalFace.UP,
    LogicalFace.DOWN,
    LogicalFace.FRONT,
    LogicalFace.BACK,
    LogicalFace.LEFT,
    LogicalFace.RIGHT,
)

_CYCLES_BY_FACE = {
    face: {
        "EDGE": MOVE_CYCLES[index * 2],
        "CORNER": MOVE_CYCLES[index * 2 + 1],
    }
    for index, face in enumerate(_FACES_IN_ORDER)
}


# ==============================================================================
# Direction consistency
# ==============================================================================

@pytest.mark.parametrize("face", _FACES_IN_ORDER, ids=lambda f: f.symbol)
def test_edge_and_corner_cycles_agree_on_rotation_direction(face):
    edge_cycle = _CYCLES_BY_FACE[face]["EDGE"]
    corner_cycle = _CYCLES_BY_FACE[face]["CORNER"]

    edge_angles = set(
        _matching_angles(face, PositionType.EDGE, edge_cycle)
    )
    corner_angles = set(
        _matching_angles(face, PositionType.CORNER, corner_cycle)
    )

    assert edge_angles, (
        f"{face.symbol}_EDGE does not correspond to any 90-degree "
        "rotation of its four positions."
    )
    assert corner_angles, (
        f"{face.symbol}_CORNER does not correspond to any 90-degree "
        "rotation of its four positions."
    )
    assert edge_angles & corner_angles, (
        f"{face.symbol}_EDGE and {face.symbol}_CORNER require opposite "
        "rotation directions - one of them cycles its positions "
        "backwards relative to the other."
    )


def test_every_face_has_exactly_one_matching_rotation_direction():
    """
    Each cycle should match exactly one of +90/-90, not both (a cycle
    that matched both directions would be degenerate/ambiguous).
    """
    for face in _FACES_IN_ORDER:
        for position_type, label in (
            (PositionType.EDGE, "EDGE"),
            (PositionType.CORNER, "CORNER"),
        ):
            cycle = _CYCLES_BY_FACE[face][label]
            angles = _matching_angles(face, position_type, cycle)
            assert len(angles) == 1, (face.symbol, label, angles)
