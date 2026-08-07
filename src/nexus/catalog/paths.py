"""Filesystem layout for wiki catalogs."""

from __future__ import annotations

from pathlib import Path

ABSORPTION_REL = Path("data") / "wiki_catalog" / "absorption"

INDEX_NAME = "index.jsonl"
CURSOR_NAME = "cursor.json"
ATTRIBUTION_NAME = "ATTRIBUTION.md"
README_NAME = "README.md"
PAGES_DIR_NAME = "pages"


def default_repo_root() -> Path:
    """Resolve repo root from this file: src/nexus/catalog/paths.py → root."""
    return Path(__file__).resolve().parents[3]


def absorption_root(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else default_repo_root()
    return (root / ABSORPTION_REL).resolve()


def ensure_absorption_layout(repo_root: Path | None = None) -> Path:
    """Create absorption catalog directories if missing. Returns absorption root."""
    base = absorption_root(repo_root)
    base.mkdir(parents=True, exist_ok=True)
    (base / PAGES_DIR_NAME).mkdir(exist_ok=True)
    index = base / INDEX_NAME
    if not index.exists():
        index.write_text("", encoding="utf-8")
    return base
