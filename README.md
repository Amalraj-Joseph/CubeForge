# CubeForge

**A language-agnostic, specification-driven Rubik's Cube engine.**

CubeForge answers one question the same way no matter what implements
it: given a cube state and an operation, what's the resulting state?
That question is answered once, formally, in [the specification](specs/)
— not baked into any one implementation's internals. The Python engine
in this repository is the reference implementation; a web app and a set
of example scripts build on top of it through its public API alone.

Every invariant a physical cube actually has — exactly twenty-six
pieces, valid orientation and permutation parity, opposite colors never
sharing a piece — is enforced at construction time. An illegal
`CubeState` cannot be built; it isn't checked for and rejected after
the fact, it's structurally impossible to represent.

📖 **[Full documentation](https://shadow-codex.github.io/CubeForge/)** ·
📋 **[Specification](specs/)** · 📜 **[License](LICENSE)** (Apache 2.0)

---

## Repository layout

```
CubeForge/
  core/       The engine. Pure Python, zero external dependencies.
  web/        Flask REST API + Three.js browser UI, consuming core/.
  docs/       This project's documentation site (GitHub Pages).
  specs/      The formal specification. The source of truth.
  examples/   Small standalone scripts: inspect, render, play.
```

Each subproject has its own README with more detail:
[`core/`](core) · [`web/`](web/README.md) · [`docs/`](docs/README.md)

## Quick start

```bash
cd core
pip install -e .
```

```python
from cube import Cube, Algorithm, R

# The one, unique solved state every implementation agrees on.
cube = Cube.canonical()
cube.solved   # True

# Apply a move.
cube = cube.apply(R)
cube.solved   # False

# Apply an algorithm, in standard Singmaster notation.
cube = Cube.canonical().apply_algorithm(Algorithm.parse("R U R' U'"))

# Inspect it.
cube.misplaced_pieces()
cube.edge_orientation_errors()

# Serialize it.
text = cube.to_json()
assert Cube.from_json(text) == cube
```

See [Getting Started](https://shadow-codex.github.io/CubeForge/getting-started.html)
for the full walkthrough, or [Architecture](https://shadow-codex.github.io/CubeForge/architecture.html)
for the domain model behind it.

## Try the web app

```bash
cd web
pip install -r requirements.txt
python3 app.py
```

Then open <http://localhost:5000> for an interactive 3D cube, backed by
the same engine, talking to it purely through the public API.

## Philosophy

The engine stays a pure mathematical model. It never depends on Flask,
HTML, JavaScript, Three.js, OpenGL, Pygame, MCP, WebSockets, or a
database — those technologies depend on it, never the reverse. `core/`
declares zero dependencies on purpose.

Everything downstream — a solver, a web app, a CLI, an MCP server, a
port to another language — either consumes `core/`'s public API
directly, or conforms independently to [the specification](specs/) it's
built from. Two conforming implementations, in any language, are
expected to produce identical observable behavior for identical
operations.

## Testing

```bash
cd core
pip install -e .[dev]
pytest              # 800+ tests, including a per-requirement compliance
                     # audit against every mandatory bullet in specs/v1/
ruff check .         # lint
pytest --cov=cube --cov-report=term-missing   # coverage
```

## Compliance

This implementation conforms to the 3×3 Cube Specification, Version 1.0
(`specs/v1/`). `core/tests/compliance/test_spec_compliance.py` is that
claim made executable: one test per mandatory requirement in
`specs/v1/11-api.md` and `specs/v1/12-compliance.md`, run against the
real public API — the permanent regression gate for this
implementation and any future port.

## Companion projects

| Project | Status |
|---|---|
| [`web/`](web/README.md) — Flask + REST + Three.js | Done |
| CLI game (`examples/03_cli_game.py`) | Done, as an example |
| Solver (beginner / CFOP / Kociemba) | Planned — see `specs/v1.1/plan.md` |
| MCP server | Planned |
| Java / Rust / C# ports | Planned, after `core/` reaches a stable v1.0 tag |

## License

[Apache License 2.0](LICENSE).
