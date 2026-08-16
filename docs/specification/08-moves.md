---
layout: page
title: Moves · Specification
---

<p><a class="spec-crumb" href="{{ '/specification.html' | relative_url }}">&larr; Specification index</a></p>

# Moves

## Purpose

This document defines the standard Moves of a 3×3×3 cube.

A **Move** is an immutable, deterministic transformation of a Cube State that rotates exactly one layer of the cube while preserving the Cube Orientation.

Moves modify the Piece States of affected Pieces but never modify Piece Signatures or Cube Orientation.

---

# Definition

A Move is an immutable transformation with the following properties.

- Layer
- Rotation
- Notation

Applying a Move transforms one valid Cube State into another valid Cube State.

A Move shall always produce a valid Cube State.

---

# Standard Moves

The specification defines exactly six primary Moves.

```
U
D
F
B
L
R
```

where

| Move | Rotated Layer |
|-------|---------------|
| U | Upper |
| D | Lower |
| F | Front |
| B | Back |
| L | Left |
| R | Right |

The rotated layer is defined relative to the current Cube Orientation.

---

# Move Variants

Each primary Move defines exactly three variants.

## Clockwise Rotation

```
R
```

Rotate the corresponding layer ninety degrees clockwise when viewed directly from that face.

---

## Counter-clockwise Rotation

```
R'
```

Rotate the corresponding layer ninety degrees counter-clockwise when viewed directly from that face.

---

## Double Rotation

```
R2
```

Rotate the corresponding layer one hundred and eighty degrees.

Double Rotations are self-inverse.

---

# Move Notation

The specification adopts the standard Singmaster notation.

The following Moves are defined.

```
U
U'
U2

D
D'
D2

F
F'
F2

B
B'
B2

L
L'
L2

R
R'
R2
```

The notation is case-sensitive.

Implementations shall recognize these symbols.

Support for additional notation systems is outside the scope of this specification.

---

# Move Semantics

Every Move shall

- preserve Cube Orientation.
- preserve Piece Signatures.
- preserve Piece Types.
- preserve Position definitions.
- preserve Cube validity.

A Move may modify

- Piece Positions.
- Piece Orientations.

Only the Piece States of Pieces contained within the rotated layer may change.

All other Piece States shall remain unchanged.

---

# Inverse Moves

Every Move has exactly one inverse.

| Move | Inverse |
|-------|----------|
| U | U' |
| U' | U |
| U2 | U2 |
| D | D' |
| D' | D |
| D2 | D2 |
| F | F' |
| F' | F |
| F2 | F2 |
| B | B' |
| B' | B |
| B2 | B2 |
| L | L' |
| L' | L |
| L2 | L2 |
| R | R' |
| R' | R |
| R2 | R2 |

Applying a Move immediately followed by its inverse shall restore the original Cube State.

---

# Identity

Applying any primary Move four consecutive times shall produce the identity transformation.

Examples

```
R R R R

U U U U

F F F F
```

Likewise,

```
R R'

U U'

F2 F2
```

are identity transformations.

Identity transformations shall not modify the Cube State.

---

# Equality

Two Moves are equal if and only if they represent the same layer rotation.

For example,

```
R == R

R != R'

R != R2
```

---

# Determinism

Moves are deterministic.

Given identical Cube States, the same Move shall always produce identical Cube States.

---

# Description

Every Move should provide a human-readable description.

Example

```
Move

R'

Layer

Right

Rotation

90° Counter-clockwise
```

The formatting is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

- supports all eighteen standard Moves.
- correctly parses Move notation.
- preserves Cube Orientation during Moves.
- correctly updates Piece States.
- correctly applies inverse Moves.
- preserves Cube validity.
- produces deterministic Cube States.

<nav class="spec-pager">
  <a class="spec-pager__prev" href="{{ '/specification/07-cube-state.html' | relative_url }}">&larr; Cube State</a>
  <a class="spec-pager__next" href="{{ '/specification/09-algorithms.html' | relative_url }}">Algorithms &rarr;</a>
</nav>
