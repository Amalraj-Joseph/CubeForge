---
layout: page
title: Orientation · Specification
---

<p><a class="spec-crumb" href="{{ '/specification.html' | relative_url }}">&larr; Specification index</a></p>

# Cube Orientation

## Purpose

This document defines the orientation of a cube.

Cube Orientation establishes the mapping between **Logical Faces** and **Center Pieces**. It provides the frame of reference used to interpret piece positions, piece orientations, and moves.

Cube Orientation is independent of the arrangement of movable pieces.

---

# Definition

A **Cube Orientation** is defined by the mapping of exactly two adjacent **Logical Faces**:

* `TOP`
* `FRONT`

to their corresponding **Center Pieces**.

These two mappings uniquely determine the mappings for the remaining four Logical Faces.

Example

```
TOP   -> WHITE
FRONT -> GREEN
```

uniquely determines

```
BOTTOM -> YELLOW
BACK   -> BLUE
RIGHT  -> RED
LEFT   -> ORANGE
```

Thus, a Cube Orientation is fully determined by the Center Pieces assigned to the `TOP` and `FRONT` Logical Faces.

---

# Properties

A Cube Orientation has the following properties.

* `TOP` and `FRONT` shall always map to adjacent Center Pieces.
* Every Logical Face maps to exactly one Center Piece.
* Every Center Piece maps to exactly one Logical Face.
* The mapping between Logical Faces and Center Pieces is bijective.

The complete face-to-center mapping is derived from the `TOP` and `FRONT` mappings.

---

# Legal Orientations

Only physically achievable orientations are permitted.

A Cube Orientation is legal if and only if:

* `TOP` and `FRONT` map to adjacent Center Pieces.
* Every Center Piece is mapped exactly once.
* Opposite Logical Faces map to opposite Center Pieces.
* Adjacent Logical Faces map to adjacent Center Pieces.

There are exactly twenty-four legal Cube Orientations.

Examples of illegal orientations include

```
TOP   -> WHITE
FRONT -> YELLOW
```

because `WHITE` and `YELLOW` are opposite Center Pieces.

Likewise,

```
TOP   -> GREEN
FRONT -> BLUE
```

is illegal because `GREEN` and `BLUE` are opposite Center Pieces.

---

# Canonical Orientation

Every implementation shall define the following canonical orientation.

```
TOP    -> WHITE
BOTTOM -> YELLOW

FRONT  -> GREEN
BACK   -> BLUE

RIGHT  -> RED
LEFT   -> ORANGE
```

Equivalently, the canonical orientation may be represented as

```
TOP   -> WHITE
FRONT -> GREEN
```

A newly constructed solved cube shall use the canonical orientation unless explicitly specified otherwise.

---

# Orientation Equality

Two Cube Orientations are equal if and only if they map the same Center Piece to the `TOP` Logical Face and the same Center Piece to the `FRONT` Logical Face.

Since all remaining mappings are derived, this is sufficient to determine equality.

---

# Effect of Moves

Moves shall not modify Cube Orientation.

Regardless of the sequence of moves applied, the mapping between Logical Faces and Center Pieces remains unchanged.

Only the states of movable pieces are modified.

Example

```
R U R' U'
```

After applying the sequence above, the Cube Orientation is unchanged.

---

# Effect of Transformations

Cube Transformations modify Cube Orientation.

A transformation changes the mapping between Logical Faces and Center Pieces while preserving the physical arrangement of the cube.

Example

Before

```
TOP   -> WHITE
FRONT -> GREEN
```

After rotating the cube upward

```
TOP   -> BLUE
FRONT -> WHITE
```

The resulting orientation shall be one of the twenty-four legal Cube Orientations.

The behaviour of transformations is defined by the Cube Transformations specification.

---

# Internal Representation

This specification defines only the observable behaviour of Cube Orientation.

Implementations may internally represent a Cube Orientation using:

* the `TOP` and `FRONT` mappings,
* all six Logical Face mappings, or
* any equivalent representation capable of deriving the complete orientation.

The internal representation is implementation-defined.

---

# Invariants

The following properties shall always hold.

* `TOP` and `FRONT` map to adjacent Center Pieces.
* Cube Orientation is always one of the twenty-four legal orientations.
* Every Logical Face maps to exactly one Center Piece.
* Every Center Piece maps to exactly one Logical Face.
* Opposite Logical Faces always map to opposite Center Pieces.
* Adjacent Logical Faces always map to adjacent Center Pieces.

---

# Description

Every Cube Orientation should provide a human-readable description.

Example

```
TOP    -> WHITE
BOTTOM -> YELLOW

FRONT  -> GREEN
BACK   -> BLUE

RIGHT  -> RED
LEFT   -> ORANGE
```

The formatting of the description is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

* represents only legal Cube Orientations
* rejects illegal Cube Orientations
* supports the canonical orientation
* preserves Cube Orientation during moves
* correctly updates Cube Orientation during transformations
* derives the complete Logical Face mapping from the defined orientation


<nav class="spec-pager">
  <a class="spec-pager__prev" href="{{ '/specification/03-logical-faces.html' | relative_url }}">&larr; Logical Faces</a>
  <a class="spec-pager__next" href="{{ '/specification/05-positions.html' | relative_url }}">Positions &rarr;</a>
</nav>
