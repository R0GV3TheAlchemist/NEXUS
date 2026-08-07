#!/usr/bin/env python3
"""I3: Fetch Superpower Wiki page extracts into the Absorption catalog.

Prereq: run scripts/discover_absorption.py so index.jsonl is populated.

Usage:

    pip install -e .
    python scripts/enrich_absorption_pages.py --dry-run --limit 5
    python scripts/enrich_absorption_pages.py --pending-only --limit 20
    python scripts/enrich_absorption_pages.py --names Bio-Capacitor --names Absorption

Does not classify policy (I4). Does not apply abilities / CoreState.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from nexus.catalog.enrich import enrich_absorption_pages
from nexus.catalog.pages import fetch_page_documents
from nexus.catalog.store import CatalogStore


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=_ROOT)
    p.add_argument("--limit", type=int, default=None, help="Max pages this run")
    p.add_argument("--pause", type=float, default=0.5, help="Pause between API batches")
    p.add_argument("--batch-size", type=int, default=10)
    p.add_argument("--pending-only", action="store_true", help="Only rows with empty summary")
    p.add_argument("--names", action="append", default=[], help="Specific titles (repeatable)")
    p.add_argument("--no-sidecars", action="store_true", help="Do not write pages/*.json")
    p.add_argument("--dry-run", action="store_true", help="Fetch first batch sample only; no write")
    args = p.parse_args(argv)

    store = CatalogStore(repo_root=args.repo_root)
    entries = store.load_index()
    if not entries:
        print("index_empty: run scripts/discover_absorption.py first", file=sys.stderr)
        return 2

    if args.dry_run:
        sample = [e.name for e in entries if not e.name.startswith("Category:")][:5]
        docs = fetch_page_documents(sample, pause_seconds=args.pause, batch_size=args.batch_size)
        print(f"dry_run_fetched={len(docs)}")
        for d in docs:
            preview = (d.summary[:120] + "…") if len(d.summary) > 120 else d.summary
            print(f"  {d.title}: {preview}")
        return 0

    report = enrich_absorption_pages(
        repo_root=args.repo_root,
        names=args.names or None,
        limit=args.limit,
        batch_size=args.batch_size,
        pause_seconds=args.pause,
        write_sidecars=not args.no_sidecars,
        pending_only=args.pending_only,
    )
    print("enrich_ok")
    print(f"requested={report.requested}")
    print(f"fetched={report.fetched}")
    print(f"updated={report.updated}")
    print(f"written_sidecars={report.written_sidecars}")
    print(f"skipped_missing={report.skipped_missing}")
    print(f"index_size={report.index_size}")
    print(f"index_path={store.index_path}")
    print(f"pages_dir={store.root / 'pages'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
