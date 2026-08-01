# 3×3 Cube Specification
**Version:** 0.1 (Draft)

## Overview

This specification defines a language-agnostic mathematical model of a standard 3×3×3 Rubik's Cube.

The objective of this specification is to provide a canonical representation of a cube that can be implemented consistently in any programming language. The specification defines the cube in terms of immutable identities, mutable state, legal operations, and deterministic transformations. It intentionally avoids prescribing implementation details or storage formats.

The scope of this specification includes:

- Cube representation
- Piece representation
- Piece state
- Cube state
- Cube orientation
- Legal moves
- Cube transformations

The specification does **not** define:

- Solving algorithms
- Search algorithms
- Rendering
- User interfaces
- Storage formats
- Performance optimizations

---

# 1. Colors

A cube consists of six unique colors.

Each color is uniquely identifiable and immutable.

A color consists of:

- Unique identifier
- Human-readable name

Implementations may attach additional metadata such as RGB values or textures, but these are outside the scope of this specification.

Example:

```
WHITE
YELLOW
GREEN
BLUE
RED
ORANGE
```

---

# 2. Pieces

A cube consists of exactly twenty-six physical pieces.

```
6 Center Pieces
12 Edge Pieces
8 Corner Pieces
```

Each physical piece has a permanent identity.

Piece identities never change throughout the lifetime of a cube.

---

## 2.1 Center Piece

A center piece contains exactly one color.

Example

```
Center(WHITE)
```

Center pieces never change position relative to one another.

---

## 2.2 Edge Piece

An edge piece contains exactly two colors.

Example

```
Edge(WHITE, GREEN)
```

The combination of colors uniquely identifies the piece.

---

## 2.3 Corner Piece

A corner piece contains exactly three colors.

Example

```
Corner(WHITE, GREEN, RED)
```

The combination of colors uniquely identifies the piece.

---

# 3. Piece Identity

The identity of a piece is immutable.

Identity is determined solely by the colors belonging to that piece.

Identity is independent of:

- Position
- Orientation
- Cube orientation

Example

```
Corner(WHITE, GREEN, RED)
```

always refers to the same physical corner cubie.

---

# 4. Piece Legality

Only physically possible pieces may exist.

The specification shall reject impossible pieces.

Examples of illegal pieces include:

```
Edge(WHITE, YELLOW)

Edge(RED, ORANGE)

Corner(WHITE, YELLOW, GREEN)

Corner(RED, ORANGE, BLUE)
```

Opposite colors shall never belong to the same piece.

---

# 5. Faces

Faces are logical references used to describe cube orientation.

The six logical faces are

```
TOP
BOTTOM
FRONT
BACK
LEFT
RIGHT
```

Faces are **not** colors.

The mapping between faces and colors is defined by the cube orientation.

---

# 6. Cube Orientation

Cube orientation defines the relationship between logical faces and center pieces.

Example

```
TOP -> WHITE

FRONT -> GREEN

RIGHT -> RED
```

The remaining mappings are implied.

Cube orientation changes only through cube transformations.

Moves never modify cube orientation.

Only physically possible orientations are legal.

Example

```
TOP -> WHITE
BOTTOM -> WHITE
```

is illegal.

Likewise,

```
TOP -> WHITE
FRONT -> YELLOW
```

is illegal because TOP and FRONT cannot reference opposite faces.

---

# 7. Positions

Positions describe where a piece currently resides.

Positions are placeholders within the cube.

Every position accepts exactly one compatible piece.

Examples

Edge positions

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

Corner positions

```
URF
UFL
ULB
UBR

DFR
DLF
DBL
DRB
```

Center positions are

```
TOP
BOTTOM
FRONT
BACK
LEFT
RIGHT
```

---

# 8. Piece Orientation

Piece orientation describes how a piece is rotated relative to the logical faces.

Orientation does not affect identity.

Example

```
Corner

WHITE -> TOP

GREEN -> FRONT

RED -> RIGHT
```

After several moves

```
WHITE -> FRONT

GREEN -> RIGHT

RED -> BOTTOM
```

The piece remains the same physical piece.

Only its orientation changes.

---

# 9. Piece State

The state of a piece is defined as

```
Piece State

=

Position

+

Orientation
```

Identity is intentionally excluded because it never changes.

---

# 10. Cube State

The complete state of a cube is defined as

```
Cube State

=

Cube Orientation

+

State of every Piece
```

This fully describes the cube.

---

# 11. Moves

Moves rotate one or more layers of the cube.

Moves operate relative to the current cube orientation.

Moves never modify cube orientation.

Moves modify

- piece positions
- piece orientations

Moves never modify

- piece identities
- center mapping

Standard move notation shall be used.

Examples

```
U
D
L
R
F
B

U'
R'

F2
```

The notation specification is defined separately.

---

# 12. Cube Transformations

Cube transformations rotate the entire cube.

Transformations modify the cube orientation.

Transformations also rewrite every piece state so that the cube remains mathematically consistent under the new frame of reference.

Transformations never alter the physical arrangement of pieces.

Examples include

```
Rotate Left

Rotate Right

Rotate Up

Rotate Down

Roll Clockwise

Roll Counter-clockwise
```

Transformations are deterministic.

---

# 13. Description Interface

Every model defined by this specification should provide a human-readable description.

The purpose of this interface is debugging, testing and visualization.

Example

```
Corner

Identity

WHITE
GREEN
RED

Position

DFR

Orientation

WHITE -> FRONT

GREEN -> RIGHT

RED -> BOTTOM
```

The output format is implementation-defined but should clearly expose the model's state.

---

# 14. Data Models

The following conceptual data models are defined by this specification.

## Color

Represents a unique cube color.

---

## Piece

Represents a physical cube piece.

Properties

- Identity
- Type

---

## Piece State

Represents the mutable state of a piece.

Properties

- Position
- Orientation

---

## Cube Orientation

Represents the mapping between logical faces and center pieces.

---

## Cube

Represents the complete cube.

Properties

- Cube Orientation
- Collection of Piece States

---

# 15. Conceptual Functions

The specification defines the following conceptual operations.

These operations define behavior only.

They do not prescribe implementation.

## Cube

- applyMove(move)
- applyMoves(sequence)
- transform(transformation)
- reset()
- describe()

---

## Piece

- identity()
- type()
- describe()

---

## Piece State

- position()
- orientation()
- describe()

---

## Cube Orientation

- top()
- front()
- left()
- right()
- back()
- bottom()
- transform()
- describe()

---

# 16. Determinism

All operations defined by this specification shall be deterministic.

Given identical cube states and identical operations, every compliant implementation shall produce identical results.

---

# 17. Compliance

An implementation conforms to this specification if it:

- Represents all legal pieces.
- Rejects illegal pieces.
- Maintains immutable piece identities.
- Preserves cube invariants.
- Correctly performs legal moves.
- Correctly performs cube transformations.
- Produces deterministic results.
- Maintains mathematically valid cube states after every operation.