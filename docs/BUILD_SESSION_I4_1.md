# Build Session — I4.1

**Trigger:** Classification dry-run labeled mostly unenriched rows `map_ok` from names alone.

## Correction

An empty source summary now produces `needs_human`; it cannot produce `map_ok`. Higher-priority `quarantine_named`, `ethics_reject`, and `high_risk` tags still win.

## Verify

```bash
pip install -e .
python -m unittest tests.catalog_classify_tests -v
python scripts/classify_absorption.py --dry-run --show 25
```

No network, CoreState mutation, cursor advance, or Walk apply.
