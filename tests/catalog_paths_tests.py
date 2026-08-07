"""Tests for catalog path resolution (error-correction)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.catalog.paths import absorption_root, default_repo_root, ensure_absorption_layout
from nexus.catalog.store import CatalogStore


class PathsTests(unittest.TestCase):
    def test_ensure_layout_creates_pages_gitkeep_and_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = ensure_absorption_layout(root)
            self.assertTrue((base / "pages" / ".gitkeep").exists())
            self.assertTrue((base / "index.jsonl").exists())
            store = CatalogStore(repo_root=root)
            self.assertEqual(store.load_index(), [])

    def test_absorption_root_under_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
            ar = absorption_root(root)
            self.assertEqual(ar, (root / "data" / "wiki_catalog" / "absorption").resolve())

    def test_default_repo_root_finds_marker(self) -> None:
        root = default_repo_root()
        self.assertTrue(root.exists())


if __name__ == "__main__":
    unittest.main()
