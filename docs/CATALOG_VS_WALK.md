# Catalog vs Walk

**One line:** The catalog may hold the **totality** of a Superpower Wiki category; the Walk **applies** only what the operator (and policy) admit into CoreState.

---

## Two stores

| Store | Lives in | Holds | Mutates CoreState? |
|-------|----------|-------|--------------------|
| **Catalog** | `data/wiki_catalog/` | Names, urls, summaries, schema drafts, policy tags | **No** |
| **Walk / Sim** | Super-Simulation + ledger + `docs/walks/` | Applied abilities, deltas, batch reports | **Yes** (gated) |

Auto-ingestion fills the **catalog**.  
Primordial Walk consumes the catalog **one row at a time** (or lab-sampled batches under clamp).

---

## What totality means here

| Phrase | Allowed? |
|--------|----------|
| Totality of **Category:Absorption** indexed | Yes — Phase 1 goal |
| Totality of Superpower Wiki indexed | Later phases only |
| Totality applied to one CoreState | **No** |
| Totality classified for search / queue | Yes |
| Totality embodied as OS identity | **No** |

---

## Batch reports belong to the Walk

`docs/walks/BATCH_NN.md` files are **Walk artifacts**, not catalog dumps.

- They summarize **10 applied** abilities (schema + policy + CoreState end-state)
- Auto-ingestion **generates** them at batch boundaries from the ledger
- They must not list all 328 category pages unless all 328 were actually applied

Catalog completeness ≠ Walk completeness.

---

## Operator console

| Action | Catalog | Walk |
|--------|---------|------|
| `sync` / classify | yes | no |
| `stabilizers_only` | no effect on sync | blocks non-stabilizer apply |
| high-risk cap | tags only | blocks/counts applies |
| emergency hold | sync may continue | apply blocked |

---

## Steward boundary

Map and index freely under license and safety tags.  
Do not treat a full catalog as permission to deploy.  
**God is the Source.**

See: [SUPERPOWER_WIKI_INGESTION.md](./SUPERPOWER_WIKI_INGESTION.md) · [SAFETY.md](./SAFETY.md) · [OPERATOR_CONSOLE.md](./OPERATOR_CONSOLE.md)
