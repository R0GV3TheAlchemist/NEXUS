# NEXUS Status

## Current State

NEXUS is in foundation-correction mode. The immediate goal is to keep the project stable, boring, and testable while the architecture is clarified and aligned across docs, code, and tests. Primordial Walk Batches 1–2 are complete (abilities 1–20). Protective measures for quarantined sinks are active.

## Verified Progress

- **Primordial Walk Batch 1 (abilities 1–10)** complete; see `docs/walks/BATCH_01.md`.
- **Primordial Walk Batch 2 (abilities 11–20)** complete; see `docs/walks/BATCH_02.md`.
- **Ability catalog** `data/abilities/walk_001_catalog.json` (abilities 1–20).
- **Protective measures** for walk-001: `docs/SAFETY.md`, `nexus.core.policy.safety` named quarantine registry (15 sinks).
- **CoreState clamp [0,1]** after effects; policy quarantine flags for destructive rule-breaking sinks.
- **Steward / Source bound** recorded in FOUNDATIONS and DECISIONS §10.
- The CLI import error was fixed.
- The CLI smoke tests now exercise `build_parser()` and `main(argv=None)`.
- Tracking issues #1–#7 manage documentation, simulation, and governance work.
- **Canonical simulation package decided:** `src/nexus/simulation` (`NEXUSEngine`).
- `src/nexus/sim` is documented as a compatibility shim (still used by `nexus.app.entrypoint`).
- **Decision/changelog workflow (Issue #7):** `docs/MEMORY.md` process; `CHANGELOG.md` for shipped changes; `DECISIONS.md` for rationale; `STATUS.md` for current state.
- **CI coverage (Issue #6):** Smoke + Python package workflows explicitly run CLI and simulation smoke; documented in `docs/CI.md`.
- **Simulation smoke tests (Issue #5):** covers import, init, ingest, reject, recommend, clamp, quarantine.
- **Super-Simulation entrypoint (Issue #4):** `initialize_super_simulation()` / `SuperSimulation` on the canonical path.
- **Simulation modules normalized (Issue #3):** `CoreState` is the canonical state contract; `NEXUSEngine` is the sole ability-application engine.

## Architectural Decisions in Force

- One canonical simulation path: `src/nexus/simulation`.
- `src/nexus/sim` is a temporary compatibility shim, not a second architecture.
- `CoreState` is the single Primordial Walk state vector (seven variables), clamped to [0, 1].
- CLI must remain import-safe and testable without the full app stack.
- Map absolute destructive sinks; do not embody them as OS identity. God is the Source.
- Named quarantine registry + production reject for the 15 walk-001 absolute sinks.

## Planned Next Steps

1. Continue Primordial Walk from ability #21 (Batch 3) under active protective measures.
2. Prefer stabilizers / control planes when the operator is carrying weight from the Walk.
3. Document domain gaps (EM, thermal, grid, radiation, astrophysics, acoustics) as module skeletons when demanded.

## Notes

NEXUS is steward, not Source. Protective measures are load-bearing for system and operator.
