"""Load/save catalog index and cursor. No CoreState mutation. No network."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from nexus.catalog.models import CatalogCursor, CatalogEntry
from nexus.catalog.paths import (
    CURSOR_NAME,
    INDEX_NAME,
    absorption_root,
    ensure_absorption_layout,
)


class CatalogStore:
    """Filesystem-backed Absorption catalog."""

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = Path(repo_root).resolve() if repo_root is not None else None
        self.root = ensure_absorption_layout(self.repo_root)

    @property
    def index_path(self) -> Path:
        return self.root / INDEX_NAME

    @property
    def cursor_path(self) -> Path:
        return self.root / CURSOR_NAME

    def load_index(self) -> list[CatalogEntry]:
        path = self.index_path
        if not path.exists() or path.stat().st_size == 0:
            return []
        entries: list[CatalogEntry] = []
        with path.open(encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"invalid JSONL at {path}:{line_no}: {exc}"
                    ) from exc
                if not isinstance(data, dict):
                    raise ValueError(
                        f"invalid JSONL at {path}:{line_no}: expected object"
                    )
                entries.append(CatalogEntry.from_dict(data))
        return entries

    def save_index(self, entries: Iterable[CatalogEntry]) -> None:
        lines = [
            json.dumps(e.to_dict(), ensure_ascii=False, sort_keys=True)
            for e in entries
        ]
        text = "\n".join(lines)
        if text:
            text += "\n"
        else:
            text = (
                "# Absorption catalog index (JSONL). "
                "Populate via scripts/discover_absorption.py\n"
            )
        self.index_path.write_text(text, encoding="utf-8")

    def append_entry(self, entry: CatalogEntry) -> None:
        row = json.dumps(entry.to_dict(), ensure_ascii=False, sort_keys=True)
        with self.index_path.open("a", encoding="utf-8") as fh:
            fh.write(row + "\n")

    def load_cursor(self) -> CatalogCursor | None:
        path = self.cursor_path
        if not path.exists():
            return None
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return None
        data = json.loads(raw)
        return CatalogCursor.from_dict(data)

    def save_cursor(self, cursor: CatalogCursor) -> None:
        payload = json.dumps(
            cursor.to_dict(), ensure_ascii=False, indent=2, sort_keys=True
        )
        self.cursor_path.write_text(payload + "\n", encoding="utf-8")

    def get_by_name(self, name: str) -> CatalogEntry | None:
        key = name.strip().casefold()
        for entry in self.load_index():
            if entry.name.casefold() == key:
                return entry
        return None


def open_absorption_store(repo_root: Path | None = None) -> CatalogStore:
    """Factory matching absorption_root resolution."""
    _ = absorption_root(repo_root)
    return CatalogStore(repo_root=repo_root)
