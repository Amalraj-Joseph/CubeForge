---
layout: page
title: Getting Started
---

# Getting Started

## Install

CubeForge's engine (`core/`) has zero external dependencies - it's pure
Python, 3.11+.

```bash
git clone https://github.com/Amalraj-Joseph/CubeForge.git
cd CubeForge/core
pip install -e .
```

That makes `cube` importable from anywhere in your environment.

## Your first cube

```python
from cube import Cube

cube = Cube.canonical()
print(cube.solved)   # True
```

`Cube.canonical()` is the one, unique solved state every implementation
of the specification agrees on.

{% include cube-diagram.html
   up="w,w,w,w,w,w,w,w,w"
   front="g,g,g,g,g,g,g,g,g"
   right="r,r,r,r,r,r,r,r,r"
   px="180" static="true"
   caption="Cube.canonical()" %}

## Applying a move

```python
from cube import Cube, R

cube = Cube.canonical().apply(R)
print(cube.solved)   # False
```

`R`, along with all seventeen other standard moves (`U`, `D`, `F`, `B`,
`L`, and their `2`/`'` variants), is importable directly from `cube`.
`R` rotates the entire right layer a quarter turn - only pieces in that
layer change; everything else on the cube is untouched:

<div class="cube-pair">
{% include cube-diagram.html
   up="w,w,w,w,w,w,w,w,w"
   front="g,g,g,g,g,g,g,g,g"
   right="r,r,r,r,r,r,r,r,r"
   px="160" static="true"
   caption="Before: Cube.canonical()" %}
{% include cube-diagram.html
   up="w,w,g,w,w,g,w,w,g"
   front="g,g,y,g,g,y,g,g,y"
   right="r,r,r,r,r,r,r,r,r"
   px="160" static="true"
   caption="After: .apply(R)" %}
</div>

## Applying an algorithm

```python
from cube import Cube, Algorithm

algorithm = Algorithm.parse("R U R' U'")
cube = Cube.canonical().apply_algorithm(algorithm)
```

`Algorithm.parse` accepts standard Singmaster notation. `algorithm.notation`
converts back the other way.

## Inspecting a cube

```python
cube = Cube.canonical().apply(R)

cube.solved                        # False
cube.misplaced_pieces()            # every PieceState in the wrong Position
cube.edge_orientation_errors()     # correctly placed but flipped edges
cube.corner_orientation_errors()   # correctly placed but twisted corners
```

## Whole-cube rotations

Moves turn a layer. Transformations turn the *entire* cube - they change
which center faces which direction, without moving any piece relative to
any other.

```python
from cube import Cube, ROTATE_UP

cube = Cube.canonical().apply_transformation(ROTATE_UP)
print(cube.orientation.top)   # no longer WHITE
print(cube.solved)            # still True - transformations preserve solved
```

## Serialization

```python
cube = Cube.canonical()

text = cube.to_json()
restored = Cube.from_json(text)
assert restored == cube
```

`to_dict()`/`from_dict()` and `to_compact_string()`/`from_compact_string()`
work the same way, for when JSON is more or less convenient than a plain
object or a short wire format.

## Validation

```python
from cube import CubeStateValidator

CubeStateValidator.is_valid(cube.state)   # True
```

Every `Cube`/`CubeState` you can actually construct is already valid -
the constructor rejects anything else (duplicate pieces, broken parity,
illegal orientation, and so on) before it exists. `CubeStateValidator`
exists mainly as a standalone capability for validating data that arrived
from *outside* the engine - e.g. before deserializing something untrusted.

## Running the tests

```bash
cd core
pip install -e .[dev]
pytest
```

## Next

- [Architecture](architecture.html) for the full domain model
- [API Reference](api-reference.html) for everything reachable from `cube`
- [Web App](web-app.html) to run the interactive 3D cube in a browser
