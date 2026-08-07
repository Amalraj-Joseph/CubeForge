"""
Guards the public API contract described in cube/__init__.py's docstring:
every capability a companion project (solver, web app, CLI, MCP server)
needs shall be reachable via `from cube import ...` alone, with nothing
imported from `cube.internal` or any deep submodule path.
"""

import cube

PUBLIC_NAMES = (
    "ALL_MOVES",
    "Algorithm",
    "B", "B2", "B_PRIME",
    "CANONICAL_ORIENTATION",
    "Color",
    "Cube",
    "CubeAnalyzer",
    "CubeOrientation",
    "CubeOrientationValidator",
    "CubeSerializer",
    "CubeState",
    "CubeStateValidator",
    "CubeStatistics",
    "CubeTransformation",
    "D", "D2", "D_PRIME",
    "F", "F2", "F_PRIME",
    "FACE_LAYOUTS",
    "L", "L2", "L_PRIME",
    "LogicalFace",
    "Move",
    "Piece",
    "PieceOrientation",
    "PieceSignature",
    "PieceState",
    "PieceType",
    "PieceValidator",
    "Position",
    "PositionType",
    "R", "R2", "R_PRIME",
    "ROLL_CLOCKWISE",
    "ROLL_COUNTERCLOCKWISE",
    "ROTATE_DOWN",
    "ROTATE_LEFT",
    "ROTATE_RIGHT",
    "ROTATE_UP",
    "SPECIFICATION_VERSION",
    "ScrambleGenerator",
    "U", "U2", "U_PRIME",
)


def test_all_declares_every_public_name():
    assert set(cube.__all__) == set(PUBLIC_NAMES)


def test_every_declared_name_is_actually_importable():
    for name in cube.__all__:
        assert hasattr(cube, name), f"cube.{name} is declared but missing"


def test_all_eighteen_canonical_moves_are_exported():
    assert len(cube.ALL_MOVES) == 18
    assert all(isinstance(move, cube.Move) for move in cube.ALL_MOVES)


def test_face_layouts_gives_nine_positions_per_face_in_raster_order():
    assert set(cube.FACE_LAYOUTS) == set(cube.LogicalFace)

    for face, positions in cube.FACE_LAYOUTS.items():
        assert len(positions) == 9
        assert all(position.contains(face) for position in positions)


def test_a_sibling_project_can_work_through_the_public_api_alone():
    """
    Simulates what a solver/web/CLI/MCP author would write: build, apply,
    inspect, validate, and serialize a Cube using only `cube.*` names.
    """
    algorithm = cube.Algorithm.parse("R U R' U'")
    scramble = cube.ScrambleGenerator.generate(length=15)

    solved = cube.Cube.canonical()
    scrambled = solved.apply_algorithm(algorithm).apply_algorithm(scramble)

    assert not scrambled.solved
    assert cube.CubeStateValidator.is_valid(scrambled.state)
    assert isinstance(cube.CubeAnalyzer.misplaced_pieces(scrambled.state), tuple)

    rotated = scrambled.apply_transformation(cube.ROTATE_UP)
    assert cube.CubeOrientationValidator.is_valid(rotated.orientation)

    restored_text = rotated.to_json()
    restored = cube.Cube.from_json(restored_text)
    assert restored == rotated

    piece_state = restored.state.piece_at(
        next(iter(restored.state)).position
    )
    assert isinstance(piece_state, cube.PieceState)
    assert isinstance(piece_state.piece, cube.Piece)
    assert isinstance(piece_state.piece.signature, cube.PieceSignature)
    assert isinstance(piece_state.orientation, cube.PieceOrientation)
