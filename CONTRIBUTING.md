# Contributing to NEXUS

## Purpose

Contributions should preserve the formal, academic, and stable nature of the project. Changes should be explicit, traceable, and aligned with the roadmap.

## Before You Start

Read the documentation in this order:

1. `PROJECT_CHARTER.md`
2. `FOUNDATIONS.md`
3. `ROADMAP.md`
4. `MODULE_SKELETONS.md`
5. `ABILITY_SCHEMA.md`
6. `docs/MEMORY.md` — decision and changelog workflow
7. `STATUS.md` / `DECISIONS.md` / `CHANGELOG.md` — current memory

## Contribution Rules

- Keep changes small and well-scoped.
- Preserve authorship and citation notices.
- Update documentation when the architecture changes.
- Prefer stable interfaces over ad hoc edits.
- Use clear commit messages and explicit descriptions.

## Decision and changelog

When a change affects architecture, contracts, CLI guarantees, or the simulation boundary:

1. Add or update an entry in `DECISIONS.md` (see `docs/MEMORY.md`).
2. Note the change under `[Unreleased]` in `CHANGELOG.md`.
3. Adjust `STATUS.md` if the verified state or next steps changed.

## Review Standard

A contribution should explain what changed, why it changed, and how it affects the current architecture. If the change affects contracts or schemas, it should include a corresponding documentation update.

## Authorship

Copyright (c) 2026 Kyle Alexander Steen.
