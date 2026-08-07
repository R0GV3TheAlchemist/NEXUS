# Build Session — I5

**Opened:** 2026-08-07  
**Scope:** Wire Primordial Walk queue to Category:Absorption catalog order  
**Spec:** [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) step I5  
**Depends on:** I1 store/cursor · I2 index · I4 tags (optional but recommended)

---

## Delivered

| Artifact | Role |
|----------|------|
| `src/nexus/catalog/walk_queue.py` | `WalkQueue` peek/upcoming/mark_applied/skip/sync_cursor |
| `scripts/walk_queue.py` | Operator CLI |
| `tests/catalog_walk_queue_tests.py` | Cursor advance + side-queue tests |

## Behavior

- **Spine order:** alphabetical walkable pages (skips `Category:*` / `_subcat`)
- **Cursor:** `data/wiki_catalog/absorption/cursor.json`
- **`mark_applied`:** sets `walk.status=applied`, batch_id from ability index, advances cursor
- **`--side-queue` / `advance_cursor=False`:** stabilizer maps (e.g. #71 Stability Manipulation) do not move the Absorption cursor
- **`peek --skip-blocking`:** jumps past ethics/quarantine/hr/needs_human when you want a safer suggestion

## Not this step

- Does **not** call Super-Simulation / CoreState
- OperatorConsole still gates real apply
- Batch markdown writer is **I6**

## Operator flow

```bash
pip install -e .
python scripts/discover_absorption.py
python scripts/classify_absorption.py
python scripts/walk_queue.py cursor
python scripts/walk_queue.py peek
python scripts/walk_queue.py upcoming --limit 10
# after a Walk apply in chat/sim:
python scripts/walk_queue.py mark-applied --name "Bio-Capacitor" --index 72
python scripts/walk_queue.py mark-applied --name "Stability Manipulation" --index 71 --side-queue
```

## walk-001 alignment

Current designed cursor (from I1):

- last: Bio-Capacitor (#72)
- next: Bio-Energetic Conversion (#73)

## Steward

Queue is a lamp for order — not auto-embody. God is the Source.

**I5 status:** complete in tree.
