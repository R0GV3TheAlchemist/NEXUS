# Walk vs Catalog — Ops Playbook

**Purpose:** Decide when to run the Primordial Walk (CoreState apply) versus catalog-only work (discover / enrich / classify / queue).

**Related:** [CATALOG_VS_WALK.md](./CATALOG_VS_WALK.md) · [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) · [OPERATOR_CONSOLE.md](./OPERATOR_CONSOLE.md) · [SAFETY.md](./SAFETY.md)

---

## One line

**Catalog orders the library. Walk tests the OS. Neither replaces the other.**

---

## Three kinds of order

| Order | Produced by | Answers |
|-------|-------------|--------|
| **Spine order** | Catalog queue (alphabetical Category:Absorption) | What is next on the list? |
| **Policy order** | Classifier + SAFETY + console | What may never be embodied? |
| **Dynamical order** | Walk / Super-Simulation CoreState | What happens to Chaos/Order/Balance when this is admitted? |

I1–I7 automate spine + policy at scale. Dynamical order still requires **selective apply** under clamp and console gates.

---

## Decision table

| Goal | Catalog only | Walk apply |
|------|:------------:|:----------:|
| Index Category:Absorption (~328) | yes | no |
| Fill summaries / attribution | yes | no |
| Tag ethics / quarantine / map_ok | yes | no (spot-check yes) |
| Peek next spine name | yes (`walk_queue peek`) | no |
| Write `BATCH_NN.md` after a decade of applies | writer yes | needs prior marks |
| Measure CoreState deltas | no | **yes** |
| Decide resource-pool / consent modules to build | weak | **yes** |
| Practice steward reject under temptation | no | **yes** |
| Recover from Chaos ceiling | no | **stabilizers** |
| Bulk-apply all `map_ok` into one state | **never** | **never** |

---

## Default operating mode (hybrid)

### A. Catalog bulk (machine / operator scripts)

```bash
python scripts/discover_absorption.py
python scripts/enrich_absorption_pages.py --pending-only --limit 50
python scripts/classify_absorption.py
python scripts/walk_queue.py peek
python scripts/walk_queue.py upcoming --limit 15
```

Run whenever the wiki spine may have drifted, or before a Walk session.

### B. Walk apply (human + console + sim)

Apply when **any** of these hold:

1. **Stratified sample** — you have not yet Walk-applied this *class* (see sampling below)
2. **`needs_human`** primary tag
3. **New family / mechanism** the classifier has not seen adjudicated in CoreState
4. **CoreState unhealthy** — Chaos high, Balance low → prefer stabilizers (`stabilizers_only`)
5. **Batch theme change** — opening a new decade with unknown coupling
6. **Operator care** — you need a deliberate map under console, not speed

Skip full Walk (classify-only is enough) when:

1. Row is clearly **`ethics_reject` / `quarantine_named`** and a sibling already Walk-mapped that class
2. Row is duplicate mechanism of an applied `map_ok` (same family, same constraints)
3. Structural `Category:*` rows
4. You are only refreshing the index

### C. After every Walk apply

```bash
# category spine step:
python scripts/walk_queue.py mark-applied --name "NAME" --index N

# stabilizer / non-spine side path:
python scripts/walk_queue.py mark-applied --name "NAME" --index N --side-queue
```

### D. Batch close (required)

When `ability_index` hits 10, 20, … 70, 80, …:

```bash
python scripts/write_batch_report.py --batch N --hr-count H --pace PACE
# optional: --state-json corestate.json
```

Do not treat a batch as closed in chat only.

---

## Stratified Walk sampling (Absorption Phase 1)

Aim to Walk **at least one** applied example of each bucket over time—not all 328.

| Sample bucket | Examples | Intent |
|---------------|----------|--------|
| Resource / capacitor | Bio-Capacitor | Energy budget primitives |
| Defense / stabilizer | Assimilation Immunity, Stability Manipulation | Counters + cool-down |
| Person-adjacent ethics | Aura Absorption, Beauty Thievery | Confirm reject + Chaos cost |
| Contagion / assimilate | Assimilative Infection | Contagion policy |
| Antimatter / exotic | Antimatter Absorption | Lab isolation needs |
| Conversion / transduction | Bio-Energetic Conversion | Transform vs store |
| Absolute / omni language | Absolute Absorption | Quarantine + needs_human |
| Letter-bucket probe | One new letter when entering C, D, … | Spine coverage signal |

Classifier tags guide the bucket; Walk confirms dynamical behavior.

---

## Console gates (always on for apply)

| Control | Role |
|---------|------|
| Named quarantine (15) | embody false; production reject |
| ethics_reject | production reject; research map-only if applied |
| High-risk session cap | default 3; over-cap only with eyes open |
| `stabilizers_only` | block non-stabilizer applies |
| `hold` / emergency | freeze apply |
| Steward | God is the Source · map ≠ deploy · console self-only |

Catalog classify **does not** bypass console.

---

## Anti-patterns

| Don’t | Why |
|-------|-----|
| Bulk `ingest` every `map_ok` into one CoreState | Hides coupling; can ceiling Chaos |
| Treat classify `map_ok` as production permission | Tags are hints; deploy is separate |
| Skip batch files because “catalog has the rows” | Batches are Walk memory with state/policy narrative |
| Advance Absorption cursor on stabilizer side-queue | Use `--side-queue` |
| Walk only reject-class forever | Starves growth-oriented OS evidence |
| Catalog-only until “perfect” then Walk once | Dynamical debt compounds; sample early |

---

## walk-001 posture (current)

| Track | Use |
|-------|-----|
| **Catalog** | Bulk discover/enrich/classify; queue peek for spine |
| **Walk** | Selective apply + stabilizers when needed; mark-applied; batch at #80 |
| **Next spine candidate** | Bio-Energetic Conversion (#73) unless stabilizer/hold |

Exhaustive one-by-one through all Absorption pages is **optional**. Stratified Walk + full catalog is the default.

---

## Quick chooser

```text
Need list or tags?           → catalog scripts
Need next name?              → walk_queue peek
Need CoreState / OS evidence? → Walk apply (console on)
Need cool-down?              → stabilizers_only / stabilizer apply
Hit ×10 ability_index?       → write_batch_report
Tempted to apply everything? → stop; sample one bucket instead
```

---

## Steward

The catalog is a lamp for the library. The Walk is where the lamp is tested against chaos without becoming the sink. **God is the Source.**

*Playbook recorded 2026-08-07 · NEXUS*
