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
    """Resolve repository root robustly.

    Walks upward from this file and from cwd looking for pyproject.toml or
    data/wiki_catalog. Falls back to cwd (with a clear last resort).
    """
    markers = ("pyproject.toml",)
    candidates: list[Path] = []
    here = Path(__file__).resolve().parent
    candidates.extend([here, *here.parents])
    try:
        cwd = Path.cwd().resolve()
        candidates.extend([cwd, *cwd.parents])
    except OSError:
        pass

    seen: set[Path] = set()
    for base in candidates:
        if base in seen:
            continue
        seen.add(base)
        if (base / "data" / "wiki_catalog").is_dir():
            return base
        if any((base / m).exists() for m in markers):
            return base
    return Path.cwd().resolve()


def absorption_root(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else default_repo_root()
    return (Path(root) / ABSORPTION_REL).resolve()


def ensure_absorption_layout(repo_root: Path | None = None) -> Path:
    """Create absorption catalog directories if missing. Returns absorption root."""
    base = absorption_root(repo_root)
    base.mkdir(parents=True, exist_ok=True)
    pages = base / PAGES_DIR_NAME
    pages.mkdir(exist_ok=True)
    gitkeep = pages / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")
    index = base / INDEX_NAME
    if not index.exists():
        index.write_text(
            "# Absorption catalog index (JSONL). Populate via scripts/discover_absorption.py\n",
            encoding="utf-8",
        )
    return base
