# Wiki catalog — Category:Absorption

**Phase 1 corpus for NEXUS auto-ingestion.**

| Field | Value |
|-------|--------|
| Source category | https://powerlisting.fandom.com/wiki/Category:Absorption |
| Approximate size | 328 members (pages + subcategory entries) |
| License | Superpower Wiki community content — treat as **CC-BY-SA**; keep attribution |
| Walk spine | walk-001 alphabetical Absorption queue |
| Design docs | `docs/SUPERPOWER_WIKI_INGESTION.md`, `docs/CATALOG_VS_WALK.md` |

## Layout (target)

```text
data/wiki_catalog/absorption/
  README.md                 # this file
  index.jsonl               # one JSON object per category member (ordered)
  pages/                    # optional raw/normalized page JSON by slug
  cursor.json               # last category name applied + ability_index
  ATTRIBUTION.md            # CC-BY-SA + link back to Superpower Wiki
```

This directory holds the **catalog only**. It does not apply CoreState deltas.

## cursor.json (example)

```json
{
  "session_id": "walk-001",
  "category": "Absorption",
  "last_applied_name": "Bio-Capacitor",
  "last_ability_index": 72,
  "next_name": "Bio-Energetic Conversion",
  "updated_at": "2026-08-07"
}
```

## Provenance

Derived from Superpower Wiki (Fandom). Not official affiliation.  
When publishing derived catalogs, preserve license notices and link to source pages.

## Steward

Catalog ≠ deploy. Map ≠ embody. God is the Source.
