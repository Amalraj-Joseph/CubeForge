# CubeCore Roadmap v2 — Spec-Compliance Refined

**Current Version:** v0.6.0-cli-game
**Target of this document:** v1.0 stable core

## How to use this document with Claude Code

Work phase by phase, in order. Do not start a phase until the previous one's
"Definition of Done" is fully green. After each phase: run the full test
suite, then re-read the relevant `specs/v1/*.md` file and confirm every
"Compliance" bullet in it is satisfied before moving on. Commit at the end
of each phase.

---

## Why this reorders the original roadmap

The original roadmap put Cube Orientation integration at v1.0 (after
Analysis, Serialization, Validation). But `CubeState` currently has **no
orientation field at all** — `cube/cube_state.py` only holds `_by_piece` /
`_by_position`. Spec `07-cube-state.md` defines `CubeState = CubeOrientation
+ PieceStates` as mandatory, and `12-compliance.md` lists "represent all
twenty-four legal Cube Orientations" as a mandatory requirement — not
optional, not deferred.

Building Analysis, Serialization, and Validation against the current
orientation-less `CubeState` means all three get rebuilt once orientation
lands. So orientation moves first.

---

## v0.7 — Cube Orientation Integration

**Goal:** `CubeState` becomes spec-compliant per `07-cube-state.md` and
`04-orientation.md`. This unblocks everything after it.

### Files to modify

- `cube/color/color.py`
  - Add `OPPOSITE_COLORS: dict[Color, Color]` and a `Color.opposite`
    property. This is the single source of truth for "White/Yellow,
    Green/Blue, Red/Orange are opposite pairs" — extract it if it's
    already implicit in `cube/internal/canonical_face_layouts.py`, don't
    duplicate it.

- `cube/orientation/cube_orientation.py`
  - `__post_init__` currently only checks the 6 colors are distinct. Add
    legality enforcement per `04-orientation.md` "Legal Orientations":
    - `up` and `front` must be adjacent (not `Color.opposite` of each
      other).
    - `down == up.opposite`, `back == front.opposite`.
    - `left`/`right` must be derivable and consistent (there is exactly
      one legal completion given `up`/`front` — derive `left`/`right`
      rather than accepting them as free parameters, or validate them
      against the derived value and raise `ValueError` on mismatch).
  - Add `CANONICAL_ORIENTATION` as a module-level constant here (matches
    spec's canonical table: `TOP=WHITE, FRONT=GREEN, ...`).

- `cube/cube_state.py`
  - Add `orientation: CubeOrientation` as a required field of `CubeState`,
    stored via `object.__setattr__` in `__init__` like the existing
    fields. Default parameter should NOT silently default to canonical —
    require it explicitly at the call site so every construction site is
    forced to be updated and reviewed.
  - Update `__eq__`/`__hash__` (currently implicit via `@dataclass`) to
    include `orientation`, per `07-cube-state.md` "Cube State Equality."
  - Update `__repr__`/description output to include orientation.

- `cube/internal/canonical_cube_state.py`
  - `CANONICAL_CUBE_STATE` construction must pass `CANONICAL_ORIENTATION`.

- `cube/cube_transformer.py`
  - `CubeTransformer.apply` / `apply_algorithm`: orientation must pass
    through unchanged (Moves preserve Cube Orientation per
    `08-moves.md`). Add an explicit assertion or test, don't just rely on
    it happening implicitly via the new required field.

- Anywhere else that constructs a `CubeState` directly (ASCII renderer,
  scramble generator, CLI game, tests) — audit and update call sites.
  Grep for `CubeState(` across the repo before starting; there will be
  several call sites that break on the signature change, and that's
  expected — this is the point of the phase.

### Files to add

- `tests/orientation/test_cube_orientation_legality.py`
  - All 24 legal (top, front) pairs construct without error (test data
    already exists in `test_cube_orientation.py` — reuse it).
  - At least one illegal case per rule: opposite colors on
    top/front (e.g. `WHITE`/`YELLOW`), and a case with a
    non-adjacent-but-not-opposite mismatch if your color-adjacency
    graph allows distinguishing it.

- `tests/test_cube_state_orientation.py`
  - Two `CubeState`s with identical piece states but different
    orientation are NOT equal.
  - `CubeTransformer.apply` (any move) preserves `cube.orientation`
    exactly.

### Definition of Done

- `CANONICAL_CUBE_STATE.orientation == CANONICAL_ORIENTATION`.
- Illegal `CubeOrientation` construction raises `ValueError`.
- All 24 legal orientations are constructible.
- Full existing suite (560+ tests) still green after signature-change
  cascade is fixed.
- Re-read `04-orientation.md` and `07-cube-state.md` "Compliance"
  sections — every bullet should now be true of the implementation.

---

## v0.8 — Core Analysis

**Goal:** Add analysis capabilities that are correct for *any* of the 24
legal orientations, not just canonical — this is the actual payoff of
doing v0.7 first.

### Files to add

- `cube/analysis/cube_analyzer.py` — `CubeAnalyzer` with:
  - `is_solved(cube: CubeState) -> bool`
  - `misplaced_pieces(cube: CubeState) -> list[Piece]`
  - `misplaced_edges(cube: CubeState) -> list[Piece]`
  - `misplaced_corners(cube: CubeState) -> list[Piece]`
  - `edge_orientation_errors(cube: CubeState) -> list[Piece]`
  - `corner_orientation_errors(cube: CubeState) -> list[Piece]`

  **Critical implementation detail:** derive "correct" position/orientation
  for a piece from `cube.orientation` (i.e. from the current mapping of
  Logical Faces to center colors), never from hardcoded canonical color
  constants. This is what makes `is_solved` orientation-independent per
  `07-cube-state.md` ("there are exactly twenty-four solved Cube
  States").

- `cube/analysis/cube_statistics.py` — `CubeStatistics` with:
  - `move_count(algorithm: Algorithm) -> int`
  - `solved_faces(cube: CubeState) -> int`
  - `solved_edges(cube: CubeState) -> int`
  - `solved_corners(cube: CubeState) -> int`

### Files to add (tests)

- `tests/analysis/test_cube_analyzer.py`
  - **The key regression test for v0.7's investment:** take
    `CANONICAL_CUBE_STATE`, construct the *same* solved arrangement
    expressed under each of the other 23 legal orientations (via
    `CubeRotator` once it exists in v1.1, or by direct construction for
    now), and assert `is_solved()` returns `True` for all 24.
  - Misplaced/orientation-error detection against known scrambles
    (reuse existing scramble fixtures from `scramble/scramble_generator.py`
    tests).

### Definition of Done

- `is_solved()` is orientation-independent (test above passes for all 24).
- Every method has direct unit tests plus at least one integration test
  against a real scramble.

---

## v0.9 — Serialization

**Goal:** Transport `CubeState` (orientation + all 26 piece states)
without a breaking format change later.

### Files to add

- `cube/serialization/cube_serializer.py` — `CubeSerializer` with:
  - `to_json(cube: CubeState) -> str`
  - `from_json(data: str) -> CubeState`
  - `to_dict(cube: CubeState) -> dict`
  - `from_dict(data: dict) -> CubeState`
  - `to_compact_string(cube: CubeState) -> str`
  - `from_compact_string(s: str) -> CubeState`

  **Schema requirements (non-negotiable, avoid a v1.x breaking change):**
  - Every format must include an explicit `"format_version"` field from
    day one, even at `"1"`. This is what the roadmap already calls out
    as a design principle ("Serialization friendly") — a version field
    is what makes that true in practice, not just in intent.
  - Every format must serialize orientation explicitly (both `up` and
    `front` colors is sufficient per `04-orientation.md`, since the rest
    is derived) — do not assume canonical.

### Files to add (tests)

- `tests/serialization/test_cube_serializer.py`
  - Round-trip: `from_json(to_json(cube)) == cube` for canonical state,
    a scrambled state, and a state in a non-canonical orientation.
  - Same for dict and compact-string formats.
  - Malformed input raises a clear, typed exception (not a bare
    `KeyError`/`json.JSONDecodeError` leaking from internals).

### Definition of Done

- Round-trip equality holds (including orientation) for all three formats.
- `format_version` present and checked on deserialization.

---

## v0.10 — Validation

**Goal:** Reject mathematically impossible cubes — including the check
your spec currently omits.

### Spec addendum to author first

Add `specs/v1/14-validity-and-parity.md` (or extend `07-cube-state.md`'s
"Validity" section) documenting:
- Permutation parity: the permutation of pieces relative to canonical
  must be even.
- Corner orientation parity: sum of corner twists mod 3 must be 0.
- Edge orientation parity: sum of edge flips mod 2 must be 0.

This closes the gap flagged in review — right now two spec-compliant
implementations could disagree on whether a structurally-valid-but-
physically-impossible `CubeState` is legal, which undermines the spec's
own cross-implementation-consistency goal.

### Files to add

- `cube/validation/cube_validator.py` — `CubeValidator` with:
  - `is_valid(cube: CubeState) -> bool`
  - `validate(cube: CubeState) -> list[ValidationError]` (report *all*
    violations, not just the first — useful for API error responses
    later)
  - Checks: duplicate piece signatures, duplicate position occupancy,
    incompatible piece/position types, illegal `CubeOrientation` (reuse
    v0.7's legality logic — do not reimplement it here), permutation
    parity, corner orientation parity, edge orientation parity.

### Files to add (tests)

- `tests/validation/test_cube_validator.py`
  - `CANONICAL_CUBE_STATE` and any state reachable via
    `CubeTransformer.apply_algorithm` are valid.
  - Two edges swapped (odd permutation) → invalid, parity check fires.
  - Single corner twisted → invalid, corner-orientation check fires.
  - Single edge flipped → invalid, edge-orientation check fires.
  - Duplicate signature / duplicate position / illegal orientation cases.

### Definition of Done

- All parity classes have a dedicated failing-case test.
- `specs/v1/14-validity-and-parity.md` exists and `12-compliance.md`
  references it.

---

## v1.0 — Compliance Audit + Public API Cleanup

**Goal:** v1.0 means something concrete: every mandatory bullet in
`11-api.md` and `12-compliance.md` is verified, not assumed.

### Files to add

- `tests/compliance/test_spec_compliance.py` — one test (or test class)
  per mandatory bullet in `11-api.md` ("Cube Construction," "Cube
  Inspection," "Move Capabilities," "Algorithm Capabilities," "Cube
  Transformation Capabilities," "Equality," "Validation," "Description")
  and `12-compliance.md` ("Mandatory Requirements," "Behavioural
  Requirements," "Invariant Preservation"). This becomes your permanent
  regression gate for every future language port.

### Public API cleanup (pulled forward from original v1.7)

- Reduce `cube.internal.*` exposure. Public surface should read like:
  `CubeState.solved()`, `Move.R`, `Algorithm.parse(...)`,
  `Algorithm.format(...)`.
- Package exposes `SPEC_VERSION = "1.0"` for the compliance statement
  described in `12-compliance.md`.

### Definition of Done

- `test_spec_compliance.py` fully green.
- Tag `v1.0.0`. Compliance statement in README:
  `This implementation conforms to The 3×3 Cube Specification Version 1.0.`

---

## v1.1 — Cube Transformations

**Goal:** Support rotating the entire cube. Because orientation is
already integrated (v0.7), this phase is purely additive — no `CubeState`
shape changes required here, unlike in the original ordering.

- `cube/transformation/cube_rotator.py` — `CubeRotator` with the six
  primitives from `10-transformations.md`: Rotate Left/Right/Up/Down,
  Roll Clockwise/Counter-clockwise.
- Update ASCII renderer to read `cube.orientation` when mapping logical
  faces to displayed colors (audit now — it likely still assumes
  canonical implicitly).
- Tests: each primitive × its inverse restores original state; the 24
  reachable orientations from canonical via composition; identity
  transformations (Left then Right, etc.) are true no-ops on the full
  `CubeState`.

---

## v1.2 — Algorithm Utilities
`inverse()`, `reverse()`, `simplify()`, `repeat()`, `concatenate()`,
`split()`, `length` — unchanged from original roadmap.

## v1.3 — Rich Analysis
Cross / F2L / OLL / PLL / solved-layer detection — unchanged.

## v1.4 — Solver Framework
`Solver`, `Solution`, `AbstractSolver`, `BeginnerSolver`, `CFOPSolver`,
`KociembaSolver` — unchanged. Do not implement solving logic inside
`CubeTransformer`.

## v1.5 — Events
Optional `MoveResult` (before/after/move/affected pieces/changed
stickers) — unchanged.

## v1.6 — Performance
Cached lookups, frozen arrays, optional fast transformer, benchmark
suite — unchanged.

---

## Companion Projects (unchanged, for reference)

- **CubeCore Web** — Flask + REST + Three.js, depends on v0.8/v0.9.
- **CubeCore CLI** — depends on v1.1 for whole-cube rotation input.
- **CubeCore MCP** — tool mapping is now direct:
  `validate_cube` → v0.10, `analyze_cube` → v0.8, `solve_cube` → v1.4,
  `apply_algorithm`/`generate_scramble` → existing core.
- **CubeCore Java / Rust / C#** — should not begin until v1.0 tag exists;
  porting against a moving core wastes the port effort.

## Philosophy (unchanged)

CubeCore remains a pure mathematical engine with zero dependency on
Flask, HTML, JavaScript, Three.js, OpenGL, Pygame, MCP, WebSockets, or
databases. Those depend on CubeCore, never the reverse.