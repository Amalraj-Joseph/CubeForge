---
layout: page
title: Specification
---

# Specification

CubeForge's engine is a reference implementation of a formal,
language-agnostic specification - not the other way around. The
specification defines the mathematical model and every invariant;
`core/` is one implementation of it, and any future port (Java, Rust,
C#, whatever) is expected to conform to the same rules and produce
identical observable behavior.

The specification lives in [`specs/`]({{ site.github_repo }}/tree/main/specs)
in the repository. This page is an index into it - the formal documents
themselves are the source of truth, not this summary.

## Core model (`specs/v1/`)

| Document | Defines |
|---|---|
| [01-colors]({{ site.github_repo }}/blob/main/specs/v1/01-colors.md) | The six colors and their opposite pairs |
| [02-pieces]({{ site.github_repo }}/blob/main/specs/v1/02-pieces.md) | The twenty-six physical pieces and their identity |
| [03-logical-faces]({{ site.github_repo }}/blob/main/specs/v1/03-logical-faces.md) | The six logical faces |
| [04-orientation]({{ site.github_repo }}/blob/main/specs/v1/04-orientation.md) | Cube orientation and the twenty-four legal orientations |
| [05-positions]({{ site.github_repo }}/blob/main/specs/v1/05-positions.md) | The twenty-six fixed positions |
| [06-piece-state]({{ site.github_repo }}/blob/main/specs/v1/06-piece-state.md) | Position + orientation for one piece |
| [07-cube-state]({{ site.github_repo }}/blob/main/specs/v1/07-cube-state.md) | The complete cube state, equality, and the Solved property |
| [08-moves]({{ site.github_repo }}/blob/main/specs/v1/08-moves.md) | The eighteen standard moves |
| [09-algorithms]({{ site.github_repo }}/blob/main/specs/v1/09-algorithms.md) | Sequences of moves |
| [10-transformations]({{ site.github_repo }}/blob/main/specs/v1/10-transformations.md) | Whole-cube rotations |
| [11-api]({{ site.github_repo }}/blob/main/specs/v1/11-api.md) | The minimum capabilities every implementation shall provide |
| [12-compliance]({{ site.github_repo }}/blob/main/specs/v1/12-compliance.md) | What it means to claim conformance |
| [13-notation]({{ site.github_repo }}/blob/main/specs/v1/13-notation.md) | Singmaster notation |
| [14-validity-and-parity]({{ site.github_repo }}/blob/main/specs/v1/14-validity-and-parity.md) | The mathematical validity rules (parity, orientation sums) |

## Supporting documents

| Document | Purpose |
|---|---|
| [glossary]({{ site.github_repo }}/blob/main/specs/v1/glossary.md) | Terminology used throughout the spec |
| [conformance-tests]({{ site.github_repo }}/blob/main/specs/v1/conformance-tests.md) | What a conformance test suite must verify |
| [v1.1/plan.md]({{ site.github_repo }}/blob/main/specs/v1.1/plan.md) | The phase-by-phase implementation roadmap for `core/` |

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
