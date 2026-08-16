---
layout: page
title: Pieces · Specification
---

<p><a class="spec-crumb" href="{{ '/specification.html' | relative_url }}">&larr; Specification index</a></p>

# Pieces

## Purpose

This document defines the physical pieces that make up a standard 3×3×3 cube.

A piece is a physical cubie identified by an immutable **piece signature**. Every piece has a permanent identity that never changes throughout the lifetime of a cube.

This specification defines piece types, piece signatures, piece identities, and piece legality. It does not define piece position or orientation.

---

# Piece Types

A standard 3×3×3 cube consists of exactly twenty-six pieces.

| Type | Count | Colors |
|------|------:|-------:|
| Center | 6 | 1 |
| Edge | 12 | 2 |
| Corner | 8 | 3 |

Every piece belongs to exactly one type.

The type of a piece is immutable.

---

# Piece Identity

Every piece has a unique identity.

A piece's identity is represented by its **piece signature**.

Piece identity never changes throughout the lifetime of the piece.

Identity is independent of:

- Position
- Orientation
- Cube Orientation

Example

```
Corner(WHITE, GREEN, RED)
```

always refers to the same physical corner piece.

---

# Piece Signature

A **piece signature** is the immutable, unordered set of colors that uniquely identifies a physical piece.

Every piece has exactly one piece signature.

A piece signature is independent of:

- Position
- Orientation
- Cube Orientation

The order of colors within a piece signature is not significant.

For example, the following signatures represent the same edge piece.

```
Edge(WHITE, GREEN)

Edge(GREEN, WHITE)
```

Likewise, the following signatures represent the same corner piece.

```
Corner(WHITE, GREEN, RED)

Corner(RED, WHITE, GREEN)

Corner(GREEN, RED, WHITE)
```

A piece signature shall remain constant throughout the lifetime of a piece.

Neither moves nor cube transformations shall modify a piece signature.

Piece signatures are used to uniquely identify pieces, validate legality, compare pieces, and reference pieces throughout this specification.

---

# Center Pieces

A center piece contains exactly one color.

Examples

```
Center(WHITE)

Center(GREEN)

Center(RED)
```

Every color has exactly one corresponding center piece.

---

# Edge Pieces

An edge piece contains exactly two colors.

Examples

```
Edge(WHITE, GREEN)

Edge(WHITE, RED)

Edge(BLUE, ORANGE)
```

The order of colors does not affect the piece signature.

---

# Corner Pieces

A corner piece contains exactly three colors.

Examples

```
Corner(WHITE, GREEN, RED)

Corner(YELLOW, BLUE, ORANGE)
```

The order of colors does not affect the piece signature.

---

# Piece Legality

Only physically possible pieces are permitted.

Implementations shall reject illegal piece definitions.

A piece is illegal if:

- it contains duplicate colors
- it contains opposite colors
- it contains an incorrect number of colors for its type

Examples

```
Edge(WHITE, WHITE)

Edge(WHITE, YELLOW)

Edge(RED, ORANGE)

Corner(WHITE, WHITE, GREEN)

Corner(WHITE, YELLOW, GREEN)

Corner(RED, ORANGE, BLUE)
```

Every compliant implementation shall represent exactly the following legal pieces.

## Center Pieces

```
WHITE
YELLOW
GREEN
BLUE
RED
ORANGE
```

## Edge Pieces

```
WHITE GREEN
WHITE RED
WHITE BLUE
WHITE ORANGE

YELLOW GREEN
YELLOW RED
YELLOW BLUE
YELLOW ORANGE

GREEN RED
GREEN ORANGE
BLUE RED
BLUE ORANGE
```

## Corner Pieces

```
WHITE GREEN RED
WHITE RED BLUE
WHITE BLUE ORANGE
WHITE ORANGE GREEN

YELLOW GREEN RED
YELLOW RED BLUE
YELLOW BLUE ORANGE
YELLOW ORANGE GREEN
```

---

# Piece Equality

Two pieces are equal if and only if they have identical piece signatures.

Since a piece signature is unordered, the order of colors shall not affect equality.

---

# Piece Immutability

A piece is an immutable value object.

Once created, none of the following properties may change.

- Type
- Piece Signature
- Identity
- Colors

Position and orientation are intentionally excluded because they are not properties of the piece itself.

Those concepts are defined by the Piece State specification.

---

# Invariants

The following properties shall always hold.

- Every piece has exactly one type.
- Every piece has exactly one piece signature.
- Piece signatures are immutable.
- No two pieces share the same piece signature.
- Every legal piece is unique.

---

# Description

Every piece should provide a human-readable description.

Example

```
Type

Corner

Signature

WHITE
GREEN
RED
```

The formatting of the description is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

- represents all twenty-six legal pieces
- rejects illegal piece definitions
- preserves piece identities
- preserves piece signatures
- treats piece signatures as unordered
- exposes immutable piece definitions

<nav class="spec-pager">
  <a class="spec-pager__prev" href="{{ '/specification/01-colors.html' | relative_url }}">&larr; Colors</a>
  <a class="spec-pager__next" href="{{ '/specification/03-logical-faces.html' | relative_url }}">Logical Faces &rarr;</a>
</nav>
