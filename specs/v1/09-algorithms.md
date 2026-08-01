# Algorithms

## Purpose

This document defines Algorithms for a standard 3×3×3 cube.

An **Algorithm** is an immutable, ordered sequence of Moves.

Algorithms provide a reusable and deterministic way of describing Cube transformations through the composition of individual Moves.

---

## Terminology

This specification distinguishes between the following related concepts.

### Transformation

A **Transformation** is the general mathematical concept of converting one valid Cube State into another valid Cube State.

Transformations are deterministic and preserve the validity of the Cube State.

### Algorithm

An **Algorithm** is an ordered sequence of **Moves**.

An Algorithm transforms the puzzle by applying each Move in sequence.

Algorithms change the state of the puzzle while preserving the Cube Orientation.

### Cube Transformation

A **Cube Transformation** changes the observer's frame of reference without changing the physical arrangement of the puzzle.

Cube Transformations modify the Cube Orientation and rewrite the Piece States accordingly.

Unlike Algorithms, Cube Transformations preserve the solved property of the cube.

Throughout this specification, the term **Transformation** refers to the general mathematical concept, while **Algorithm** and **Cube Transformation** refer to two distinct categories of transformations.

# Definition

An Algorithm consists of zero or more Moves arranged in a defined order.

```text
Algorithm

=

Ordered Sequence of Moves
```

Every Move within an Algorithm shall conform to the Move specification.

Algorithms are immutable.

---

# Empty Algorithm

An Algorithm may contain zero Moves.

An Algorithm containing no Moves is called the **Empty Algorithm**.

Applying the Empty Algorithm shall produce the identity transformation.

---

# Move Order

Moves within an Algorithm are executed sequentially from left to right.

For example,

```text
R U R' U'
```

is evaluated as

```text
(((Cube → R) → U) → R') → U'
```

Every Move operates on the Cube State produced by the previous Move.

---

# Algorithm Notation

Algorithms are represented using standard Move notation separated by whitespace.

Example

```text
R U R' U'

F R U R' U' F'
```

The exact formatting is implementation-defined provided the Move ordering is preserved.

---

# Equality

Two Algorithms are equal if and only if they contain identical Moves in the same order.

For example,

```text
R U

==

R U
```

whereas

```text
U R
```

is not equal to

```text
R U
```

even if both Algorithms eventually produce the same Cube State under certain circumstances.

Algorithm Equality is structural, not behavioural.

---

# Length

The length of an Algorithm is the number of Moves it contains.

Examples

```text
R
```

Length = 1

```text
R U R' U'
```

Length = 4

The Empty Algorithm has length zero.

---

# Application

Applying an Algorithm consists of applying each Move in order.

An Algorithm transforms one valid Cube State into another valid Cube State.

Applying an Algorithm shall always produce a valid Cube State.

---

# Composition

Two Algorithms may be composed.

The composition of two Algorithms is the concatenation of their Move sequences.

Example

```text
A

R U
```

```text
B

F R'
```

Composition

```text
A ∘ B

R U F R'
```

Composition preserves Move ordering.

---

# Inverse Algorithm

Every Algorithm has exactly one inverse.

The inverse Algorithm is constructed by

1. reversing the Move order, and
2. replacing every Move with its inverse.

Example

```text
Algorithm

R U R' U'
```

Inverse

```text
U R U' R'
```

Applying an Algorithm immediately followed by its inverse shall restore the original Cube State.

---

# Identity Algorithm

An Algorithm is an **Identity Algorithm** if applying it does not modify the Cube State.

Examples

```text
R R'

U U'

F2 F2

R R R R
```

The Empty Algorithm is an Identity Algorithm.

Determining whether an arbitrary Algorithm is an Identity Algorithm is implementation-defined.

---

# Determinism

Algorithms are deterministic.

Given identical Cube States, applying the same Algorithm shall always produce identical Cube States.

---

# Immutability

Algorithms are immutable.

Once created,

* the Move sequence
* the Move ordering
* the Algorithm length

shall never change.

Implementations may construct new Algorithms through composition or inversion, but existing Algorithms shall remain unchanged.

---

# Description

Every Algorithm should provide a human-readable description.

Example

```text
Algorithm

Moves

R U R' U'

Length

4
```

The formatting is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

* represents Algorithms as ordered Move sequences.
* preserves Move ordering.
* correctly applies Algorithms.
* correctly composes Algorithms.
* correctly computes inverse Algorithms.
* supports the Empty Algorithm.
* produces deterministic results.
