# Local pull checklist (Git Bash)

Use this after the I1–I7 catalog work lands on `main`.

## 1. Update the clone

```bash
cd /path/to/NEXUS
git fetch origin
git status
git pull origin main
```

If you have local commits, prefer:

```bash
git pull --rebase origin main
```

## 2. Reinstall editable package

```bash
python -m pip install -U pip
pip install -e .
```

## 3. Run catalog tests (offline)

```bash
python -m unittest \
  tests.catalog_smoke_tests \
  tests.catalog_paths_tests \
  tests.catalog_discover_tests \
  tests.catalog_pages_tests \
  tests.catalog_classify_tests \
  tests.catalog_walk_queue_tests \
  tests.catalog_batch_report_tests \
  tests.catalog_golden_tests \
  tests.catalog_pipeline_smoke_tests \
  -v
```

## 4. Optional live catalog fill (network)

```bash
python scripts/discover_absorption.py --dry-run
python scripts/discover_absorption.py
python scripts/enrich_absorption_pages.py --pending-only --limit 20
python scripts/classify_absorption.py --dry-run
python scripts/walk_queue.py cursor
python scripts/walk_queue.py peek
```

## 5. Ops playbook

See [WALK_VS_CATALOG_OPS.md](./WALK_VS_CATALOG_OPS.md).

## If something fails

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: nexus.catalog` | `pip install -e .` from repo root |
| Empty index / wrong data path | Run from repo root; check `data/wiki_catalog/absorption/` |
| Tests fail on URL encoding | Ensure you have the latest `fix(catalog): harden…` commit |
| Merge conflicts in `index.jsonl` | Keep remote structure; re-run `discover_absorption.py` |

## Steward

Pull updates the lamp factory. Walk apply stays console-gated. God is the Source.
