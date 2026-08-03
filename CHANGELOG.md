# Changelog

All notable changes to NEXUS are recorded here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)-inspired.
Versioning aims toward [SemVer](https://semver.org/) once the foundation stabilizes.
Architecture decisions live in `DECISIONS.md`; this file records *what shipped*.

## [Unreleased]

### Added

- (none pending)

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
