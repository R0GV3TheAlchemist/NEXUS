# NEXUS Status

## Current State

NEXUS is in foundation-correction mode. The immediate goal is to keep the project stable, boring, and testable while the architecture is clarified and aligned across docs, code, and tests.

## Verified Progress

- The CLI import error was fixed.
- The CLI smoke tests now exercise `build_parser()` and `main(argv=None)`.
- Tracking issues #1–#7 manage documentation, simulation, and governance work.
- **Canonical simulation package decided:** `src/nexus/simulation` (`NEXUSEngine`).
- `src/nexus/sim` is documented as a compatibility shim (still used by `nexus.app.entrypoint`).
- **Simulation modules normalized (Issue #3):** `CoreState` is the canonical state contract via `nexus.simulation.state`; `NEXUSEngine` is the sole ability-application engine; shadowed `core/policy.py` removed.

## Architectural Decisions in Force

- One canonical simulation path: `src/nexus/simulation`.
- `src/nexus/sim` is a temporary compatibility shim, not a second architecture.
- `CoreState` is the single Primordial Walk state vector (seven variables).
- CLI must remain import-safe and testable without the full app stack.

## Open Architectural Questions

- When should `NexusApp` migrate from `SimulationEngine` to `NEXUSEngine`?
- What is the minimal Super-Simulation entrypoint surface? (Issue #4)
- Which remaining parts of the system are conceptual vs scaffolded vs operational?

## Working Principles

- Keep the system boring before making it powerful.
- Prefer explicit contracts over implicit behavior.
- Update docs whenever code changes the architecture.
- Keep one source of truth for each major concept.
- Record decisions so the project can retain memory beyond chat.

## Planned Next Steps

1. ~~Consolidate simulation namespaces (choose canonical path).~~ **Done** (Issue #2)
2. ~~Read and normalize simulation engine/state modules.~~ **Done** (Issue #3)
3. Add a minimal Super-Simulation entrypoint (Issue #4).
4. Add a simulation smoke test (Issue #5).
5. Extend CI to protect the CLI and simulation entrypoints (Issue #6).
6. Keep the decision/changelog workflow current (Issue #7).

## Notes

This repository is intended to evolve through disciplined layers: core system, meta-system, super-system, and higher-order symbolic layers, while remaining grounded in reproducible, testable engineering.
