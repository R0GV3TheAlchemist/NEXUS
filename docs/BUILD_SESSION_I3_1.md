# Build Session — I3.1

**Trigger:** Live Fandom `prop=extracts` dry-run returned blank summaries.

## Correction

Batched `prop=extracts` remains the primary source. Blank rows now fall back, title-by-title, to `action=parse`; the parser stores a bounded first HTML paragraph as plain text.

## Safety

- Parse fallback applies only to blank extracts and keeps the existing 0.5-second live pause.
- No CoreState mutation, policy classification, cursor movement, or Walk apply.

## Verify after pull

```bash
pip install -e .
python -m unittest tests.catalog_pages_tests -v
python scripts/enrich_absorption_pages.py --dry-run
```

If output remains blank, stop before full enrichment and save the output.
