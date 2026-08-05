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

These rules apply in every legal Cube Orientation.

---

# Compliance

An implementation conforms to this specification if it:

* rejects Cube States with an odd Edge orientation sum
* rejects Cube States with a Corner orientation sum not divisible by three
* rejects Cube States whose Edge and Corner permutation parity differ
