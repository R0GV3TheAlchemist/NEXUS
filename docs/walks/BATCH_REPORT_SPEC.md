# Batch Report Spec

**Purpose:** Define the durable batch catalog format used by walk-001 (`BATCH_01` … `BATCH_07` and successors) so **auto-ingestion / Walk tooling can generate the same files** without drift.

**Output path:** `docs/walks/BATCH_{NN}.md` with `NN` = zero-padded batch number (`01`, `02`, …).  
**Optional twin:** `docs/walks/BATCH_{NN}.json` (machine ledger snapshot) — recommended for automation, not required for human parity.

---

## When to write

| Event | Action |
|-------|--------|
| `ability_index` reaches 10, 20, 30, … | **Required:** write/close `BATCH_NN.md` |
| Batch ends mid-session | Write before cool-down or pace change is “done” |
| Stabilizer side-queue abilities | Include if they consumed an ability_index slot in that decade |
| Catalog sync only (no applies) | **Do not** write a Walk batch |

**Batch number:** `NN = ceil(ability_index / 10)` at close.  
Example: abilities #61–#70 → Batch 07; #71–#80 → Batch 08.

**Process rule:** Never close a batch in chat only — disk catalog is part of completion (Batch 7 correction).

---

## Required sections (Markdown)

Mirror existing catalogs (especially `BATCH_07.md`):

1. **Title** — `# Batch {NN} — Primordial Walk Catalog`
2. **Header metadata**
   - Session id (`walk-001`)
   - Range (`#Lo–#Hi`)
   - Source (Superpower Wiki; Category:Absorption when applicable)
   - Console state (pace, HR count/cap)
   - Named quarantine note
   - Post-batch actions (e.g. `stabilizers_only`)
3. **Ability table** — one row per applied ability:
   - `#` · Name · Stability · Growth · Family · HR · Embody · Production
4. **Wiki references** — name + URL from catalog
5. **Batch narrative** — short theme / OS lesson (template-assisted OK; human edit allowed)
6. **CoreState**
   - End of last ability in batch (required)
   - Optional: post cool-down table if stabilizers ran before report finalize
7. **Policy summary** — counts: accept / map-constrain / HR reject / quarantine
8. **Console / operator** — pace, HR, steward line
9. **Recommendations** — from `sim.recommend()` or equivalent heuristics
10. **Build implications** — bullet or table (evidence only)
11. **Files** — pointers to SAFETY, OPERATOR_CONSOLE, this batch
12. **Footer** — batch closed · next ability index · ISO date

---

## Ability table columns

```markdown
| # | Name | Stability | Growth | Family | HR | Embody | Production |
|---|------|-----------|--------|--------|----|--------|------------|
| 72 | Bio-Capacitor | conditionally_stable | growth_oriented | energy_storage | no | constrained | accept with capacity |
```

Stability values: `stable` | `conditionally_stable` | `rule_breaking`  
Growth values: `growth_oriented` | `context_dependent` | `destructive_oriented`  
HR: `yes` / `no`  
Embody: `false` | `eligible` | `constrained` | `counter`  
Production: short policy phrase

---

## JSON twin (optional but preferred for auto)

```json
{
  "batch_id": "batch-08",
  "batch_number": 8,
  "session_id": "walk-001",
  "ability_range": [71, 80],
  "category_spine": "Absorption",
  "closed_at": "2026-08-07T00:00:00Z",
  "console": {
    "pace": "allow",
    "high_risk_count": 7,
    "high_risk_cap": 3
  },
  "core_state_end": {
    "chaos": 0.0,
    "order": 0.0,
    "void": 0.0,
    "light": 0.0,
    "balance": 0.0,
    "law": 0.0,
    "magic": 0.0,
    "time_step": 0
  },
  "abilities": [],
  "policy_counts": {
    "accept": 0,
    "map_constrain": 0,
    "reject": 0,
    "quarantine": 0
  },
  "markdown_path": "docs/walks/BATCH_08.md"
}
```

---

## Generator API (future)

```text
write_batch_report(
  sim,
  console,
  ledger_slice,   # abilities Hi-9 .. Hi
  batch_number: int,
  out_dir: "docs/walks"
) -> paths["md", "json?"]
```

**Inputs must include:** final CoreState snapshot, per-ability policy decisions, wiki urls, HR tally.  
**Idempotent:** re-running for Batch N overwrites the same paths with a new commit message recommended.

---

## Acceptance tests

- Golden test: given a fixture ledger for #61–#70, generator produces headers + 10 table rows + CoreState section
- Batch file exists immediately after simulated apply of index 70, 80, …
- Catalog sync without applies creates **zero** new BATCH files

---

## Naming compatibility

| Batch | Abilities |
|------:|-----------|
| 01 | 1–10 |
| 02 | 11–20 |
| … | … |
| 07 | 61–70 |
| 08 | 71–80 |
| 09 | 81–90 |

---

*Spec recorded 2026-08-07 · aligns with BATCH_07.md structure*
