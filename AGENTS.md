# CubeForge Development Guide for AI Agents

This repository implements **CubeForge**, a specification-driven Rubik's Cube
engine.

The specification is the source of truth.

Never implement behaviour that contradicts the specification.

---

# Reading Order

Before making ANY code changes:

1. Read `plan.md`.
2. Read the specification files relevant to the current phase.
3. Inspect the current implementation.
4. Inspect existing tests.

Never skip these steps.

---

# Development Workflow

Work exactly ONE phase at a time.

Do not begin the next phase until the user explicitly approves.

Each phase follows this workflow.

## Step 1 — Understand

Read the relevant specification(s).

Quote every bullet under the **Compliance** section.

Do not paraphrase.

Present those bullets to the user before implementation.

---

## Step 2 — Plan

Explain:

- files that will change
- why they change
- implementation approach
- possible compatibility concerns

If a public API changes, list every affected call site before editing.

Search the repository first.

Never modify signatures blindly.

---

## Step 3 — Wait

Do not edit code until the implementation plan has been approved.

---

## Step 4 — Implement

Implement only what belongs to the current phase.

Avoid unrelated refactoring.

Preserve backwards compatibility unless the roadmap explicitly requires a
breaking change.

Keep changes as small as practical.

---

## Step 5 — Tests

Tests are part of implementation.

Whenever plan.md lists:

- Files to add (tests)
- Definition of Done

Treat them as mandatory acceptance criteria.

Never postpone tests until later.

---

## Step 6 — Validation

Run the complete test suite.

Report:

- number of passing tests
- failures
- regressions
- warnings

Do not claim tests passed unless they were actually executed.

---

## Step 7 — Verify Against the Spec

Re-read the relevant specification.

Walk through every Compliance bullet.

State exactly how the implementation satisfies it.

---

## Step 8 — Commit

Create one commit per phase.

Commit format:

<version>: <phase description>

Example:

v0.7: integrate CubeOrientation into CubeState

---

# Ambiguity Policy

If the specification is ambiguous:

STOP.

Do not guess.

Do not invent behaviour.

Ask the user.

---

# Refactoring Rules

Avoid unnecessary cleanup.

Avoid formatting-only commits.

Avoid renaming files without reason.

Avoid moving code unless required.

---

# Public API

Never modify public APIs outside the current phase.

Never modify companion projects unless explicitly requested.

Companion projects include:

- CubeForge Web
- CubeForge CLI
- CubeForge MCP
- Java implementation
- Rust implementation
- C# implementation

---

# Quality Standards

Prefer:

- immutable data
- explicit behaviour
- descriptive names
- small functions
- comprehensive tests

Avoid:

- duplicated logic
- hidden state
- magic constants
- speculative abstractions

---

# Repository Search Rules

Before changing:

- constructor signatures
- dataclasses
- enums
- shared models

search the entire repository for:

- constructor usage
- imports
- subclasses
- serialization
- tests

List affected files before editing.

---

# General Rule

The specification has higher priority than existing implementation.

The roadmap has higher priority than convenience.

Correctness has higher priority than optimization.