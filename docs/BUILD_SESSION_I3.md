# Build Session — I3

**Opened:** 2026-08-07  
**Scope:** Per-page fetch/parse of Superpower Wiki summaries into the Absorption catalog  
**Spec:** [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) step I3  
**Depends on:** I1 models/store · I2 discover/index

---

## Delivered

| Artifact | Role |
|----------|------|
| `src/nexus/catalog/pages.py` | MediaWiki `prop=extracts` client, `PageDocument`, slugify |
| `src/nexus/catalog/enrich.py` | Merge summaries into `index.jsonl` + `pages/{slug}.json` |
| `scripts/enrich_absorption_pages.py` | CLI with `--limit`, `--pending-only`, `--names`, `--dry-run` |
| `tests/fixtures/page_extract_*.json` | Offline extract fixtures |
| `tests/catalog_pages_tests.py` | Parse + enrich + preserve walk tests |

## Operator flow

```bash
pip install -e .
# 1) members list
python scripts/discover_absorption.py
# 2) page summaries (rate-limited batches of 10, 0.5s pause)
python scripts/enrich_absorption_pages.py --dry-run
python scripts/enrich_absorption_pages.py --pending-only --limit 50
python -m unittest tests.catalog_smoke_tests tests.catalog_discover_tests tests.catalog_pages_tests -v
```

## Guarantees

- Walk status / policy_tags / schema_draft preserved on enrich
- Subcategory rows skipped
- Missing wiki pages skipped (not written as empty lies)
- No CoreState / simulation imports
- Attribution remains on each catalog row (CC-BY-SA fields from I1)

## Out of scope

| Step | Work |
|------|------|
| I4 | Policy classifier |
| I5 | Walk queue wiring |
| I6 | `write_batch_report` |
| I7 | CI golden batch tests |

## Steward

Enrichment is still **catalog only**. Map ≠ deploy. God is the Source.

**I3 status:** complete in tree — run enrich script after discover to fill summaries.
