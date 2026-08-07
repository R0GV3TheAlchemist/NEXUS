"""Enrich catalog index rows with fetched page summaries (I3).

Writes optional pages/{slug}.json sidecars and updates entry.summary / url.
Preserves walk, policy_tags, and schema_draft. No CoreState mutation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from nexus.catalog.models import CatalogEntry
from nexus.catalog.pages import PageDocument, fetch_page_documents, slugify_title
from nexus.catalog.paths import PAGES_DIR_NAME, ensure_absorption_layout
from nexus.catalog.store import CatalogStore


@dataclass(frozen=True)
class EnrichReport:
    requested: int
    fetched: int
    updated: int
    skipped_missing: int
    written_sidecars: int
    index_size: int


def write_page_sidecar(pages_dir: Path, doc: PageDocument) -> Path:
    pages_dir.mkdir(parents=True, exist_ok=True)
    path = pages_dir / f"{slugify_title(doc.title)}.json"
    path.write_text(
        json.dumps(doc.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def apply_documents_to_index(
    store: CatalogStore,
    documents: list[PageDocument],
    *,
    write_sidecars: bool = True,
    only_names: set[str] | None = None,
) -> EnrichReport:
    """Merge documents into index by casefold(title)."""
    entries = store.load_index()
    by_key = {e.name.casefold(): e for e in entries}
    docs_by_key = {d.title.casefold(): d for d in documents}

    if only_names is not None:
        allow = {n.casefold() for n in only_names}
        target_keys = [k for k in by_key if k in allow]
    else:
        target_keys = list(by_key.keys())

    pages_dir = store.root / PAGES_DIR_NAME
    updated = 0
    written = 0
    skipped = 0

    for key in target_keys:
        doc = docs_by_key.get(key)
        if doc is None:
            continue
        old = by_key[key]
        new_summary = doc.summary or old.summary
        new_url = doc.url or old.url
        if new_summary != old.summary or new_url != old.url:
            updated += 1
        by_key[key] = CatalogEntry(
            name=old.name,
            url=new_url,
            category_path=old.category_path,
            letter_bucket=old.letter_bucket,
            source_license=old.source_license,
            attribution=old.attribution,
            fanon=old.fanon,
            summary=new_summary,
            schema_draft=old.schema_draft,
            policy_tags=old.policy_tags,
            walk=old.walk,
        )
        if write_sidecars:
            write_page_sidecar(pages_dir, doc)
            written += 1

    for key, doc in docs_by_key.items():
        if key in by_key:
            continue
        skipped += 1

    ordered = sorted(by_key.values(), key=lambda e: e.name.casefold())
    store.save_index(ordered)

    return EnrichReport(
        requested=len(target_keys),
        fetched=len(documents),
        updated=updated,
        skipped_missing=skipped,
        written_sidecars=written,
        index_size=len(ordered),
    )


def enrich_absorption_pages(
    repo_root: Path | None = None,
    *,
    names: list[str] | None = None,
    limit: int | None = None,
    fetch=None,
    batch_size: int = 10,
    pause_seconds: float = 0.5,
    write_sidecars: bool = True,
    pending_only: bool = False,
) -> EnrichReport:
    """Fetch extracts for index rows and merge summaries."""
    ensure_absorption_layout(repo_root)
    store = CatalogStore(repo_root=repo_root)
    entries = store.load_index()

    candidates = [
        e
        for e in entries
        if not (len(e.category_path) > 1 and e.category_path[-1] == "_subcat")
        and not e.name.startswith("Category:")
    ]
    if pending_only:
        candidates = [e for e in candidates if not (e.summary or "").strip()]
    if names:
        allow = {n.casefold() for n in names}
        candidates = [e for e in candidates if e.name.casefold() in allow]
    candidates.sort(key=lambda e: e.name.casefold())
    if limit is not None:
        candidates = candidates[: max(0, limit)]

    titles = [e.name for e in candidates]
    if not titles:
        return EnrichReport(
            requested=0,
            fetched=0,
            updated=0,
            skipped_missing=0,
            written_sidecars=0,
            index_size=len(entries),
        )

    docs = fetch_page_documents(
        titles,
        fetch=fetch,
        batch_size=batch_size,
        pause_seconds=pause_seconds if fetch is None else 0.0,
    )
    only = {t for t in titles}
    return apply_documents_to_index(
        store,
        docs,
        write_sidecars=write_sidecars,
        only_names=only,
    )
