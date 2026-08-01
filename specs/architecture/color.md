# Color

## Purpose

A **Color** represents one of the six immutable colors of a standard 3×3×3 cube.

Colors are fundamental value objects used to construct Piece Signatures and identify Center Pieces.

Colors never change throughout the lifetime of the application.

---

# Mutability

Immutable.

---

# Ownership

Colors are singleton value objects.

They are not owned by any other object and may be freely shared throughout the implementation.

---

# Properties

| Property | Type    | Description                            |
| -------- | ------- | -------------------------------------- |
| mask     | Integer | Unique bit mask identifying the Color. |
| name     | String  | Human-readable name.                   |

---

# Defined Colors

The implementation shall define exactly six Colors.

| Color  | Name   | Bit Mask |   Binary   |
| ------ | ------ | -------: | :--------: |
| WHITE  | White  |        1 | `0b000001` |
| YELLOW | Yellow |        2 | `0b000010` |
| GREEN  | Green  |        4 | `0b000100` |
| BLUE   | Blue   |        8 | `0b001000` |
| RED    | Red    |       16 | `0b010000` |
| ORANGE | Orange |       32 | `0b100000` |

No additional Colors are permitted.

---

# Bit Mask Representation

Every Color is represented by exactly one bit within a six-bit integer.

Each Color occupies a unique bit position.

This representation guarantees that every Color has a unique identifier and enables efficient construction of Piece Signatures using bitwise operations.

Example

```
WHITE

0b000001

GREEN

0b000100

RED

0b010000
```

---

# Responsibilities

A Color is responsible for

* representing one immutable cube color.
* providing a unique identity.
* providing a human-readable name.
* participating in Piece Signature construction.

A Color is not responsible for

* rendering.
* RGB values.
* user interface concerns.
* localization.

---

# Invariants

The following properties shall always hold.

* Every Color has exactly one bit mask.
* Every bit mask contains exactly one set bit.
* Bit masks are unique.
* Names are unique.
* Colors are immutable.

---

# Equality

Two Colors are equal if and only if their bit masks are equal.

Since Colors are singleton value objects, implementations may also compare object identity.

---

# Hashing

The hash value of a Color shall be derived solely from its bit mask.

Hash values shall remain stable throughout the lifetime of the application.

---

# Public Capabilities

Every Color shall provide the following capabilities.

| Capability | Description                           |
| ---------- | ------------------------------------- |
| mask()     | Returns the unique bit mask.          |
| name()     | Returns the display name.             |
| describe() | Returns a human-readable description. |

---

# Relationships

```
Color

↓

PieceSignature

↓

Piece
```

Colors are referenced only by Piece Signatures.

---

# Construction

Colors shall be created exactly once during application initialization.

User code shall not construct additional Colors.

---

# Serialization

Colors may serialize using either

* their bit mask, or
* their symbolic name.

Examples

```
16
```

or

```
RED
```

The serialization format is implementation-defined.

---

# Python Mapping

The reference Python implementation shall represent Color as an `Enum`.

Each enum value shall store

* bit mask
* display name

Example

```python
class Color(Enum):
    WHITE = (0b000001, "White")
```

---

# Java Mapping

The reference Java implementation shall represent Color as an `enum`.

Each enum constant shall store

* bit mask
* display name

Example

```java
public enum Color {
    WHITE(0b000001, "White");
}
```

---

# Implementation Notes

The bit-mask representation is an implementation optimization that directly supports the construction and comparison of Piece Signatures.

For example,

```
WHITE | GREEN | RED

=

0b000001
|
0b000100
|
0b010000

=

0b010101
```

This enables Piece Signatures to be represented efficiently using bitwise operations while preserving the abstraction defined by the specification.

Colors remain immutable singleton value objects and shall never be instantiated after application initialization.
