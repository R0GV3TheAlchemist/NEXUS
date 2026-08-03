# Continuous Integration

NEXUS uses two GitHub Actions workflows to keep the CLI contract and Super-Simulation entrypoint stable.

## Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| **Smoke** | `.github/workflows/smoke.yml` | Fast gate: `python -m nexus --help`, CLI smoke tests, simulation smoke tests |
| **Python package** | `.github/workflows/python-package.yml` | Editable install, full `unittest` discovery, CLI help, simulation import check |

Both run on:

- Push to `main`
- Every pull request

## What must stay green

1. **CLI import-safe startup** — `python -m nexus --help` exits successfully without the full app stack.
2. **CLI smoke** — `tests/cli_smoke_tests.py` (`build_parser` / `main` behavior).
3. **Simulation smoke** — `tests/simulation_smoke_tests.py` (canonical package import, `initialize_super_simulation`, ingest, reject, recommend).
4. **Full suite** — `python -m unittest discover -s tests` in the package workflow.

## Local equivalent

```bash
pip install -e .
python -m nexus --help
python -m unittest tests.cli_smoke_tests tests.simulation_smoke_tests -v
python -m unittest discover -s tests -p '*smoke*.py' -v
python -m unittest discover -s tests -v
```

## Merge visibility

Workflow failures appear on the pull request Checks tab. For hard merge blocking, enable branch protection on `main` requiring the **Smoke** and **Python package** status checks. That setting is repository administration, not code; the workflows are written so those checks exist and fail clearly when CLI or simulation startup regresses.

## Related issues

- Issue #5 — simulation smoke tests
- Issue #6 — CI coverage for CLI and simulation startup
