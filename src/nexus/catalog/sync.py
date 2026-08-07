"""Merge discovered category members into the catalog index (I2).

Preserves existing walk status / policy_tags / schema_draft on name match.
Never touches CoreState or simulation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from nexus.catalog.discover import (
    CategoryMember,
    discover_absorption_members,
    pages_only,
    subcats_only,
)
from nexus.catalog.models import CatalogEntry, SchemaDraft, WalkRef
from nexus.catalog.store import CatalogStore


@dataclass(frozen=True)
class SyncReport:
    discovered_total: int
    pages: int
    subcats: int
    added: int
    updated_meta: int
    preserved: int
    index_size: int


def _letter_bucket(title: str) -> str:
    title = title.strip()
    return title[:1].upper() if title else ""


def member_to_entry(member: CategoryMember) -> CatalogEntry:
    tags: tuple[str, ...] = ()
    # Subcategory rows are structural; pages start untagged (I4 classifies).
    return CatalogEntry(
        name=member.title,
        url=member.url,
        category_path=("Absorption",) if not member.is_subcategory else ("Absorption", "_subcat"),
        letter_bucket=_letter_bucket(member.title),
        summary="",
        schema_draft=SchemaDraft(),
        policy_tags=tags,
        walk=WalkRef(status="pending"),
        fanon="/Fanon:" in member.title or member.title.startswith("Fanon:"),
    )


def merge_members_into_index(
    store: CatalogStore,
    members: list[CategoryMember],
    *,
    include_subcats: bool = True,
) -> SyncReport:
    """Upsert members by casefold(name). Preserve walk/policy/schema on hit."""
    existing = store.load_index()
    by_key = {e.name.casefold(): e for e in existing}

    selected: list[CategoryMember] = []
    page_rows = pages_only(members)
    selected.extend(page_rows)
    sub_rows = subcats_only(members) if include_subcats else []
    if include_subcats:
        selected.extend(sub_rows)

    added = 0
    updated_meta = 0
    preserved = 0
    merged: dict[str, CatalogEntry] = dict(by_key)

    for member in selected:
        key = member.title.casefold()
        fresh = member_to_entry(member)
        old = merged.get(key)
        if old is None:
            merged[key] = fresh
            added += 1
            continue
        # Preserve adjudication fields; refresh url/letter/category_path/fanon.
        preserved += 1
        if old.url != fresh.url or old.letter_bucket != fresh.letter_bucket:
            updated_meta += 1
        merged[key] = CatalogEntry(
            name=old.name,
            url=fresh.url,
            category_path=fresh.category_path,
            letter_bucket=fresh.letter_bucket or old.letter_bucket,
            source_license=old.source_license,
            attribution=old.attribution,
            fanon=fresh.fanon,
            summary=old.summary,
            schema_draft=old.schema_draft,
            policy_tags=old.policy_tags,
            walk=old.walk,
        )

    # Stable order: alphabetical by name (category spine).
    ordered = sorted(merged.values(), key=lambda e: e.name.casefold())
    store.save_index(ordered)

    return SyncReport(
        discovered_total=len(members),
        pages=len(page_rows),
        subcats=len(sub_rows),
        added=added,
        updated_meta=updated_meta,
        preserved=preserved,
        index_size=len(ordered),
    )


def sync_absorption_catalog(
    repo_root: Path | None = None,
    *,
    fetch=None,
    include_subcats: bool = True,
    pause_seconds: float = 0.5,
) -> SyncReport:
    """Live or injected-fetch discovery + merge into absorption index."""
    store = CatalogStore(repo_root=repo_root)
    members = discover_absorption_members(fetch=fetch, pause_seconds=pause_seconds)
    return merge_members_into_index(
        store, members, include_subcats=include_subcats
    )
