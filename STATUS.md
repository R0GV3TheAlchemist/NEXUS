# NEXUS Status

## Current State

NEXUS is in foundation-correction mode. The immediate goal is to keep the project stable, boring, and testable while the architecture is clarified and aligned across docs, code, and tests.

## Verified Progress

- The CLI import error was fixed.
- The CLI smoke tests now exercise `build_parser()` and `main(argv=None)`.
- A tracking issue exists to manage the remaining documentation, simulation, and governance work.
- Simulation-related scaffolding exists in both `src/nexus/sim` and `src/nexus/simulation`.

## Open Architectural Questions

- Which simulation namespace is canonical?
- Which modules are implementation and which are compatibility shims?
- What is the minimal Super-Simulation entrypoint?
- Which parts of the system are conceptual, scaffolded, or operational?

## Working Principles

- Keep the system boring before making it powerful.
- Prefer explicit contracts over implicit behavior.
- Update docs whenever code changes the architecture.
- Keep one source of truth for each major concept.
- Record decisions so the project can retain memory beyond chat.

## Planned Next Steps

1. Consolidate simulation namespaces.
2. Read and normalize simulation engine/state modules.
3. Add a minimal Super-Simulation smoke test.
4. Add a decision log for major architectural choices.
5. Extend CI to protect the CLI and simulation entrypoints.

## Notes

This repository is intended to evolve through disciplined layers: core system, meta-system, super-system, and higher-order symbolic layers, while remaining grounded in reproducible, testable engineering.
