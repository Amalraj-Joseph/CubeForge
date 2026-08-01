# Compliance

## Purpose

This document defines the requirements for an implementation to claim compliance with the 3×3 Cube Specification.

Compliance requires adherence to the mathematical model, behavioural guarantees, and invariants defined throughout this specification.

An implementation shall not claim compliance if it violates any mandatory requirement defined by this specification.

---

# Compliance Principles

A compliant implementation shall

* preserve the mathematical model defined by this specification.
* preserve all invariants.
* produce deterministic behaviour.
* expose the mandatory implementation capabilities.
* reject or prevent invalid states.

Implementation details are outside the scope of this specification.

Only observable behaviour is considered when determining compliance.

---

# Mandatory Requirements

A compliant implementation shall

* represent all six Colors.
* represent all twenty-six Pieces.
* represent all six Logical Faces.
* represent all twenty-four legal Cube Orientations.
* represent all twenty-six Positions.
* represent Piece States.
* represent Cube States.
* support all eighteen standard Moves.
* support Algorithms.
* support Cube Transformations.

---

# Behavioural Requirements

A compliant implementation shall

* correctly apply every Move.
* correctly apply every Algorithm.
* correctly apply every Cube Transformation.
* correctly determine equality as defined by this specification.
* correctly derive the Solved property.
* correctly identify the Canonical Cube State.
* preserve Piece Signatures.
* preserve Cube validity after every operation.

---

# Invariant Preservation

A compliant implementation shall preserve every invariant defined throughout this specification.

In particular,

* Piece Signatures shall remain immutable.
* Positions shall remain immutable.
* Cube Orientation shall remain valid.
* Piece Types shall remain compatible with their Positions.
* Every Position shall contain exactly one Piece.
* Every Piece shall occupy exactly one Position.

---

# Determinism

Given identical inputs,

* constructing a Cube,
* applying a Move,
* applying an Algorithm,
* applying a Cube Transformation,

shall always produce identical Cube States.

Observable behaviour shall not depend on implementation details.

---

# Validation

A compliant implementation shall reject or prevent

* illegal Piece definitions.
* illegal Cube Orientations.
* incompatible Piece and Position assignments.
* duplicate Piece Signatures.
* duplicate Position occupancy.
* invalid Cube States.

The mechanism used to detect or report invalid input is implementation-defined.

---

# Optional Features

The following features are optional and are not required for compliance.

* Serialization.
* Visualization.
* Graphical user interfaces.
* Command-line interfaces.
* Model Context Protocol (MCP) tools.
* Solver implementations.
* Scramble generation.
* Performance optimizations.
* Additional notation systems.
* Additional convenience APIs.

Optional features shall preserve every invariant defined by this specification.

---

# Language Independence

This specification is language-independent.

A compliant implementation may be written in any programming language or exposed through any software architecture.

Examples include

* libraries.
* command-line applications.
* web services.
* desktop applications.
* embedded systems.
* MCP servers.

Compliance depends solely on observable behaviour.

---

# Conformance Testing

An implementation should be verified using a conformance test suite.

A conforming implementation shall produce identical observable behaviour for every test case.

The design of the conformance test suite is outside the scope of this specification.

---

# Versioning

Compliance shall be evaluated against a specific version of this specification.

An implementation shall identify the version of the specification to which it conforms.

---

# Claiming Compliance

An implementation may claim compliance only if every mandatory requirement defined by this specification is satisfied.

Optional features shall not affect compliance provided they preserve the mathematical model and behavioural guarantees defined by this specification.

---

# Compliance Statement

A compliant implementation may include a statement similar to the following.

```
This implementation conforms to
The 3×3 Cube Specification
Version X.Y.
```
