---
layout: page
title: Validity & Parity · Specification
---

<p><a class="spec-crumb" href="{{ '/specification.html' | relative_url }}">&larr; Specification index</a></p>

# Cube Validity and Parity

## Purpose

This document defines the mathematical validity rules for a standard 3×3×3
cube state.

These rules supplement the structural Cube State invariants.

---

# Validity Rules

A Cube State is mathematically valid only if all of the following hold.

* The sum of all Edge orientations is even.
* The sum of all Corner orientations is divisible by three.
* The parity of the Edge permutation matches the parity of the Corner
  permutation.
* Every Center Piece's Position agrees with the Cube Orientation: for each
  Logical Face, the Center Piece occupying that face's Position shall have
  the Color that the Cube Orientation assigns to that Logical Face.

These rules apply in every legal Cube Orientation.

Center Pieces never permute relative to one another on a physical cube;
the Cube Orientation is precisely the record of which Color currently
faces which Logical Face. A Cube State whose Center placement disagrees
with its own Cube Orientation describes no physically reachable cube and
is therefore invalid.

---

# Compliance

An implementation conforms to this specification if it:

* rejects Cube States with an odd Edge orientation sum
* rejects Cube States with a Corner orientation sum not divisible by three
* rejects Cube States whose Edge and Corner permutation parity differ
* rejects Cube States whose Center Piece placement disagrees with their
  Cube Orientation


<nav class="spec-pager">
  <a class="spec-pager__prev" href="{{ '/specification/13-notation.html' | relative_url }}">&larr; Notation</a>
</nav>
