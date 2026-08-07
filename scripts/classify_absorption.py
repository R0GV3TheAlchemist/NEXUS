#!/usr/bin/env python3
"""I4: Fail-closed policy classification for Absorption catalog rows.

Prereq: discover (I2) and ideally enrich (I3) so summaries exist.

Usage:

    pip install -e .
    python scripts/classify_absorption.py --dry-run
    python scripts/classify_absorption.py
    python scripts/classify_absorption.py --names "Aura Absorption" --names Bio-Capacitor

Does not apply abilities or touch CoreState.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from nexus.catalog.classify import classify_index
from nexus.catalog.store import CatalogStore


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=_ROOT)
    p.add_argument("--dry-run", action="store_true", help="Print counts; do not write index")
    p.add_argument("--names", action="append", default=[], help="Limit to titles")
    p.add_argument(
        "--no-schema-hints",
        action="store_true",
        help="Do not update schema_draft stability/growth from primary tag",
    )
    p.add_argument(
        "--show", type=int, default=15, help="Print first N classification lines"
    )
    args = p.parse_args(argv)

    store = CatalogStore(repo_root=args.repo_root)
    if not store.load_index():
        print("index_empty: run discover_absorption.py first", file=sys.stderr)
        return 2

    report, results = classify_index(
        store,
        write=not args.dry_run,
        names=args.names or None,
        update_schema_hints=not args.no_schema_hints,
    )
    print("classify_ok" if not args.dry_run else "classify_dry_run")
    print(f"total={report.total}")
    print(f"updated={report.updated}")
    for key, count in sorted(report.by_primary.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"primary.{key}={count}")
    for row in results[: max(0, args.show)]:
        print(f"  {row.name}: {row.primary} tags={list(row.tags)}")
    if len(results) > args.show:
        print("  …")
    print(f"index_path={store.index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
