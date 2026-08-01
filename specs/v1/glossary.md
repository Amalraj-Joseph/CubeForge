# Glossary

This glossary defines the terminology used throughout the 3×3 Cube Specification.

---

# Algorithm

An immutable, ordered sequence of Moves.

Applying an Algorithm applies each Move in sequence to transform a Cube State.

See: **09-algorithms.md**

---

# Canonical Cube State

The unique reference Cube State defined by this specification.

It consists of the Canonical Cube Orientation together with every Piece in its canonical Position and canonical Orientation.

See: **07-cube-state.md**

---

# Canonical Cube Orientation

The reference Cube Orientation defined by this specification.

By convention,

* Top = White
* Front = Green

The remaining mappings are uniquely determined.

See: **04-orientation.md**

---

# Center Piece

A Piece consisting of exactly one color.

Center Pieces define Cube Orientation and never change relative to one another.

See: **02-pieces.md**

---

# Center Position

A Position corresponding to one Logical Face.

Each Center Position is permanently occupied by its corresponding Center Piece.

See: **05-positions.md**

---

# Color

One of the six immutable colors defined by this specification.

Colors uniquely identify Pieces through Piece Signatures.

See: **01-colors.md**

---

# Cube

The complete mathematical model of a standard 3×3×3 cube.

A Cube is represented by its current Cube State.

---

# Cube Orientation

The mapping between Logical Faces and Center Pieces.

Cube Orientation defines the observer's frame of reference.

See: **04-orientation.md**

---

# Cube State

The complete observable state of a Cube.

A Cube State consists of a Cube Orientation together with the Piece State of every Piece.

See: **07-cube-state.md**

---

# Cube Transformation

A deterministic transformation that changes the observer's frame of reference without changing the physical arrangement of the puzzle.

Cube Transformations preserve the Solved property.

See: **10-transformations.md**

---

# Edge Piece

A Piece consisting of exactly two colors.

Edge Pieces may occupy only Edge Positions.

See: **02-pieces.md**

---

# Edge Position

A Position located at the intersection of two Logical Faces.

Only Edge Pieces may occupy Edge Positions.

See: **05-positions.md**

---

# Identity Transformation

A Transformation that leaves the Cube State unchanged.

Examples include the Empty Algorithm and a Move followed immediately by its inverse.

---

# Logical Face

One of the six logical directions:

* U
* D
* F
* B
* L
* R

Logical Faces provide the frame of reference used throughout the specification.

See: **03-logical-faces.md**

---

# Move

An immutable, deterministic transformation that rotates exactly one layer of the cube.

Moves preserve Cube Orientation while modifying Piece States.

See: **08-moves.md**

---

# Orientation

The mapping between the colors of a Piece Signature and the Logical Faces defining the Piece's current Position.

Orientation describes how a Piece is rotated within its Position.

See: **06-piece-state.md**

---

# Piece

A physical cubie identified by an immutable Piece Signature.

Pieces are immutable.

See: **02-pieces.md**

---

# Piece Signature

The immutable, unordered set of colors that uniquely identifies a Piece.

Neither Moves nor Cube Transformations modify a Piece Signature.

See: **02-pieces.md**

---

# Piece State

The mutable state of a Piece.

A Piece State consists of a Piece Signature, Position, and Orientation.

See: **06-piece-state.md**

---

# Position

A logical placeholder within the Cube that may be occupied by exactly one compatible Piece.

Positions are immutable.

See: **05-positions.md**

---

# Position Type

The classification of a Position.

The specification defines three Position Types:

* Center
* Edge
* Corner

See: **05-positions.md**

---

# Solved Property

A derived property of a Cube State.

A Cube State is solved if every Piece occupies its correct Position and Orientation relative to the current Center Pieces.

The Solved property is independent of Cube Orientation.

See: **07-cube-state.md**

---

# Transformation

The general mathematical concept of converting one valid Cube State into another valid Cube State.

Moves, Algorithms, and Cube Transformations are all categories of Transformations.

See: **09-algorithms.md** and **10-transformations.md**
