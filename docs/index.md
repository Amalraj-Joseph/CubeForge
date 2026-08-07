---
layout: page
title: Home
---

# CubeForge

CubeForge is a language-agnostic, specification-driven model of a
standard 3x3x3 Rubik's Cube. It exists to answer one question the same
way, no matter what implements it: **given a cube state and an
operation, what is the resulting state?**

That question is answered once, formally, in [the specification](specification.html)
- not in any one implementation. The Python engine in this repository
(`core/`) is the reference implementation. Anything else - a solver, a
web app, a CLI, another language port - builds on top of it, or
conforms to the same specification independently.

## Why this exists

Most Rubik's Cube libraries bake their model into whatever they're used
for: a solver ties piece representation to its search algorithm, a
visualizer ties it to its rendering pipeline. CubeForge inverts that.
The engine is a pure mathematical model - colors, pieces, positions,
orientation, moves, algorithms, whole-cube transformations - with
**zero dependency** on any UI, network, or storage technology. Every
invariant a real cube has (parity, orientation legality, exactly
twenty-six pieces) is enforced at construction time, not checked
after the fact.

## What's in this repository

| Subproject | What it is |
|---|---|
| [`core/`]({{ site.github_repo }}/tree/main/core) | The engine itself: an immutable Python library with zero external dependencies. |
| [`web/`](web-app.html) | A Flask REST API + Three.js browser UI, consuming `core/` through its public API. |
| [`specs/`](specification.html) | The formal, language-agnostic specification. The source of truth. |
| [`examples/`]({{ site.github_repo }}/tree/main/examples) | Small standalone scripts: inspect a cube, render one to the terminal, play an interactive CLI game. |
| `docs/` | This site. |

## Start here

- New to the engine? [Getting Started](getting-started.html)
- Want the mental model before the API? [Architecture](architecture.html)
- Know what you're looking for? [API Reference](api-reference.html)
- Want the formal, implementation-independent rules? [Specification](specification.html)
