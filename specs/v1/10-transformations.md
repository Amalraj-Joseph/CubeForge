# Cube Transformations

## Purpose

This document defines Cube Transformations for a standard 3×3×3 cube.

A **Cube Transformation** changes the observer's frame of reference without changing the physical arrangement of the puzzle.

Cube Transformations modify the Cube Orientation and rewrite the Piece States accordingly.

Cube Transformations preserve the solved property of a Cube State.

---

# Definition

A Cube Transformation is an immutable, deterministic transformation of a Cube State.

A Cube Transformation:

* modifies the Cube Orientation.
* rewrites every Piece State to preserve the physical arrangement of the cube.
* preserves Piece Signatures.
* preserves the solved property.

Applying a Cube Transformation transforms one valid Cube State into another valid Cube State.

---

# Primitive Cube Transformations

The specification defines the following primitive Cube Transformations.

## Rotate Left

Rotate the entire cube ninety degrees to the left about the vertical axis.

---

## Rotate Right

Rotate the entire cube ninety degrees to the right about the vertical axis.

---

## Rotate Up

Rotate the entire cube ninety degrees upward about the horizontal axis.

---

## Rotate Down

Rotate the entire cube ninety degrees downward about the horizontal axis.

---

## Roll Clockwise

Rotate the entire cube ninety degrees clockwise about the front-to-back axis.

---

## Roll Counter-clockwise

Rotate the entire cube ninety degrees counter-clockwise about the front-to-back axis.

These primitive Cube Transformations are sufficient to produce every legal Cube Orientation.

---

# Semantics

Every Cube Transformation shall

* preserve Piece Signatures.
* preserve Piece Types.
* preserve the physical arrangement of Pieces.
* preserve the solved property.
* preserve Cube validity.

A Cube Transformation may modify

* Cube Orientation.
* Piece Positions.
* Piece Orientations.

---

# Composition

Cube Transformations may be composed.

Applying multiple Cube Transformations produces another valid Cube Transformation.

Composition is performed sequentially from left to right.

---

# Inverse Cube Transformations

Every Cube Transformation has exactly one inverse.

Applying a Cube Transformation immediately followed by its inverse shall restore the original Cube State.

---

# Identity Cube Transformation

A Cube Transformation is an Identity Cube Transformation if applying it does not modify the Cube State.

Examples include

* Rotate Left followed by Rotate Right.
* Rotate Up followed by Rotate Down.
* Roll Clockwise followed by Roll Counter-clockwise.

The identity Cube Transformation preserves every component of the Cube State.

---

# Equality

Two Cube Transformations are equal if and only if they produce identical Cube Orientations when applied to the Canonical Cube State.

---

# Determinism

Cube Transformations are deterministic.

Given identical Cube States, applying the same Cube Transformation shall always produce identical Cube States.

---

# Immutability

Cube Transformations are immutable.

Once created, their behaviour shall never change.

---

# Description

Every Cube Transformation should provide a human-readable description.

Example

```text id="sg8r9q"
Cube Transformation

Rotate Left
```

The formatting is implementation-defined.

---

# Compliance

An implementation conforms to this specification if it:

* supports every primitive Cube Transformation.
* correctly updates Cube Orientation.
* correctly rewrites Piece States.
* preserves Piece Signatures.
* preserves the solved property.
* preserves Cube validity.
* produces deterministic results.
