# Catalog CI

**I7** — continuous checks for the Absorption catalog pipeline (offline only).

## Workflow

[`.github/workflows/catalog.yml`](../.github/workflows/catalog.yml) runs on push to `main` and every pull request.

| Check | What |
|-------|------|
| `catalog_*_tests` | I1–I6 unit tests |
| `catalog_golden_tests` | Batch 7 fixed ledger → required MD sections |
| `catalog_pipeline_smoke_tests` | classify → queue → batch write without network |
| import smoke | public `nexus.catalog` surface |

## Local equivalent

```bash
pip install -e .
python -m unittest \
  tests.catalog_smoke_tests \
  tests.catalog_discover_tests \
  tests.catalog_pages_tests \
  tests.catalog_classify_tests \
  tests.catalog_walk_queue_tests \
  tests.catalog_batch_report_tests \
  tests.catalog_golden_tests \
  tests.catalog_pipeline_smoke_tests \
  -v
```

## Guarantees

- **No Fandom/network** in CI (discover/enrich live scripts are operator-only)
- Fail-closed classifier still forbids `map_ok` on ethics samples in unit tests
- Batch writer always emits required section headings for a full decade ledger

## Related

- [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md)
- [walks/BATCH_REPORT_SPEC.md](./walks/BATCH_REPORT_SPEC.md)
- [BUILD_SESSION_I7.md](./BUILD_SESSION_I7.md)
