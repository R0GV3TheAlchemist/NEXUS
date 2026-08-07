#!/usr/bin/env python3
"""I5: Walk queue over Category:Absorption catalog order.

Usage:

    python scripts/walk_queue.py peek
    python scripts/walk_queue.py peek --skip-blocking
    python scripts/walk_queue.py upcoming --limit 15
    python scripts/walk_queue.py mark-applied --name "Bio-Capacitor" --index 72
    python scripts/walk_queue.py mark-applied --name "Stability Manipulation" --index 71 --side-queue
    python scripts/walk_queue.py sync-cursor --name "Bio-Capacitor" --index 72

Does not run Super-Simulation. Console still gates real apply.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from nexus.catalog.walk_queue import WalkQueue


def _print_item(item) -> None:
    flag = "BLOCK" if item.blocking else "ok"
    print(f"{item.name}\t{flag}\t{item.primary_tag}\t{item.url}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=_ROOT)
    p.add_argument("--session-id", default="walk-001")
    sub = p.add_subparsers(dest="cmd", required=True)

    peek_p = sub.add_parser("peek", help="Show next queue item")
    peek_p.add_argument("--skip-blocking", action="store_true")

    up_p = sub.add_parser("upcoming", help="List upcoming items")
    up_p.add_argument("--limit", type=int, default=10)
    up_p.add_argument("--skip-blocking", action="store_true")

    mark_p = sub.add_parser("mark-applied", help="Mark applied + advance cursor")
    mark_p.add_argument("--name", required=True)
    mark_p.add_argument("--index", type=int, required=True, dest="ability_index")
    mark_p.add_argument("--batch-id", default=None)
    mark_p.add_argument(
        "--side-queue",
        action="store_true",
        help="Do not advance category cursor (stabilizer side path)",
    )

    skip_p = sub.add_parser("mark-skipped", help="Mark skipped and advance cursor")
    skip_p.add_argument("--name", required=True)
    skip_p.add_argument("--index", type=int, default=None, dest="ability_index")

    sync_p = sub.add_parser("sync-cursor", help="Set cursor without walk status change")
    sync_p.add_argument("--name", required=True)
    sync_p.add_argument("--index", type=int, default=None, dest="ability_index")

    sub.add_parser("cursor", help="Show cursor.json")

    args = p.parse_args(argv)
    q = WalkQueue(repo_root=args.repo_root, session_id=args.session_id)

    if args.cmd == "peek":
        item = q.peek(skip_blocking=args.skip_blocking)
        if item is None:
            print("queue_empty")
            return 0
        _print_item(item)
        return 0

    if args.cmd == "upcoming":
        items = q.upcoming(limit=args.limit, skip_blocking=args.skip_blocking)
        print(f"count={len(items)}")
        for item in items:
            _print_item(item)
        return 0

    if args.cmd == "mark-applied":
        entry = q.mark_applied(
            args.name,
            ability_index=args.ability_index,
            batch_id=args.batch_id,
            advance_cursor=not args.side_queue,
        )
        print("marked_applied", entry.name, entry.walk.ability_index)
        cur = q.load_cursor()
        if cur:
            print(f"cursor.next={cur.next_name}")
        return 0

    if args.cmd == "mark-skipped":
        entry = q.mark_skipped(args.name, ability_index=args.ability_index)
        print("marked_skipped", entry.name)
        return 0

    if args.cmd == "sync-cursor":
        cur = q.sync_cursor_from_name(args.name, ability_index=args.ability_index)
        print(
            f"cursor last={cur.last_applied_name} next={cur.next_name} index={cur.last_ability_index}"
        )
        return 0

    if args.cmd == "cursor":
        cur = q.load_cursor()
        if cur is None:
            print("cursor_missing")
            return 0
        print(f"session_id={cur.session_id}")
        print(f"last_applied_name={cur.last_applied_name}")
        print(f"last_ability_index={cur.last_ability_index}")
        print(f"next_name={cur.next_name}")
        print(f"updated_at={cur.updated_at}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
