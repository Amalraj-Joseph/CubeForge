# Piece State

## Purpose

This document defines the mutable state of a Piece within a Cube.

A Piece State describes the current location and orientation of a Piece.

While a Piece is immutable, its Piece State changes as moves and cube transformations are applied.

---

# Definition

A Piece State consists of the following components.

- Piece Signature
- Position
- Orientation

The Piece Signature identifies the Piece.

The Position identifies where the Piece currently resides.

The Orientation identifies how the Piece is currently oriented relative to the Logical Faces.

---

# Piece Signature

Every Piece State references exactly one Piece Signature.

The Piece Signature never changes.

Moves and cube transformations shall not modify a Piece Signature.

---

# Position

Every Piece State contains exactly one Position.

The Position indicates the current location of the Piece.

The Position shall always be compatible with the Piece Type.

For example,

- an Edge Piece shall occupy an Edge Position.
- a Corner Piece shall occupy a Corner Position.
- a Center Piece shall occupy a Center Position.

---

# Orientation

Every Piece State contains an Orientation.

Orientation describes how the Piece is currently rotated relative to the Logical Faces.

Orientation is represented as a mapping between the colors of the Piece Signature and the Logical Faces currently exposed by those colors.

For example,

```
Corner

Signature

WHITE
GREEN
RED

Orientation

WHITE -> U
GREEN -> F
RED   -> R
```

The exact representation is implementation-defined provided it completely describes the orientation.

---

# State Equality

Two Piece States are equal if and only if they have identical

- Piece Signatures
- Positions
- Orientations

---

# Effect of Moves

Moves modify the Piece States of affected Pieces.

A move may change

- Position
- Orientation

A move shall never modify

- Piece Signature

---

# Effect of Transformations

Cube Transformations rewrite Piece States according to the new Cube Orientation.

A transformation may change

- Position
- Orientation

A transformation shall never modify

- Piece Signature

The resulting Piece States shall describe the same physical cube from the new frame of reference.

---

# Immutability

The Piece Signature is immutable.

The Position and Orientation are mutable.

Implementations may choose either mutable or immutable data structures for Piece State.

The observable behaviour defined by this specification shall remain unchanged.

---

# Invariants

The following properties shall always hold.

- Every Piece has exactly one Piece State.
- Every Piece State references exactly one Piece Signature.
- Every Piece occupies exactly one compatible Position.
- Every Piece has exactly one Orientation.
- Every Piece Signature appears exactly once within a Cube State.

---

# Description

Every Piece State should provide a human-readable description.

Example

```
Type

Corner

Signature

WHITE
GREEN
RED

Position

DFR

Orientation

WHITE -> F
GREEN -> R
RED   -> D
```

The formatting of the description is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

- represents exactly one Piece State for every Piece
- preserves Piece Signatures
- correctly updates Positions during moves
- correctly updates Orientations during moves
- correctly rewrites Piece States during cube transformations
- maintains all Piece State invariants