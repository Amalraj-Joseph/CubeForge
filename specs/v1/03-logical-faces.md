# Faces

## Purpose

This document defines the logical faces of a standard 3×3×3 cube.

Faces provide a consistent frame of reference for describing piece positions, piece orientations, moves, and cube orientation.

A face is a logical construct and does not represent a physical color.

The relationship between faces and colors is defined by the Cube Orientation specification.

---

# Defined Faces

The specification defines exactly six logical faces.

```
TOP
BOTTOM
FRONT
BACK
LEFT
RIGHT
```

No additional faces are permitted.

---

# Face Identity

Each face has a unique identity.

A face is immutable and always represents the same logical direction.

For example,

```
TOP
```

always refers to the logical top face of the cube.

It does **not** necessarily refer to a particular color.

The color represented by a face is determined by the current Cube Orientation.

---

# Face Relationships

The following opposite face pairs are defined.

| Face | Opposite |
|--------|----------|
| TOP | BOTTOM |
| FRONT | BACK |
| LEFT | RIGHT |

These relationships are immutable.

---

# Adjacent Faces

Each face is adjacent to exactly four other faces.

For example,

| Face | Adjacent Faces |
|--------|----------------|
| TOP | FRONT, RIGHT, BACK, LEFT |
| BOTTOM | FRONT, LEFT, BACK, RIGHT |
| FRONT | TOP, RIGHT, BOTTOM, LEFT |
| BACK | TOP, LEFT, BOTTOM, RIGHT |
| LEFT | TOP, FRONT, BOTTOM, BACK |
| RIGHT | TOP, BACK, BOTTOM, FRONT |

The order represents the clockwise traversal of adjacent faces when looking directly at the specified face.

---

# Face Equality

Two faces are equal if and only if they represent the same logical face.

---

# Description

Every face should provide a human-readable description.

Example

```
TOP
```

The formatting of the description is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

- represents exactly six logical faces
- preserves immutable face identities
- preserves opposite face relationships
- preserves adjacent face relationships