"""Walk queue over Category:Absorption catalog order (I5).

The queue reads index.jsonl + cursor.json and advances the category spine.
Stabilizer side-queue abilities should NOT call mark_applied with advance_cursor=True.

Does not mutate CoreState. OperatorConsole still gates real simulation apply.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from nexus.catalog.models import CatalogCursor, CatalogEntry, WalkRef
from nexus.catalog.store import CatalogStore

_BLOCKING_TAGS = frozenset(
    {"quarantine_named", "ethics_reject", "high_risk", "needs_human"}
)


@dataclass(frozen=True)
class QueueItem:
    entry: CatalogEntry
    position: int
    blocking: bool
    primary_tag: str

    @property
    def name(self) -> str:
        return self.entry.name

    @property
    def url(self) -> str:
        return self.entry.url


def _is_structural(entry: CatalogEntry) -> bool:
    if entry.name.startswith("Category:"):
        return True
    if len(entry.category_path) > 1 and entry.category_path[-1] == "_subcat":
        return True
    return False


def _primary_tag(entry: CatalogEntry) -> str:
    order = [
        "quarantine_named",
        "ethics_reject",
        "high_risk",
        "needs_human",
        "stabilizer",
        "resource_pool",
        "map_ok",
    ]
    tags = set(entry.policy_tags)
    for key in order:
        if key in tags:
            return key
    return "untagged"


def _is_blocking(entry: CatalogEntry) -> bool:
    return bool(set(entry.policy_tags) & _BLOCKING_TAGS)


def walkable_entries(entries: Iterable[CatalogEntry]) -> list[CatalogEntry]:
    pages = [e for e in entries if not _is_structural(e)]
    return sorted(pages, key=lambda e: e.name.casefold())


class WalkQueue:
    def __init__(
        self,
        store: CatalogStore | None = None,
        *,
        repo_root: Path | None = None,
        session_id: str = "walk-001",
    ) -> None:
        self.store = store or CatalogStore(repo_root=repo_root)
        self.session_id = session_id

    def _pages(self) -> list[CatalogEntry]:
        return walkable_entries(self.store.load_index())

    def load_cursor(self) -> CatalogCursor | None:
        return self.store.load_cursor()

    def _cursor_index(self, pages: list[CatalogEntry], cursor: CatalogCursor | None) -> int:
        if cursor is None or not cursor.last_applied_name:
            return -1
        key = cursor.last_applied_name.casefold()
        for i, e in enumerate(pages):
            if e.name.casefold() == key:
                return i
        return -1

    def peek(
        self,
        *,
        skip_blocking: bool = False,
        skip_applied: bool = True,
    ) -> QueueItem | None:
        pages = self._pages()
        if not pages:
            return None
        cursor = self.load_cursor()
        start = self._cursor_index(pages, cursor) + 1
        for pos in range(start, len(pages)):
            entry = pages[pos]
            if skip_applied and entry.walk.status == "applied":
                continue
            if skip_blocking and _is_blocking(entry):
                continue
            return QueueItem(
                entry=entry,
                position=pos,
                blocking=_is_blocking(entry),
                primary_tag=_primary_tag(entry),
            )
        return None

    def upcoming(
        self,
        limit: int = 10,
        *,
        skip_blocking: bool = False,
        skip_applied: bool = True,
    ) -> list[QueueItem]:
        pages = self._pages()
        cursor = self.load_cursor()
        start = self._cursor_index(pages, cursor) + 1
        out: list[QueueItem] = []
        for pos in range(start, len(pages)):
            entry = pages[pos]
            if skip_applied and entry.walk.status == "applied":
                continue
            if skip_blocking and _is_blocking(entry):
                continue
            out.append(
                QueueItem(
                    entry=entry,
                    position=pos,
                    blocking=_is_blocking(entry),
                    primary_tag=_primary_tag(entry),
                )
            )
            if len(out) >= limit:
                break
        return out

    def mark_applied(
        self,
        name: str,
        *,
        ability_index: int,
        batch_id: str | None = None,
        advance_cursor: bool = True,
        session_id: str | None = None,
        updated_at: str | None = None,
    ) -> CatalogEntry:
        sid = session_id or self.session_id
        when = updated_at or date.today().isoformat()
        entries = self.store.load_index()
        found: CatalogEntry | None = None
        out: list[CatalogEntry] = []
        key = name.casefold()

        for entry in entries:
            if entry.name.casefold() != key:
                out.append(entry)
                continue
            walk = WalkRef(
                status="applied",
                ability_index=ability_index,
                batch_id=batch_id or _batch_id_for_index(ability_index),
                session_id=sid,
            )
            found = CatalogEntry(
                name=entry.name,
                url=entry.url,
                category_path=entry.category_path,
                letter_bucket=entry.letter_bucket,
                source_license=entry.source_license,
                attribution=entry.attribution,
                fanon=entry.fanon,
                summary=entry.summary,
                schema_draft=entry.schema_draft,
                policy_tags=entry.policy_tags,
                walk=walk,
            )
            out.append(found)

        if found is None:
            raise KeyError(f"catalog entry not found: {name}")

        self.store.save_index(sorted(out, key=lambda e: e.name.casefold()))

        if advance_cursor:
            pages = walkable_entries(out)
            next_name = None
            for i, e in enumerate(pages):
                if e.name.casefold() == key:
                    if i + 1 < len(pages):
                        next_name = pages[i + 1].name
                    break
            cursor = CatalogCursor(
                session_id=sid,
                category="Absorption",
                last_applied_name=found.name,
                last_ability_index=ability_index,
                next_name=next_name,
                updated_at=when,
            )
            self.store.save_cursor(cursor)

        return found

    def mark_skipped(
        self,
        name: str,
        *,
        advance_cursor: bool = True,
        ability_index: int | None = None,
        session_id: str | None = None,
        updated_at: str | None = None,
    ) -> CatalogEntry:
        sid = session_id or self.session_id
        when = updated_at or date.today().isoformat()
        entries = self.store.load_index()
        found: CatalogEntry | None = None
        out: list[CatalogEntry] = []
        key = name.casefold()
        for entry in entries:
            if entry.name.casefold() != key:
                out.append(entry)
                continue
            walk = WalkRef(
                status="skipped",
                ability_index=ability_index,
                batch_id=None,
                session_id=sid,
            )
            found = CatalogEntry(
                name=entry.name,
                url=entry.url,
                category_path=entry.category_path,
                letter_bucket=entry.letter_bucket,
                source_license=entry.source_license,
                attribution=entry.attribution,
                fanon=entry.fanon,
                summary=entry.summary,
                schema_draft=entry.schema_draft,
                policy_tags=entry.policy_tags,
                walk=walk,
            )
            out.append(found)
        if found is None:
            raise KeyError(f"catalog entry not found: {name}")
        self.store.save_index(sorted(out, key=lambda e: e.name.casefold()))
        if advance_cursor:
            pages = walkable_entries(out)
            next_name = None
            idx = ability_index
            cur = self.load_cursor()
            if idx is None and cur is not None:
                idx = cur.last_ability_index
            for i, e in enumerate(pages):
                if e.name.casefold() == key:
                    if i + 1 < len(pages):
                        next_name = pages[i + 1].name
                    break
            self.store.save_cursor(
                CatalogCursor(
                    session_id=sid,
                    category="Absorption",
                    last_applied_name=found.name,
                    last_ability_index=idx,
                    next_name=next_name,
                    updated_at=when,
                )
            )
        return found

    def sync_cursor_from_name(
        self,
        last_applied_name: str,
        *,
        ability_index: int | None = None,
        session_id: str | None = None,
    ) -> CatalogCursor:
        sid = session_id or self.session_id
        pages = self._pages()
        key = last_applied_name.casefold()
        next_name = None
        matched = None
        for i, e in enumerate(pages):
            if e.name.casefold() == key:
                matched = e.name
                if i + 1 < len(pages):
                    next_name = pages[i + 1].name
                break
        if matched is None:
            raise KeyError(f"not on walkable spine: {last_applied_name}")
        cursor = CatalogCursor(
            session_id=sid,
            category="Absorption",
            last_applied_name=matched,
            last_ability_index=ability_index,
            next_name=next_name,
            updated_at=date.today().isoformat(),
        )
        self.store.save_cursor(cursor)
        return cursor


def _batch_id_for_index(ability_index: int) -> str:
    if ability_index <= 0:
        return "batch-00"
    n = (ability_index - 1) // 10 + 1
    return f"batch-{n:02d}"


def open_walk_queue(
    repo_root: Path | None = None,
    *,
    session_id: str = "walk-001",
) -> WalkQueue:
    return WalkQueue(repo_root=repo_root, session_id=session_id)
