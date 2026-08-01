# Cube State

## Purpose

This document defines the complete state of a standard 3×3×3 cube.

A **Cube State** completely describes the observable state of a cube at any instant.

A Cube State consists of the current **Cube Orientation** and the current **Piece State** of every Piece.

---

# Definition

A Cube State is defined as

```
Cube State

=

Cube Orientation

+

Piece States
```

where

- Cube Orientation is defined by the Cube Orientation specification.
- Piece States are defined by the Piece State specification.

Together, these uniquely describe the state of a cube.

---

# Components

A Cube State consists of:

- one Cube Orientation
- exactly twenty-six Piece States

Every Piece shall have exactly one corresponding Piece State.

---

# Completeness

A Cube State is complete if all of the following conditions are satisfied.

- Every Piece has exactly one Piece State.
- Every Position is occupied.
- Every Position is occupied by exactly one compatible Piece.
- Every Piece Signature appears exactly once.
- Cube Orientation is valid.

A complete Cube State uniquely defines a cube.

---

# Canonical Cube State

The **Canonical Cube State** is the unique reference Cube State defined by this specification.

A Cube is in the Canonical Cube State if:

- the Cube Orientation is the Canonical Orientation defined by the Cube Orientation specification.
- every Piece occupies its canonical Position.
- every Piece has its canonical Orientation.

There exists exactly one Canonical Cube State.

The Canonical Cube State serves as the reference state for implementations, testing, serialization, and documentation.

---

# Solved Property

A Cube State has the derived property **Solved**.

A Cube State is considered solved if and only if:

- every Piece occupies its correct Position relative to the Center Pieces, and
- every Piece has its correct Orientation relative to the Center Pieces.

Equivalently, every visible face of the cube consists of a single uniform color.

The Solved property is independent of Cube Orientation.

Consequently, every Cube State obtained from the Canonical Cube State by applying one or more Cube Transformations shall also be considered solved.

There are exactly twenty-four solved Cube States, corresponding to the twenty-four legal Cube Orientations.

The Canonical Cube State is one of these solved Cube States.

The Solved property is derived from the Cube State and shall not be stored as part of the Cube State.

---

# Cube State Equality

Two Cube States are equal if and only if

- their Cube Orientations are equal, and
- every corresponding Piece State is equal.

---

# Effect of Moves

A Move transforms one valid Cube State into another valid Cube State.

Moves

- preserve Cube Orientation.
- preserve Piece Signatures.
- update the affected Piece States.

Moves shall always produce a valid Cube State.

A Move may change the Solved property.

---

# Effect of Cube Transformations

A Cube Transformation transforms one valid Cube State into another valid Cube State.

Cube Transformations

- modify Cube Orientation.
- rewrite Piece States.
- preserve Piece Signatures.

Cube Transformations shall always produce a valid Cube State.

Cube Transformations shall preserve the Solved property.

---

# Validity

A Cube State is valid if it satisfies every invariant defined by this specification.

Implementations may reject invalid Cube States.

Examples of invalid Cube States include

- duplicate Piece Signatures
- duplicate Position occupancy
- incompatible Piece and Position types
- illegal Cube Orientation

Additional mathematical validity rules are defined by the Compliance specification.

---

# Invariants

The following properties shall always hold.

- Every Cube State contains exactly one Cube Orientation.
- Every Piece has exactly one Piece State.
- Every Piece Signature appears exactly once.
- Every Position is occupied exactly once.
- Every Position contains a compatible Piece Type.
- Every Cube State is internally consistent.

---

# Description

Every Cube State should provide a human-readable description.

A description should include

- Cube Orientation
- every Piece State

The formatting of the description is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

- represents exactly one Cube Orientation.
- represents exactly twenty-six Piece States.
- correctly identifies the Canonical Cube State.
- correctly derives the Solved property.
- preserves all Cube State invariants.
- correctly applies Moves.
- correctly applies Cube Transformations.
- produces deterministic Cube States.