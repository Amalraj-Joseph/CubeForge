---
layout: page
title: API Reference
---

# API Reference

Everything here is reachable with `from cube import <name>`. Nothing
outside this list is supported - `cube.internal` is a private
implementation detail with no compatibility guarantee. If you're
building on CubeForge, this page is the contract.

## Construction

| Name | What it does |
|---|---|
| `Cube.canonical()` | The one, unique solved cube. |
| `Cube(state)` | Wrap an existing, valid `CubeState`. Raises `ValueError` on an invalid one. |
| `Cube.from_json(text)` / `.from_dict(data)` / `.from_compact_string(text)` | Deserialize. |

## The move vocabulary

`ALL_MOVES` and all eighteen standard moves as ready-made `Move` instances:
`U`, `U2`, `U_PRIME`, `D`, `D2`, `D_PRIME`, `F`, `F2`, `F_PRIME`, `B`,
`B2`, `B_PRIME`, `L`, `L2`, `L_PRIME`, `R`, `R2`, `R_PRIME`.

## Applying things

| Method | Takes | Returns |
|---|---|---|
| `cube.apply(move)` | a `Move` | a new `Cube` |
| `cube.apply_algorithm(algorithm)` | an `Algorithm` | a new `Cube` |
| `cube.apply_transformation(transformation)` | a `CubeTransformation` | a new `Cube` |

## Algorithms

`Algorithm.parse(notation)` and `Algorithm(*moves)` construct one;
`.notation` formats it back to a string. `.inverse` and `.compose(other)`
give you the reverse and the concatenation. Iterate it (`for move in
algorithm`), index it, or check `len(algorithm)` - it behaves like a
tuple of `Move`.

## Whole-cube transformations

`CubeTransformation` plus the six primitives: `ROTATE_LEFT`, `ROTATE_RIGHT`,
`ROTATE_UP`, `ROTATE_DOWN`, `ROLL_CLOCKWISE`, `ROLL_COUNTERCLOCKWISE`.
Each has `.inverse()` and composes with `.then(other)`.

## Inspecting a cube

| Property / Method | Returns |
|---|---|
| `cube.state` | The underlying `CubeState`. |
| `cube.orientation` | The current `CubeOrientation`. |
| `cube.solved` | `bool` |
| `cube.misplaced_pieces()` / `.misplaced_edges()` / `.misplaced_corners()` | `tuple[PieceState, ...]` |
| `cube.edge_orientation_errors()` / `.corner_orientation_errors()` | `tuple[PieceState, ...]` - correctly placed but mis-oriented |
| `cube.describe()` / `str(cube)` | Human-readable description |

`CubeAnalyzer` and `CubeStatistics` expose the same analysis as static
methods over a raw `CubeState`, for when you don't want the `Cube`
wrapper (`CubeAnalyzer.is_solved(state)`, `CubeStatistics.solved_faces(state)`,
and so on).

## Serialization

`CubeSerializer`, and directly on `Cube`: `to_json()`/`from_json()`,
`to_dict()`/`from_dict()`, `to_compact_string()`/`from_compact_string()`.
Every format embeds an explicit `format_version` and both `up`/`front`
orientation colors, so it survives a future breaking format change and
never assumes canonical orientation.

## Validation

`PieceValidator`, `CubeOrientationValidator`, `CubeStateValidator` - each
has a static `is_valid(x)`. `CubeStateValidator.validate(state)` returns
every detectable violation as a tuple of strings, rather than stopping
at the first one.

## The domain vocabulary

`Color`, `LogicalFace`, `PieceType`, `PositionType`, `Move`, `Piece`,
`PieceSignature`, `PieceState`, `PieceOrientation`, `Position`,
`CubeOrientation` (+ `CANONICAL_ORIENTATION`), `CubeState`,
`CubeTransformation`. Everything the engine's own vocabulary is built
from, importable directly if you need to construct or pattern-match
against it yourself.

## Reference data

`FACE_LAYOUTS` - for each of the six `LogicalFace` values, the nine
`Position`s on that face in raster order (row-major, top-left to
bottom-right). This is what any visualization needs to lay a face out
correctly; the web app's renderer is built entirely from it.

`ScrambleGenerator.generate(length=25)` - a random `Algorithm` with no
two consecutive moves on the same face.

## Versioning

`SPECIFICATION_VERSION` - the version of [the specification](specification.html)
this implementation conforms to.
