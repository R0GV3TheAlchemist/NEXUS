# Build Session — I2

**Opened:** 2026-08-07  
**Scope:** Discover Category:Absorption members (paginated MediaWiki API)  
**Spec:** [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) step I2  
**Depends on:** I1 (`nexus.catalog` models + store)

---

## Delivered

| Artifact | Role |
|----------|------|
| `src/nexus/catalog/discover.py` | `categorymembers` URL builder, parser, paginated discover |
| `src/nexus/catalog/sync.py` | Merge into `index.jsonl`, preserve walk/policy |
| `scripts/discover_absorption.py` | Operator CLI (live sync or `--dry-run`) |
| `tests/fixtures/absorption_categorymembers_*.json` | Offline API fixtures |
| `tests/catalog_discover_tests.py` | Pagination + merge preservation tests |

## Live sync (on your machine)

CI stays offline. Populate the real index from your network:

```bash
pip install -e .
python scripts/discover_absorption.py --dry-run
python scripts/discover_absorption.py
python -m unittest tests.catalog_smoke_tests tests.catalog_discover_tests -v
```

Default pause between API pages: **0.5s**. User-Agent identifies NEXUS research index.

## Explicitly out of scope

| Step | Work |
|------|------|
| I3 | Per-page fetch/parse summaries |
| I4 | Policy classifier |
| I5 | Walk queue wiring |
| I6 | Batch report writer |
| I7 | CI golden batch tests |

## Steward

Discovery fills the **catalog only**. Catalog ≠ deploy. God is the Source.

**I2 status:** complete in tree — run `scripts/discover_absorption.py` to fill `index.jsonl` from live wiki.
