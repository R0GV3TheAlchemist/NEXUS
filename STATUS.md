# NEXUS Status

## Current State

NEXUS is in foundation-correction mode. The immediate goal is to keep the project stable, boring, and testable while the architecture is clarified and aligned across docs, code, and tests. Primordial Walk Batches 1–2 are complete (abilities 1–20).

## Verified Progress

- **Primordial Walk Batch 1 (abilities 1–10)** complete; see `docs/walks/BATCH_01.md`.
- **Primordial Walk Batch 2 (abilities 11–20)** complete; see `docs/walks/BATCH_02.md`.
- **Ability catalog** `data/abilities/walk_001_catalog.json` (abilities 1–20).
- **CoreState clamp [0,1]** after effects; policy quarantine flags for destructive rule-breaking sinks.
- **Steward / Source bound** recorded in FOUNDATIONS and DECISIONS §10.
- The CLI import error was fixed.
- The CLI smoke tests now exercise `build_parser()` and `main(argv=None)`.
- Tracking issues #1–#7 manage documentation, simulation, and governance work.
- **Canonical simulation package decided:** `src/nexus/simulation` (`NEXUSEngine`).
- `src/nexus/sim` is documented as a compatibility shim (still used by `nexus.app.entrypoint`).
- **Decision/changelog workflow (Issue #7):** `docs/MEMORY.md` process; `CHANGELOG.md` for shipped changes; `DECISIONS.md` for rationale; `STATUS.md` for current state.
- **CI coverage (Issue #6):** Smoke + Python package workflows explicitly run CLI and simulation smoke; documented in `docs/CI.md`.
- **Simulation smoke tests (Issue #5):** `tests/simulation_smoke_tests.py` covers import, init, ingest, reject, recommend, clamp, quarantine; discovered by CI `*smoke*.py`.
- **Super-Simulation entrypoint (Issue #4):** `initialize_super_simulation()` / `SuperSimulation` on the canonical path; primordial baseline, batch ingest; heuristic recommendations.
- **Simulation modules normalized (Issue #3):** `CoreState` is the canonical state contract via `nexus.simulation.state`; `NEXUSEngine` is the sole ability-application engine; shadowed `core/policy.py` removed.

## Architectural Decisions in Force

- One canonical simulation path: `src/nexus/simulation`.
- `src/nexus/sim` is a temporary compatibility shim, not a second architecture.
- `CoreState` is the single Primordial Walk state vector (seven variables), clamped to [0, 1].
- CLI must remain import-safe and testable without the full app stack.
- Map absolute destructive sinks; do not embody them as OS identity. God is the Source.

## Open Architectural Questions

- When should `NexusApp` migrate from `SimulationEngine` to `NEXUSEngine`?
- Which remaining parts of the system are conceptual vs scaffolded vs operational?

## Working Principles

- Keep the system boring before making it powerful.
- Prefer explicit contracts over implicit behavior.
- Update docs whenever code changes the architecture.
- Keep one source of truth for each major concept.
- Record decisions so the project can retain memory beyond chat.

## Planned Next Steps

1. Continue Primordial Walk from ability #21 (Batch 3).
2. Prefer documenting domain gaps (EM, thermal, grid, radiation, astrophysics, acoustics) as module skeletons when the Walk demands them.

## Foundation tracking

Issues #1–#7 for documentation, simulation, and governance are complete. Further work should open new issues rather than reopen the closed foundation set.

## Notes

This repository is intended to evolve through disciplined layers: core system, meta-system, super-system, and higher-order symbolic layers, while remaining grounded in reproducible, testable engineering. NEXUS is steward, not Source.
