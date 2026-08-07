# CubeForge Roadmap (Status Index)

Current Version: v0.10 — Cube Orientation, Analysis, Serialization,
Validation, and Cube Transformations are implemented. Public API exposure
and the compliance audit are not yet finished.

Target Version: v1.0

This document is a status index, not the detailed roadmap. The
authoritative, phase-by-phase plan is `specs/v1.1/plan.md` — read that for
file-level detail on every phase, past and future.

Development behaviour is defined in AGENTS.md.

The specification remains the authoritative source of behaviour.

---

# Status Summary

| Phase | Status |
|---|---|
| v0.7 Cube Orientation Integration | Done |
| v0.8 Core Analysis (`CubeAnalyzer`, `CubeStatistics`) | Logic done in `cube/analysis/`. **Not yet exposed on the `Cube` facade.** |
| v0.9 Serialization (`CubeSerializer`) | Logic done in `cube/serialization/`. **Not yet exposed on the `Cube` facade.** |
| v0.10 Validation (`CubeValidator`) | Done — enforced as `CubeState` constructor invariants, not just post-hoc checks. |
| v1.1 Cube Transformations | Done, ahead of the original schedule. |
| v1.0 Compliance audit + Public API cleanup | In progress. `Cube` facade currently only covers `apply`/`apply_algorithm`/`apply_transformation`/`solved`. `tests/compliance/test_spec_compliance.py` is a single smoke test, not a per-requirement audit. |

---

# Current Phase — v1.0 Finalization

**Goal:** make the work already done in v0.8/v0.9 actually reachable
through the public API, and make "v1.0" mean something verified rather
than assumed.

## Task 1 — Expose Analysis and Serialization on the `Cube` facade

Files to modify: `cube/cube.py`, `cube/__init__.py`

Add to `Cube`:
- `misplaced_pieces()`, `misplaced_edges()`, `misplaced_corners()`
- `edge_orientation_errors()`, `corner_orientation_errors()`
- `to_json()`, `to_dict()`, `to_compact_string()`
- `Cube.from_json(text)`, `Cube.from_dict(data)`,
  `Cube.from_compact_string(text)` as classmethods — construct via
  `CubeSerializer.from_*`, then wrap the result in `Cube(...)`

`.solved` already exists on `Cube`/`CubeState`. Decide whether it should
keep its own implementation or delegate to `CubeAnalyzer.is_solved`
internally so there is exactly one definition of "solved" — don't leave
two independent implementations that could drift apart.

Export `CubeAnalyzer`, `CubeStatistics`, `CubeSerializer` from
`cube/__init__.py` alongside `Cube` and `CubeState`.

## Task 2 — Expand the compliance audit

File: `tests/compliance/test_spec_compliance.py`

Currently a single smoke test. Rewrite as one test function per mandatory
bullet in `specs/v1/11-api.md` and `specs/v1/12-compliance.md` —
construction, inspection, move application, algorithm application,
transformation application, equality, validation, description. Every
capability listed there needs its own assertion against the real public
API, not just `Cube.canonical().apply(R).solved`.

## Task 3 — Resolve the center-piece / orientation consistency question

Open question found during v0.8 review: nothing currently enforces that
a center piece's `PieceState.position` agrees with `CubeState.orientation`.
Example: `orientation.up == WHITE` while the WHITE center's `PieceState`
is assigned to a different position is not rejected by
`CubeStateValidator` or `CubeState.__init__` today.

Decide one of:

- **(a)** `CubeOrientation` is independent of center-piece placement by
  design (an observer's frame of reference). If so, document this
  explicitly in `specs/v1/07-cube-state.md` so it isn't ambiguous for a
  future language port.
- **(b)** `CubeOrientation` must always agree with center-piece placement
  (matches a real physical cube, where centers never permute relative to
  each other). If so, add a check — either to `CubeStateValidator` or as
  a `CubeState` constructor invariant, consistent with how parity is
  already enforced — and add a corresponding bullet to
  `specs/v1/07-cube-state.md` or `specs/v1/14-validity-and-parity.md`.

Do not silently pick one without updating the spec. This is exactly the
kind of gap `specs/v1/conformance-tests.md` is meant to catch across
language ports.

## Task 4 — Spec hygiene

- Archive `specs/v0/INITIAL_DRAFT.md` — add a clear "SUPERSEDED, see
  specs/v1/" note at the top, or delete it if it isn't needed for
  history.
- Fold `specs/architecture/color.md` into `specs/v1/` (e.g. as part of
  `01-colors.md`) or mark it explicitly non-normative at the top of the
  file.

## Definition of Done

- `Cube` exposes analysis and serialization directly; no caller needs to
  import `cube.analysis` or `cube.serialization` to use them.
- `tests/compliance/test_spec_compliance.py` has one test per mandatory
  requirement in `11-api.md`/`12-compliance.md`.
- The center/orientation question has an explicit answer, reflected in
  both the spec and (if applicable) `CubeStateValidator`.
- `specs/v0/INITIAL_DRAFT.md` and `specs/architecture/color.md` no longer
  read as ambiguous or current.
- Full test suite passes.
- Tag `v1.0.0`.

---

# Philosophy

CubeForge should remain a pure mathematical engine. It should never depend
on Flask, HTML, JavaScript, Three.js, OpenGL, Pygame, MCP, WebSockets, or
databases. Those technologies should depend on CubeForge, not the reverse.

---

For every phase beyond this one (v1.2 Algorithm Utilities onward), see
`specs/v1.1/plan.md`.