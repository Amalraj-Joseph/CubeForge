---
layout: page
title: Specification
---

# Specification

CubeForge's engine is built to a formal specification - not the other
way around. The specification defines the mathematical model and every
invariant; `core/` conforms to it, and that conformance is checked by
an executable, per-requirement compliance suite rather than assumed.

The specification lives in [`specs/`]({{ site.github_repo }}/tree/main/specs)
in the repository; every normative document is also rendered in full
below, so you never have to leave the site to read it. This page is an
index into it - the formal documents themselves are the source of
truth, not this summary.

{% include cube-diagram.html
   up="w,w,w,w,w,w,w,w,w"
   front="g,g,g,g,g,g,g,g,g"
   right="r,r,r,r,r,r,r,r,r"
   px="190" static="true"
   caption="Fourteen documents, one cube: colors in, whole-cube transformations out" %}

## Core model (`specs/v1/`)

| Document | Defines |
|---|---|
| [01 · Colors](specification/01-colors.html) | The six colors and their opposite pairs |
| [02 · Pieces](specification/02-pieces.html) | The twenty-six physical pieces and their identity |
| [03 · Logical Faces](specification/03-logical-faces.html) | The six logical faces |
| [04 · Orientation](specification/04-orientation.html) | Cube orientation and the twenty-four legal orientations |
| [05 · Positions](specification/05-positions.html) | The twenty-six fixed positions |
| [06 · Piece State](specification/06-piece-state.html) | Position + orientation for one piece |
| [07 · Cube State](specification/07-cube-state.html) | The complete cube state, equality, and the Solved property |
| [08 · Moves](specification/08-moves.html) | The eighteen standard moves |
| [09 · Algorithms](specification/09-algorithms.html) | Sequences of moves |
| [10 · Transformations](specification/10-transformations.html) | Whole-cube rotations |
| [11 · API](specification/11-api.html) | The minimum capabilities every implementation shall provide |
| [12 · Compliance](specification/12-compliance.html) | What it means to claim conformance |
| [13 · Notation](specification/13-notation.html) | Singmaster notation |
| [14 · Validity & Parity](specification/14-validity-and-parity.html) | The mathematical validity rules (parity, orientation sums) |

## Supporting documents

| Document | Purpose |
|---|---|
| [Glossary](specification/glossary.html) | Terminology used throughout the spec |
| [Conformance Tests](specification/conformance-tests.html) | What a conformance test suite must verify |

## Historical / non-normative

- [`specs/v0/INITIAL_DRAFT.md`]({{ site.github_repo }}/blob/main/specs/v0/INITIAL_DRAFT.md) -
  the original v0.1 draft. Superseded by everything above; kept for
  history only.
- [`specs/architecture/color.md`]({{ site.github_repo }}/blob/main/specs/architecture/color.md) -
  implementation-specific design rationale for the reference
  implementations' bit-mask `Color` representation. Not part of the
  normative spec - see 01-colors above for that.

## Compliance

An implementation may claim conformance only once every mandatory
requirement in 11-api and 12-compliance is satisfied. `core/`'s own
`tests/compliance/test_spec_compliance.py` is exactly that check, made
executable: one test per mandatory bullet in both documents, run against
the real public API.
