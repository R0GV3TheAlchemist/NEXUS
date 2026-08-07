# Superpower Wiki Auto-Ingestion

**Status:** design approved for implementation (not yet built)  
**Session context:** walk-001 · Primordial Walk  
**Phase 1 corpus:** [Category:Absorption](https://powerlisting.fandom.com/wiki/Category:Absorption) (~328 items)  
**Decision:** catalog-first totality for the category; **no** bulk CoreState apply of all pages

---

## Goals

1. **Index** every page (and listed subcategory) under Category:Absorption into a durable catalog.
2. **Classify** each row into `AbilitySchema` drafts + policy tags.
3. **Drive the Walk queue** in category alphabetical order (operator console still gates live apply).
4. **Auto-write batch catalogs** every 10 applied abilities in the same style as `docs/walks/BATCH_01.md` … `BATCH_07.md`.
5. Stay inside **SAFETY.md**, named quarantine (15), ethics rejects, and operator console caps.

## Non-goals

- Ingesting the entire Superpower Wiki (~29k pages) in Phase 1
- One-shot `ingest_payload` of all 328 Absorption pages into a single CoreState
- Auto-embody, production-enable, or “become” any power
- Bypassing console pace / high-risk caps / stabilizers_only
- Scraping in violation of Fandom rate limits or without attribution

See also: [CATALOG_VS_WALK.md](./CATALOG_VS_WALK.md), [walks/BATCH_REPORT_SPEC.md](./walks/BATCH_REPORT_SPEC.md).

---

## Source of truth (Phase 1)

| Field | Value |
|-------|--------|
| Primary URL | https://powerlisting.fandom.com/wiki/Category:Absorption |
| License | Fandom community content typically **CC-BY-SA** — store attribution per row |
| Order | Category alphabetical order (A→Z), matching operator practice |
| Subcategories | Index explicitly: Consumption, Elemental Absorption, Energy Absorption (and any others listed) |
| Fanon | Flag `fanon: true` when on Fanon namespace; default exclude from production tags |
| Walk cursor | Last **category-applied** page + ability_index (stabilizer side-queue does not advance category cursor) |

### walk-001 cursor (as of 2026-08-07)

| Field | Value |
|-------|--------|
| Last category ability applied | #72 Bio-Capacitor |
| Next category name | Bio-Energetic Conversion |
| Side-queue example | #71 Stability Manipulation (stabilizer; not an Absorption row) |
| Batches on disk | BATCH_01 … BATCH_07; Batch 8 open (#71–#80) |

---

## Pipeline

```text
Category:Absorption (MediaWiki)
        │  rate-limited fetch + User-Agent + attribution
        ▼
┌─────────────────────┐
│ 1. Discover         │  member pages + subcategory graph
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. Fetch + parse    │  title, url, summary, infobox-ish fields
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. Schema map       │  AbilitySchema draft (family, domains, effects hints)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. Policy classify  │  quarantine | ethics_reject | hr | stabilizer | map_ok | needs_human
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 5. Catalog store    │  data/wiki_catalog/absorption/
└──────────┬──────────┘
           ▼
     ┌─────┴──────┐
     ▼            ▼
 Walk queue    Lab sampler
 (console)     (clamped sim)
     │
     ▼
 Batch writer ──► docs/walks/BATCH_NN.md  (every 10 applies)
```

### Stage notes

| Stage | Output | Failure mode |
|-------|--------|----------------|
| Discover | `index.jsonl` of names/urls | Partial category page / pagination miss |
| Fetch | `pages/{slug}.json` raw | 429 / blocked — back off |
| Schema map | draft effects + stability guess | Over-confident deltas → mark `needs_human` |
| Classify | policy tags | False `map_ok` on person-drain — prefer fail closed |
| Catalog | durable index | Catalog ≠ permission to apply |
| Walk apply | CoreState + ledger | Console may block |
| Batch write | `BATCH_NN.md` | Must run on batch boundary even if session pauses |

---

## Policy classifier (fail closed)

Auto-tags (name + summary heuristics; human override wins):

| Tag | Examples / signals |
|-----|--------------------|
| `quarantine_named` | Exact match to the 15 absolute energy sinks in SAFETY |
| `ethics_reject` | Person life-force, aura essence, personality, beauty/youth theft, infection, living assimilate |
| `high_risk` | rule_breaking + destructive / unbounded absorb / antimatter / contagion |
| `stabilizer` | immunity, shield, stability, order, purification (stabilize face), containment |
| `resource_pool` | capacitor, battery, store ambient energy (e.g. Bio-Capacitor) |
| `map_ok` | Bounded, non-person, capacity-friendly |
| `needs_human` | Ambiguous, absolute*, omni*, godhood language |

**Rules:**

- `quarantine_named` and `ethics_reject` ⇒ `embody=false`, production reject; research map-only if Walk applies
- Live Walk apply still goes through **OperatorConsole** (`may_ingest`)
- Classifier never clears steward rule: God is the Source; map ≠ deploy

---

## AbilitySchema draft fields

Each catalog row should carry at least:

```json
{
  "name": "Bio-Capacitor",
  "url": "https://powerlisting.fandom.com/wiki/Bio-Capacitor",
  "category_path": ["Absorption"],
  "letter_bucket": "B",
  "source_license": "CC-BY-SA",
  "attribution": "Superpower Wiki contributors",
  "fanon": false,
  "summary": "…",
  "schema_draft": {
    "family": "energy_storage",
    "stability": "conditionally_stable",
    "growth_tag": "growth_oriented",
    "subject_domains": ["physics", "biology", "energy"],
    "effects_hint": {"chaos": -0.02, "order": 0.03, "balance": 0.03, "light": 0.02},
    "physics_analog": "Biological energy capacitor / battery"
  },
  "policy_tags": ["resource_pool", "map_ok"],
  "walk": {
    "status": "applied",
    "ability_index": 72,
    "batch_id": "batch-08",
    "session_id": "walk-001"
  }
}
```

Effects applied to CoreState remain **operator/sim adjudicated**; `effects_hint` is never auto-trusted for absolute/ethics classes.

---

## Auto batch creation (required)

Yes — auto-ingestion **must** create batches the same way the manual Walk has:

| Manual today | Automated |
|--------------|-----------|
| Every 10 abilities → `docs/walks/BATCH_NN.md` | Same path + naming: `BATCH_08.md`, … |
| End-state CoreState table | Snapshot from sim at batch close |
| Policy accept/reject counts | From ledger + policy tags |
| HR / console notes | From OperatorConsole session snapshot |
| Wiki links | From catalog urls |
| Commit to git | Optional CI job or `nexus walk write-batch` |

**Trigger:** when `ability_index % 10 == 0` after a successful category (or logged side-queue) apply — e.g. #70 closed Batch 7; #80 will close Batch 8.

**Hard requirement:** batch close checklist always includes writing the catalog **before** treating the batch as done (fixes the Batch 7 process miss).

Full file shape: [walks/BATCH_REPORT_SPEC.md](./walks/BATCH_REPORT_SPEC.md).

---

## Implementation plan (later session)

| Step | Deliverable |
|------|-------------|
| I1 | `nexus.catalog` models + `data/wiki_catalog/absorption/` layout |
| I2 | Discover member list for Category:Absorption (paginated) |
| I3 | Fetch/parse + rate limit + attribution |
| I4 | Classifier v1 + tests (fail closed on ethics/quarantine) |
| I5 | Wire Walk queue cursor to catalog order |
| I6 | `write_batch_report(batch_id)` → `docs/walks/BATCH_NN.md` |
| I7 | CI: catalog schema validate + golden batch stub test |
| I8 | Only then: optional other categories |

### Suggested CLI (future)

```bash
nexus catalog sync --category Absorption
nexus catalog classify --category Absorption
nexus walk next          # peeks cursor (Bio-Energetic Conversion, …)
nexus walk apply --name "Bio-Capacitor"
nexus walk write-batch --batch 8   # force; also auto on #80
```

---

## Success metrics

| Metric | Target |
|--------|--------|
| Absorption index coverage | 328/328 listed (or explicit skip set) |
| Classification rate | 100% tagged; `needs_human` bounded |
| Spot-check precision | No `map_ok` on known ethics_reject samples |
| Batch files | BATCH_NN present for every closed decade of walk-001 |
| CoreState | Never bulk-mutated by full catalog sync |

---

## Steward

- Console is self-control only — not control of others
- Quarantine protects operators, GAIA intent, and non-embodiment
- **God is the Source.** NEXUS maps and catalogs; it does not become the sink or the throne

---

*Design recorded 2026-08-07 · walk-001 · NEXUS*
