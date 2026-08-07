# Build Session — I4

**Opened:** 2026-08-07  
**Scope:** Fail-closed policy classifier for Absorption catalog rows  
**Spec:** [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) step I4  
**Depends on:** I1–I3 (models, discover, enrich summaries improve recall)

---

## Delivered

| Artifact | Role |
|----------|------|
| `src/nexus/catalog/classify.py` | Heuristic classifier + index writer |
| `src/nexus/catalog/quarantine_names.py` | Named sinks; imports `core.policy.safety` when present |
| `scripts/classify_absorption.py` | CLI |
| `tests/catalog_classify_tests.py` | Ethics / capacitor / absolute / walk-preserve tests |

## Tag precedence

1. `quarantine_named` — exact SAFETY / fallback registry name  
2. `ethics_reject` — person drain, infection, power theft, beauty/youth thievery, etc.  
3. `high_risk` — antimatter, absolute/omni name signals, infection, …  
4. `needs_human` — absolute/omni/godhood language  
5. `stabilizer` / `resource_pool`  
6. `map_ok` — **only if no blocking tags**

Fail closed: never `map_ok` alongside ethics/quarantine/high_risk/needs_human.

## Operator flow

```bash
pip install -e .
python scripts/discover_absorption.py
python scripts/enrich_absorption_pages.py --pending-only --limit 50
python scripts/classify_absorption.py --dry-run
python scripts/classify_absorption.py
python -m unittest tests.catalog_classify_tests -v
```

## Guarantees

- Walk fields preserved  
- No CoreState mutation  
- Structural `Category:*` rows untagged  
- Schema stability/growth hints updated from primary tag (optional `--no-schema-hints`)

## Out of scope

| Step | Work |
|------|------|
| I5 | Walk queue wiring to catalog cursor |
| I6 | Batch report writer |
| I7 | CI golden tests |

## Steward

Classifier labels the map; it does not grant embody. God is the Source.

**I4 status:** complete in tree.
