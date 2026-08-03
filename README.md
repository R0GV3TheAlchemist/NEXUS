# NEXUS

## Command-line usage

Run a single ability:

```bash
nexus run --principal '{"id": "u1"}' --ability '{"name": "Absorption"}' --policy '{}'
```

Bootstrap the package skeleton:

```bash
nexus bootstrap --root .
```

Validate inputs without running the pipeline:

```bash
nexus validate --principal '{"id": "u1"}' --ability '{"name": "Absorption"}' --policy '{}'
```
