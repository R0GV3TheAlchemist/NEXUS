# NEXUS Decisions

## Purpose

This document records the architectural decisions that keep NEXUS stable, explainable, and easy to extend. It exists so the project can retain memory beyond chat and so implementation work stays aligned with the documented plan.

## Current Decisions

### 1. Foundation-first development

NEXUS will remain boring, stable, and testable until the core contracts are settled. New symbolic or higher-order ideas must not weaken the execution path.

### 2. Documentation must match code

Any change to architecture, CLI behavior, or simulation structure must be reflected in repository docs. Documentation is part of the system, not a separate artifact.

### 3. One canonical simulation path

The repository currently contains simulation-related code in both `src/nexus/sim` and `src/nexus/simulation`. One path should become canonical, and the other should be clearly treated as a compatibility shim or removed after migration.

### 4. Preserve the CLI contract

The CLI must keep supporting import-safe startup, `build_parser()`, and `main(argv=None)` behavior so tests can exercise it without relying on the app stack.

### 5. Track progress publicly

A status file and at least one tracking issue should remain current so the project can be resumed safely and reviewed without reconstructing context from chat.

## Required Build Work

The documentation implies several build tasks that still need to exist in code:

1. A canonical simulation package boundary.
2. A minimal Super-Simulation entrypoint.
3. A smoke test for simulation initialization.
4. CI coverage for CLI and simulation startup.
5. A structured changelog or status update workflow.
6. A single, clearly documented architecture path for future modules.

## Quality Standard

Work should be evaluated by correctness, clarity, reproducibility, and architectural fit. If a change cannot be explained in docs and validated by tests, it is not complete.

## Future Updates

Add new decisions here whenever the repo changes direction. Keep entries short, specific, and tied to concrete implementation outcomes.
