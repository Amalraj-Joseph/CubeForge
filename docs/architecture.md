---
layout: page
title: Architecture
---

# Architecture

This is the mental model behind CubeForge, built up in the order each
concept depends on the last. The formal, precise version of every rule
mentioned here lives in [the specification](specification.html) - this
page is the tour, not the contract.

## Colors

Six immutable colors: White, Yellow, Green, Blue, Red, Orange. They come
in three fixed opposite pairs (White/Yellow, Green/Blue, Red/Orange) -
no piece and no cube orientation can ever put two opposite colors on the
same physical thing. That single rule underpins almost every other
invariant in the engine.

{% include cube-diagram.html
   up="w,w,w,w,w,w,w,w,w"
   front="g,g,g,g,g,g,g,g,g"
   right="r,r,r,r,r,r,r,r,r"
   px="170" static="true"
   caption="White/Green/Red visible here - Yellow, Blue, and Orange sit opposite them, out of view" %}

## Pieces

A standard cube has exactly twenty-six physical pieces: six **centers**
(one color each), twelve **edges** (two colors each), eight **corners**
(three colors each). A piece's identity is its unordered set of colors -
`Piece(WHITE, GREEN, RED)` always refers to the same physical cubie,
regardless of where it currently sits or how it's twisted. Position and
orientation are explicitly *not* part of identity.

{% include cube-diagram.html
   up="g,g,g,w,w,w,w,w,r"
   front="o,r,r,g,g,w,g,g,r"
   right="w,g,b,r,r,r,y,r,r"
   px="170" static="true"
   caption="Cube.canonical().apply_algorithm(&quot;R U R' U' R U R' U'&quot;) - same 26 pieces, different positions and orientations" %}

## Positions

Positions are the twenty-six fixed slots a piece can occupy - `UF`,
`DFL`, `UFR`, and so on, named the same way as the pieces that fit into
them (an edge position takes an edge, a corner position takes a corner).
A position never moves; pieces move *between* positions.

## Piece State

A `PieceState` is one piece's current situation: which `Piece`, which
`Position`, and which orientation (encoded as an integer - 0/1 for a
flipped edge, 0/1/2 for a twisted corner). Twenty-six of these,
one per piece, are half of what a full cube state needs.

## Cube Orientation

The other half is knowing which way you're holding the cube - `CubeOrientation`
records which color currently faces "up" and which faces "front" (the
other four directions follow automatically). There are exactly
twenty-four legal orientations - one per way you can physically hold a
cube with a fixed handedness. This is *not* the same thing as scrambling
the cube: rotating your grip doesn't move a single piece relative to any
other.

## Cube State

`CubeState = CubeOrientation + 26 PieceStates`. That's the complete,
observable state of a cube at any instant, and it's what every operation
in the engine reads and produces. Two cube states are equal exactly when
their orientation and every corresponding piece state are equal.

Constructing a `CubeState` enforces every invariant a real cube has, in
one place, at the moment of construction:

- exactly one of each of the twenty-six pieces, each in a distinct legal
  position
- edge orientation values summing to an even number
- corner orientation values summing to a multiple of three
- edge and corner permutation parity in agreement
- center placement consistent with the declared orientation

A state that violates any of these describes a cube that could never
exist physically - twist one corner on a real cube and you'll find you
can't do it without moving something else too. `CubeState` refuses to
represent that possibility rather than let you build it and find out
later.

## Solved

A cube is solved when every visible sticker matches its own face's
center - which, because orientation is independent of piece placement,
means there are exactly twenty-four solved states (the canonical one,
and the same physical arrangement held twenty-three other ways).
`CubeAnalyzer`/`Cube.solved` check this relative to the cube's *own*
current orientation, never a hardcoded assumption about which way is
"up."

## Moves

The eighteen standard face turns (`U`, `D`, `F`, `B`, `L`, `R`, each with
a `2` and `'` variant). A move rotates one layer, updating the position
and orientation of every piece in that layer, and leaves `CubeOrientation`
completely untouched - a move never changes which way you're holding the
cube.

## Algorithms

An ordered sequence of moves. `Algorithm.parse("R U R' U'")` reads
Singmaster notation; `.notation` writes it back out. Algorithms compose
(`a.compose(b)`) and invert (`a.inverse`) as you'd expect from a sequence
of reversible operations.

## Cube Transformations

Where a move turns a layer, a `CubeTransformation` turns the *entire*
cube - `ROTATE_UP`, `ROTATE_LEFT`, `ROLL_CLOCKWISE`, and their inverses.
These change `CubeOrientation` and rewrite every piece's position/orientation
to match, but never alter which piece sits next to which - solved stays
solved, scrambled stays scrambled, just viewed from a different angle.

## Validation

Everything above is enforced by construction, which means the standalone
validators (`PieceValidator`, `CubeOrientationValidator`, `CubeStateValidator`)
mostly exist for one specific job: checking data that arrived from
*outside* the engine - deserialized from JSON, say - before or instead
of trusting it blindly.

## Putting it together

```python
from cube import Cube, Algorithm, ROTATE_UP

cube = Cube.canonical()
cube = cube.apply_algorithm(Algorithm.parse("R U R' U'"))
cube = cube.apply_transformation(ROTATE_UP)

cube.solved                # False - the algorithm scrambled it
cube.misplaced_pieces()    # exactly which PieceStates are out of place
cube.to_json()             # portable, versioned wire format
```

Every one of those calls returns a *new* `Cube` - nothing here is
mutable. That's deliberate: a `Cube` is a value, like the number 5. You
don't mutate 5 into 6; you compute a new value.
