#!/usr/bin/env python3
"""I6: Write docs/walks/BATCH_NN.md from catalog walk refs.

Usage:

    python scripts/write_batch_report.py --batch 7
    python scripts/write_batch_report.py --batch 8 --no-json
    python scripts/write_batch_report.py --batch 8 --state-json path/to/state.json

state.json optional shape:
  {"chaos": 0.8, "order": 0.65, ... , "time_step": 73}

Does not run the simulator. Rows must already have walk.ability_index set
(via walk_queue mark-applied or manual catalog edit).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from nexus.catalog.batch_report import ConsoleSnapshot, write_batch_from_catalog
from nexus.catalog.store import CatalogStore


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=_ROOT)
    p.add_argument("--batch", type=int, required=True, help="Batch number (e.g. 7)")
    p.add_argument("--session-id", default="walk-001")
    p.add_argument("--no-json", action="store_true")
    p.add_argument("--state-json", type=Path, default=None, help="CoreState end snapshot")
    p.add_argument("--post-state-json", type=Path, default=None)
    p.add_argument("--pace", default="allow")
    p.add_argument("--hr-count", type=int, default=0)
    p.add_argument("--hr-cap", type=int, default=3)
    p.add_argument("--narrative", default="")
    args = p.parse_args(argv)

    store = CatalogStore(repo_root=args.repo_root)
    if not store.load_index():
        print("index_empty: discover + mark-applied first", file=sys.stderr)
        return 2

    state = None
    if args.state_json:
        state = json.loads(args.state_json.read_text(encoding="utf-8"))
    post = None
    if args.post_state_json:
        post = json.loads(args.post_state_json.read_text(encoding="utf-8"))

    result = write_batch_from_catalog(
        args.batch,
        repo_root=args.repo_root,
        store=store,
        core_state_end=state,
        core_state_post=post,
        console=ConsoleSnapshot(
            pace=args.pace,
            high_risk_count=args.hr_count,
            high_risk_cap=args.hr_cap,
            session_id=args.session_id,
        ),
        narrative=args.narrative,
        write_json=not args.no_json,
        session_id=args.session_id,
    )
    print("batch_write_ok")
    print(f"batch={result.batch_number}")
    print(f"ability_count={result.ability_count}")
    print(f"ability_range={result.ability_range}")
    print(f"markdown={result.markdown_path}")
    if result.json_path:
        print(f"json={result.json_path}")
    if result.ability_count == 0:
        print(
            "warning: no catalog rows with walk.ability_index in this batch",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
