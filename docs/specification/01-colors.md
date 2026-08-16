---
layout: page
title: Colors · Specification
---

<p><a class="spec-crumb" href="{{ '/specification.html' | relative_url }}">&larr; Specification index</a></p>

# Colors

## Purpose

This document defines the color model used throughout the cube specification.

Colors are immutable identifiers used to define piece identities and cube orientation.

This specification defines colors conceptually and does not prescribe visual representations.

---

## Defined Colors

The specification defines exactly six colors.

```
WHITE
YELLOW
GREEN
BLUE
RED
ORANGE
```

No additional colors are permitted.

---

## Identity

Each color has a unique identity.

Implementations may internally represent colors using integers, enums, strings, UUIDs, or other mechanisms.

The representation is implementation-defined.

---

## Metadata

Implementations may associate optional metadata with colors.

Examples include

- Display name
- RGB values
- Hexadecimal color values
- UI textures
- ANSI terminal colors

This metadata is outside the scope of this specification.

---

## Equality

Two colors are equal if and only if they represent the same defined color.

---

## Opposite Colors

The following colors are opposites.

| Color | Opposite |
|---------|----------|
| WHITE | YELLOW |
| GREEN | BLUE |
| RED | ORANGE |

Opposite relationships are immutable.

These relationships are used when validating piece legality and cube orientation.

---

## Description

Every color should provide a human-readable description.

Example

```
White
```

The exact formatting is implementation-defined.

<nav class="spec-pager">
  <span></span>
  <a class="spec-pager__next" href="{{ '/specification/02-pieces.html' | relative_url }}">Pieces &rarr;</a>
</nav>
