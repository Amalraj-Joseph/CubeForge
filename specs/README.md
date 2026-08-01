# 3×3 Cube Specification

This directory contains the formal specification for the language-agnostic 3×3 Cube model.

The objective of this specification is to provide a deterministic mathematical model that can be implemented consistently across programming languages.

The specification intentionally separates concepts such as piece identity, cube orientation, moves, transformations, and state to ensure implementations remain consistent while allowing implementation-specific optimizations.

Implementations that conform to this specification should produce identical observable behaviour.