# Notation

## Purpose

This document defines the notation used throughout the 3×3 Cube Specification.

The notation defined herein is normative.

Implementations shall interpret notation according to this specification.

---

# Logical Face Notation

The specification defines the following identifiers for the six Logical Faces.

| Logical Face | Identifier |
| ------------ | ---------- |
| Top          | U          |
| Bottom       | D          |
| Front        | F          |
| Back         | B          |
| Left         | L          |
| Right        | R          |

These identifiers shall be used consistently throughout the specification.

---

# Position Notation

Positions are represented by the concatenation of their defining Logical Faces.

Examples

## Center Positions

```text
U
D
F
B
L
R
```

## Edge Positions

```text
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

## Corner Positions

```text
UFR
UFL
UBL
UBR

DFR
DFL
DBL
DBR
```

---

# Move Notation

Moves use standard Singmaster notation.

A Move consists of

* a face identifier
* an optional modifier

Examples

```text
R
U
F
```

---

# Move Modifiers

The following modifiers are defined.

| Modifier | Meaning               |
| -------- | --------------------- |
| *(none)* | 90° clockwise         |
| `'`      | 90° counter-clockwise |
| `2`      | 180°                  |

Examples

```text
R
R'
R2
```

---

# Algorithm Notation

Algorithms are represented as ordered sequences of Moves separated by whitespace.

Example

```text
R U R' U'
```

Whitespace separates Moves.

Leading and trailing whitespace may be ignored.

---

# Reserved Symbols

The following symbols have reserved meanings.

| Symbol | Meaning                    |
| ------ | -------------------------- |
| `'`    | Counter-clockwise modifier |
| `2`    | Double rotation            |
| Space  | Move separator             |

Implementations shall not assign alternative meanings to reserved symbols.

---

# Case Sensitivity

Notation is case-sensitive.

The identifiers defined by this specification shall be represented using uppercase letters.

Examples

```text
R
U
UF
DBR
```

Lowercase identifiers are outside the scope of this specification.

---

# Extensibility

Implementations may support additional notation systems.

Support for additional notation shall not alter the meaning of the notation defined by this specification.

---

# Compliance

An implementation conforms to this specification if it

* correctly interprets every identifier defined herein.
* preserves the meaning of standard notation.
* correctly parses Algorithms.
* preserves Move ordering.
