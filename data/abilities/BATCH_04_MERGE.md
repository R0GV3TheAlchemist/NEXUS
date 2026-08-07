# Batch 4 merge note

## Files landed

| Path | Role |
|------|------|
| `docs/walks/BATCH_04.md` | Human batch report (abilities 31–40) |
| `data/abilities/walk_001_batch_04.json` | Machine catalog slice for Batch 4 |
| `data/abilities/walk_001_catalog.json` | **Merge target** — append Batch 4 abilities; set `batches_complete` to include `4`; set `count` to `40` |

## Merge rules

1. Do **not** insert any ability named `Absorption Field Generation`.
2. Ability **#39** must be exactly `Absorption Field Projection`.
3. Keep named quarantine count at **15** (unchanged).
4. Set session end_state from `walk_001_batch_04.json` → `end_state` after merge checkpoint.
5. `console_attached`: true from Batch 3 onward.

## Suggested root fields after merge

```json
{
  "session": "walk-001",
  "count": 40,
  "batches_complete": [1, 2, 3, 4],
  "named_quarantine_count": 15,
  "console_attached": true,
  "steward_bound": "Map fully. Find higher order. Never become the Source."
}
```
