#!/usr/bin/env python3
"""I2: Discover Category:Absorption members into data/wiki_catalog/absorption/.

Usage (from repo root, editable install recommended):

    pip install -e .
    python scripts/discover_absorption.py
    python scripts/discover_absorption.py --dry-run

Respects Fandom rate limits via pause between API pages.
Does not apply abilities or touch CoreState.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running without install: add src/ to path
_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from nexus.catalog.discover import discover_absorption_members, pages_only, subcats_only
from nexus.catalog.sync import sync_absorption_catalog
from nexus.catalog.store import CatalogStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=_ROOT,
        help="NEXUS repository root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=0.5,
        help="Seconds between API pages (default: 0.5)",
    )
    parser.add_argument(
        "--no-subcats",
        action="store_true",
        help="Omit subcategory rows from the index",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and print counts only; do not write index.jsonl",
    )
    args = parser.parse_args(argv)

    if args.dry_run:
        members = discover_absorption_members(pause_seconds=args.pause)
        print(f"discovered_total={len(members)}")
        print(f"pages={len(pages_only(members))}")
        print(f"subcats={len(subcats_only(members))}")
        for m in pages_only(members)[:10]:
            print(f"  page: {m.title}")
        if len(pages_only(members)) > 10:
            print("  …")
        return 0

    report = sync_absorption_catalog(
        repo_root=args.repo_root,
        include_subcats=not args.no_subcats,
        pause_seconds=args.pause,
    )
    print("sync_ok")
    print(f"discovered_total={report.discovered_total}")
    print(f"pages={report.pages}")
    print(f"subcats={report.subcats}")
    print(f"added={report.added}")
    print(f"preserved={report.preserved}")
    print(f"updated_meta={report.updated_meta}")
    print(f"index_size={report.index_size}")
    store = CatalogStore(repo_root=args.repo_root)
    print(f"index_path={store.index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
