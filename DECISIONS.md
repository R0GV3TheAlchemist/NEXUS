# NEXUS Decisions

## Purpose

This document records the architectural decisions that keep NEXUS stable, explainable, and easy to extend. It exists so the project can retain memory beyond chat and so implementation work stays aligned with the documented plan.

## Current Decisions

### 1. Foundation-first development

NEXUS will remain boring, stable, and testable until the core contracts are settled. New symbolic or higher-order ideas must not weaken the execution path.

### 2. Documentation must match code

Any change to architecture, CLI behavior, or simulation structure must be reflected in repository docs. Documentation is part of the system, not a separate artifact.

### 3. Canonical simulation path: `src/nexus/simulation`

**Decision (2026-08-03):** `src/nexus/simulation` is the canonical simulation package.

**Rationale:**

- `NEXUSEngine` already integrates `CoreState` (the seven Primordial Walk variables), `AbilitySchema`, policy acceptance, subject adaptation, ledger accounting, and run persistence.
- That integration matches the Super-Simulation / Primordial Walk direction described in the project charter and ability schema.
- `src/nexus/sim` is a lighter, generic step/ledger helper used only by `nexus.app.entrypoint`. It does not own the core state model.

**Non-canonical path:**

- `src/nexus/sim` is retained as a **compatibility shim** for `NexusApp` until a later migration moves that consumer onto the canonical package.
- New simulation features, entrypoints, and smoke tests must target `nexus.simulation` only.
- Do not add new public APIs under `nexus.sim`.

**Migration note:** Issue #3 (normalize engine/state modules) and Issue #4 (minimal Super-Simulation entrypoint) continue from this boundary. Removal of the shim is deferred until the app entrypoint no longer depends on it.

### 4. Preserve the CLI contract

The CLI must keep supporting import-safe startup, `build_parser()`, and `main(argv=None)` behavior so tests can exercise it without relying on the app stack.

### 5. Track progress publicly

A status file and at least one tracking issue should remain current so the project can be resumed safely and reviewed without reconstructing context from chat.

## Required Build Work

The documentation implies several build tasks that still need to exist in code:

1. ~~A canonical simulation package boundary.~~ (decided: `src/nexus/simulation`)
2. Normalize simulation engine/state modules under the canonical path (Issue #3).
3. A minimal Super-Simulation entrypoint (Issue #4).
4. A smoke test for simulation initialization (Issue #5).
5. CI coverage for CLI and simulation startup (Issue #6).
6. A structured changelog or status update workflow (Issue #7).

## Quality Standard

Work should be evaluated by correctness, clarity, reproducibility, and architectural fit. If a change cannot be explained in docs and validated by tests, it is not complete.

## Future Updates

Add new decisions here whenever the repo changes direction. Keep entries short, specific, and tied to concrete implementation outcomes.
