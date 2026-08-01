# Conformance Tests

## Purpose

This document defines the requirements for verifying compliance with the 3×3 Cube Specification.

It does not define an exhaustive test suite.

Instead, it defines the categories of behaviour that every compliant implementation shall verify.

---

# Test Principles

Conformance tests shall verify observable behaviour.

Tests shall not depend on implementation details.

Different implementations may use different internal representations while producing identical observable behaviour.

---

# Piece Tests

The test suite shall verify

* all legal Pieces.
* illegal Piece rejection.
* Piece Signature equality.
* Piece immutability.
* Piece invariants.

---

# Cube Orientation Tests

The test suite shall verify

* all twenty-four legal Cube Orientations.
* illegal orientation rejection.
* canonical orientation.
* orientation equality.
* orientation invariants.

---

# Position Tests

The test suite shall verify

* all twenty-six Positions.
* Position compatibility.
* Position equality.
* Position invariants.

---

# Piece State Tests

The test suite shall verify

* Position updates.
* Orientation updates.
* Piece Signature preservation.
* Piece State equality.

---

# Cube State Tests

The test suite shall verify

* Cube construction.
* Canonical Cube State.
* Solved property.
* Cube State equality.
* Cube State validity.

---

# Move Tests

The test suite shall verify

* all eighteen standard Moves.
* inverse Moves.
* identity Moves.
* Move determinism.
* Move invariants.

Example

```text
Initial

Canonical Cube State

Apply

R

Expected

<reference Cube State>
```

---

# Algorithm Tests

The test suite shall verify

* Algorithm parsing.
* Algorithm application.
* Algorithm composition.
* Algorithm inversion.
* Empty Algorithm.
* Algorithm equality.

Example

```text
Algorithm

R U R' U'

Expected

<reference Cube State>
```

---

# Cube Transformation Tests

The test suite shall verify

* every primitive Cube Transformation.
* inverse Cube Transformations.
* preservation of the Solved property.
* orientation updates.
* Piece State rewriting.

---

# API Capability Tests

The test suite shall verify every mandatory capability defined by the API specification.

---

# Determinism Tests

The test suite shall verify that identical inputs always produce identical outputs.

---

# Reference Test Data

A reference implementation or reference data set may be provided.

Every compliant implementation shall produce identical observable behaviour when evaluated against the reference data.

---

# Compliance

An implementation conforms to this specification if it passes every mandatory conformance test applicable to the implemented features.
