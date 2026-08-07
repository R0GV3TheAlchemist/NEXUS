# Changelog

All notable changes to NEXUS are recorded here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)-inspired.
Versioning aims toward [SemVer](https://semver.org/) once the foundation stabilizes.
Architecture decisions live in `DECISIONS.md`; this file records *what shipped*.

## [Unreleased]

### Added

- CoreState clamp to [0, 1] after ability effects.
- Policy quarantine / embody flags for rule_breaking + destructive_oriented abilities.
- Primordial Walk Batch 1 report (`docs/walks/BATCH_01.md`).
- Steward / Source bound in FOUNDATIONS and DECISIONS §10.
- Primordial Walk Batch 2 report (`docs/walks/BATCH_02.md`).
- Ability catalog for walk-001 (`data/abilities/walk_001_catalog.json`, abilities 1–20).
- Protective measures module `nexus.core.policy.safety` + `docs/SAFETY.md` (named quarantine for 15 absolute sinks).

## [0.1.0] — 2026-08-03

### Added

- Canonical simulation package `nexus.simulation` (`NEXUSEngine`, `CoreState`).
- Super-Simulation entrypoint: `initialize_super_simulation` / `SuperSimulation`.
- Primordial baseline state and ability batch ingest surface.
- Simulation smoke tests (`tests/simulation_smoke_tests.py`).
- CI workflows: explicit CLI + simulation smoke; full package suite (`docs/CI.md`).
- Project memory docs: `STATUS.md`, `DECISIONS.md`, this changelog.

### Changed

- `nexus.sim` retained as compatibility shim for `NexusApp` only.
- Core policy assessment consolidated under `nexus.core.policy` package.

### Removed

- Shadowed `src/nexus/core/policy.py` module (unreachable under the package).

### Decisions

See `DECISIONS.md` §§3–8 (canonical path, normalization, Super-Simulation, CI).
