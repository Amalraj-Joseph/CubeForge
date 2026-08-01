# Positions

## Purpose

This document defines the positions that exist within a standard 3×3×3 cube.

A **Position** is a logical placeholder within the cube that may be occupied by exactly one compatible Piece.

Positions are immutable and are defined relative to the **Logical Faces** of the cube.

Positions are independent of:

- Piece Identity
- Piece Signature
- Piece Orientation
- Cube Orientation

The mapping between Pieces and Positions is defined by the Piece State specification.

---

# Position Notation

This specification adopts the standard cubing notation for Position identifiers.

The notation is defined in terms of the Logical Faces as follows.

| Logical Face | Position Identifier |
|--------------|---------------------|
| TOP | U |
| BOTTOM | D |
| FRONT | F |
| BACK | B |
| LEFT | L |
| RIGHT | R |

These identifiers are used throughout the remainder of this specification.

For example,

```
UF
```

represents the Edge Position at the intersection of the **TOP** and **FRONT** Logical Faces.

Likewise,

```
DBR
```

represents the Corner Position at the intersection of the **BOTTOM**, **BACK**, and **RIGHT** Logical Faces.

---

# Position Types

A standard 3×3×3 cube defines exactly twenty-six Positions.

| Position Type | Count | Occupied By |
|--------------|------:|------------:|
| Center | 6 | Center Piece |
| Edge | 12 | Edge Piece |
| Corner | 8 | Corner Piece |

Each Position accepts exactly one compatible Piece Type.

A Piece shall never occupy an incompatible Position Type.

For example,

- an Edge Piece may occupy only an Edge Position.
- a Corner Piece may occupy only a Corner Position.
- a Center Piece may occupy only a Center Position.

---

# Center Positions

The specification defines exactly six Center Positions.

```
U
D

F
B

L
R
```

Each Center Position corresponds directly to one Logical Face.

Center Positions are immutable.

The Piece occupying a Center Position never changes.

The relationship between Center Positions and Center Pieces is defined by the Cube Orientation specification.

---

# Edge Positions

The specification defines exactly twelve Edge Positions.

```
UF
UR
UB
UL

FR
FL
BR
BL

DF
DR
DB
DL
```

Each Edge Position is defined by the intersection of exactly two Logical Faces.

For example,

```
UF
```

represents the Position shared by the **TOP** and **FRONT** Logical Faces.

---

# Corner Positions

The specification defines exactly eight Corner Positions.

```
UFR
UFL
UBL
UBR

DFR
DFL
DBL
DBR
```

Each Corner Position is defined by the intersection of exactly three Logical Faces.

For example,

```
UFR
```

represents the Position shared by the **TOP**, **FRONT**, and **RIGHT** Logical Faces.

---

# Position Identity

Every Position has a unique identity.

Position identity never changes.

A Position is identified solely by its Position Type and its location relative to the Logical Faces.

Position identity is independent of:

- Piece Identity
- Piece Signature
- Piece Orientation
- Cube Orientation

---

# Position Equality

Two Positions are equal if and only if they represent the same logical location within the cube.

---

# Position Compatibility

Every Position accepts exactly one compatible Piece Type.

| Position Type | Compatible Piece |
|--------------|------------------|
| Center | Center Piece |
| Edge | Edge Piece |
| Corner | Corner Piece |

Assigning a Piece to an incompatible Position shall be considered invalid.

---

# Position Occupancy

Every Position is occupied by exactly one Piece.

Every Piece occupies exactly one Position.

No Position may contain multiple Pieces.

No Piece may occupy multiple Positions.

---

# Effect of Moves

Moves modify the Position occupied by movable Pieces.

Moves never create, remove, or modify Positions.

Center Pieces always remain in their respective Center Positions.

Positions are immutable.

---

# Effect of Transformations

Cube Transformations do not modify Positions.

Positions remain fixed relative to the Logical Faces.

Transformations modify the Cube Orientation and rewrite the Piece States accordingly.

As a result, the Position associated with a Piece may change, while the definition of every Position remains unchanged.

---

# Invariants

The following properties shall always hold.

- Every Position has exactly one Position Type.
- Every Position has a unique identity.
- Every Position is occupied by exactly one compatible Piece.
- Every Piece occupies exactly one Position.
- Positions are immutable.
- The set of Positions never changes.

---

# Description

Every Position should provide a human-readable description.

Examples

```
Edge Position

UF
```

```
Corner Position

DBR
```

The formatting of the description is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

- represents all twenty-six Positions.
- preserves Position identities.
- preserves Position compatibility.
- maintains exactly one Piece per Position.
- maintains exactly one Position per Piece.
- preserves Positions during moves.
- preserves Positions during cube transformations.