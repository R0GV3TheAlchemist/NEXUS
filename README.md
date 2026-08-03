# NEXUS

## CLI

- `nexus run` runs a single ability through the pipeline.
- `nexus bootstrap` checks and creates the current package skeleton.
- `nexus validate` validates JSON inputs without running the pipeline.

## Workflows

- `Python package` installs the package, runs the test suite, and checks `python -m nexus --help`.
- `Smoke` runs help/import checks and the smoke-focused tests.

## Current approach

The repository is being kept intentionally boring and stable: small imports, predictable startup, and minimal CI surface area.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the test suite locally.
5. Open a pull request with a clear description of the change.
