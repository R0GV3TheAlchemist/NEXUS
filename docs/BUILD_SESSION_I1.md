# Build Session — I1

**Opened:** 2026-08-07  
**Scope:** `nexus.catalog` models + `data/wiki_catalog/absorption/` layout  
**Spec:** [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) step I1  
**Walk session:** walk-001 remains separate (ability apply unchanged)

---

## Delivered

| Artifact | Role |
|----------|------|
| `src/nexus/catalog/models.py` | `CatalogEntry`, `SchemaDraft`, `WalkRef`, `CatalogCursor`, `POLICY_TAGS` |
| `src/nexus/catalog/paths.py` | Absorption paths + `ensure_absorption_layout` |
| `src/nexus/catalog/store.py` | JSONL index + cursor load/save (no network, no CoreState) |
| `src/nexus/catalog/__init__.py` | Public exports |
| `data/wiki_catalog/absorption/cursor.json` | walk-001 cursor @ Bio-Capacitor #72 |
| `data/wiki_catalog/absorption/index.jsonl` | Empty starter index |
| `data/wiki_catalog/absorption/ATTRIBUTION.md` | CC-BY-SA provenance |
| `tests/catalog_smoke_tests.py` | Round-trip + store smoke |

## Explicitly out of scope (later I-steps)

| Step | Work |
|------|------|
| I2 | Discover Category:Absorption members |
| I3 | Fetch/parse pages + rate limit |
| I4 | Policy classifier |
| I5 | Wire Walk queue to catalog order |
| I6 | `write_batch_report` → BATCH_NN.md |
| I7 | CI golden tests for batches |

## Verify locally

```bash
pip install -e .
python -m unittest tests.catalog_smoke_tests -v
```

## Steward

Catalog ≠ deploy. Map ≠ embody. God is the Source.

**I1 status:** complete in tree (pending your push verification / CI).
