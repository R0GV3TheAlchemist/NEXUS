# NEXUS Ability Schema

## Purpose

The ability schema defines the canonical structure for a NEXUS ability. An ability is the smallest formally described unit of behavior in the system. It must be explicit, testable, and reproducible.

## Required Fields

1. `name`: A stable identifier for the ability.
2. `description`: A concise statement of the ability's purpose.
3. `domain`: The subject domain to which the ability belongs.
4. `inputs`: The declared inputs, including type and constraints.
5. `outputs`: The declared outputs, including type and constraints.
6. `dependencies`: External or internal requirements needed for execution.
7. `invariants`: Conditions that must remain true during execution.
8. `failure_modes`: Expected failure states and their handling.
9. `version`: A semantic version identifying the schema or ability revision.
10. `traceability`: References to source data, simulation data, or design rationale.

## Execution Context

Each ability should define the context in which it executes. The execution context includes substrate assumptions, policy constraints, and any bounded environmental conditions that affect behavior.

## Validation Rules

- The schema must be machine-readable wherever possible.
- Fields must be stable and versioned.
- Inputs and outputs must be deterministic where determinism is intended.
- A change to contract structure should be treated as an architectural event, not a casual edit.

## Relationship to GAIA

In the GAIA layer, abilities are treated as contract-bound units that can participate in higher-order orchestration, policy control, accounting, and conformance validation.

## Relationship to Super-Simulation

The ability schema is informed by the super-simulation model. Simulation-derived evidence may be used to refine the schema, but the schema itself remains a formal contract rather than a freeform narrative artifact.

## Authorship

Copyright (c) 2026 Kyle Alexander Steen.
