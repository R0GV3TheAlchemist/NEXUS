# Project Memory Workflow

NEXUS keeps durable memory in the repository so work does not depend on chat history.

## Where things live

| Artifact | Purpose | When to update |
|----------|---------|----------------|
| `DECISIONS.md` | Architecture decisions + short rationale | Any change to structure, contracts, simulation boundary, or CLI guarantees |
| `CHANGELOG.md` | Notable shipped changes by version | After meaningful code or docs land on `main` |
| `STATUS.md` | Current verified state and next steps | After completing a tracking issue or major milestone |
| GitHub Issues | Task checklists and progress notes | During implementation; close only when code + docs agree |

## Decision entry template

Append under **Current Decisions** in `DECISIONS.md`:

```markdown
### N. Short title (YYYY-MM-DD)

**Decision:** One sentence.

**Rationale:** Bullet list of why.

**Consequences:** What must / must not change next.
```

Keep entries short. Prefer one decision per architectural shift.

## Changelog entry template

Under `[Unreleased]` in `CHANGELOG.md`, use:

- **Added** — new capability or doc
- **Changed** — behavior or boundary shift
- **Fixed** — bug fix
- **Removed** — deleted surface
- **Decisions** — pointer to `DECISIONS.md` section if relevant

When releasing, move `[Unreleased]` items into a dated version section.

## Rules of thumb

1. If the architecture changed, update `DECISIONS.md` in the same change set.
2. If users or contributors would notice the change, update `CHANGELOG.md`.
3. If “where are we?” would be answered differently, update `STATUS.md`.
4. Close tracking issues only when tests and docs match the code.

## Related

- `docs/CI.md` — continuous integration
- `docs/INDEX.md` — documentation map
- `CONTRIBUTING.md` — contribution rules
