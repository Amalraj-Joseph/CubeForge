---
layout: page
title: API · Specification
---

<p><a class="spec-crumb" href="{{ '/specification.html' | relative_url }}">&larr; Specification index</a></p>

# API Capabilities

## Purpose

This document defines the minimum capabilities that every compliant implementation shall provide.

This specification does not prescribe programming language constructs, object models, method names, function names, module layouts, or service interfaces.

Implementations may expose these capabilities through classes, interfaces, functions, modules, services, command-line interfaces, Model Context Protocol (MCP) tools, or any other language-appropriate mechanism.

---

# Design Principles

Every implementation shall expose the capabilities defined by this specification while preserving the mathematical model and behavioural guarantees defined throughout the specification.

The API surface is implementation-defined.

Only the observable behaviour is prescribed.

---

# Cube Construction

An implementation shall provide the capability to

* construct a Cube in the Canonical Cube State.
* construct a Cube from a valid Cube State.
* construct a Cube from a serialized representation, if serialization is supported.

Implementations may reject invalid Cube States.

---

# Cube Inspection

An implementation shall provide the capability to inspect

* Cube State.
* Cube Orientation.
* Piece States.
* Piece Signatures.
* Piece Positions.
* Piece Orientations.
* the Solved property.

Implementations may expose additional derived properties.

---

# Move Capabilities

An implementation shall provide the capability to

* represent standard Moves.
* interpret Move notation.
* apply a Move.
* apply multiple Moves sequentially.
* determine Move equality.
* compute the inverse of a Move.

Applying a Move shall update the Cube State according to the Move specification.

---

# Algorithm Capabilities

An implementation shall provide the capability to

* represent Algorithms.
* interpret Algorithm notation.
* apply an Algorithm.
* compose Algorithms.
* compute the inverse of an Algorithm.
* determine Algorithm equality.

Implementations may expose additional Algorithm capabilities.

---

# Cube Transformation Capabilities

An implementation shall provide the capability to

* represent Cube Transformations.
* apply a Cube Transformation.
* compose Cube Transformations.
* compute the inverse of a Cube Transformation.
* determine Cube Transformation equality.

Applying a Cube Transformation shall preserve the Solved property.

---

# Equality

An implementation shall provide the capability to determine equality for

* Colors.
* Pieces.
* Positions.
* Piece States.
* Cube Orientations.
* Cube States.
* Moves.
* Algorithms.
* Cube Transformations.

Equality shall conform to the corresponding specification documents.

---

# Validation

An implementation shall provide the capability to determine whether

* a Piece is valid.
* a Cube Orientation is valid.
* a Cube State is valid.

Implementations may expose additional validation capabilities.

---

# Description

An implementation shall provide the capability to produce human-readable descriptions for

* Colors.
* Pieces.
* Positions.
* Piece States.
* Cube Orientation.
* Cube State.
* Moves.
* Algorithms.
* Cube Transformations.

The formatting of descriptions is implementation-defined.

---

# Serialization

Serialization is optional.

If supported, an implementation shall provide the capability to

* serialize a Cube State.
* deserialize a Cube State.

The serialization format is implementation-defined and outside the scope of this specification.

---

# Extensibility

Implementations may provide capabilities beyond those defined by this specification.

Additional capabilities shall preserve the mathematical model, behavioural guarantees, and invariants defined throughout this specification.

---

# Compliance

An implementation conforms to this API specification if it provides every mandatory capability defined in this document while preserving the behaviour, invariants, and mathematical model specified throughout the remainder of this specification.


<nav class="spec-pager">
  <a class="spec-pager__prev" href="{{ '/specification/10-transformations.html' | relative_url }}">&larr; Transformations</a>
  <a class="spec-pager__next" href="{{ '/specification/12-compliance.html' | relative_url }}">Compliance &rarr;</a>
</nav>
