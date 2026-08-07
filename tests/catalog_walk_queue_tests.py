"""Tests for I5 Walk queue."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.catalog.models import CatalogCursor, CatalogEntry
from nexus.catalog.store import CatalogStore
from nexus.catalog.walk_queue import WalkQueue, walkable_entries


def _entry(name: str, **kwargs) -> CatalogEntry:
    return CatalogEntry(
        name=name,
        url=f"https://powerlisting.fandom.com/wiki/{name.replace(' ', '_')}",
        **kwargs,
    )


class WalkQueueTests(unittest.TestCase):
    def test_peek_after_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    _entry("Absorption"),
                    _entry("Bio-Capacitor", policy_tags=("map_ok", "resource_pool")),
                    _entry("Bio-Energetic Conversion", policy_tags=("map_ok",)),
                    _entry(
                        "Category:Consumption",
                        category_path=("Absorption", "_subcat"),
                    ),
                    _entry("Aura Absorption", policy_tags=("ethics_reject",)),
                ]
            )
            store.save_cursor(
                CatalogCursor(
                    session_id="walk-001",
                    category="Absorption",
                    last_applied_name="Bio-Capacitor",
                    last_ability_index=72,
                    next_name="Bio-Energetic Conversion",
                    updated_at="2026-08-07",
                )
            )
            q = WalkQueue(store=store)
            item = q.peek()
            assert item is not None
            self.assertEqual(item.name, "Bio-Energetic Conversion")

    def test_skip_blocking_peek(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    _entry("A-One", policy_tags=("ethics_reject",)),
                    _entry("B-Two", policy_tags=("map_ok",)),
                ]
            )
            q = WalkQueue(store=store, session_id="walk-001")
            item = q.peek(skip_blocking=True)
            assert item is not None
            self.assertEqual(item.name, "B-Two")

    def test_mark_applied_advances_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    _entry("Bio-Capacitor"),
                    _entry("Bio-Energetic Conversion"),
                    _entry("Bio-Energetic Sourcing"),
                ]
            )
            q = WalkQueue(store=store)
            q.mark_applied("Bio-Capacitor", ability_index=72)
            cur = q.load_cursor()
            assert cur is not None
            self.assertEqual(cur.last_applied_name, "Bio-Capacitor")
            self.assertEqual(cur.next_name, "Bio-Energetic Conversion")
            self.assertEqual(cur.last_ability_index, 72)
            entry = store.get_by_name("Bio-Capacitor")
            assert entry is not None
            self.assertEqual(entry.walk.status, "applied")
            self.assertEqual(entry.walk.batch_id, "batch-08")

    def test_side_queue_does_not_advance_cursor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    _entry("Bio-Capacitor"),
                    _entry("Bio-Energetic Conversion"),
                    _entry(
                        "Stability Manipulation",
                        policy_tags=("stabilizer", "map_ok"),
                    ),
                ]
            )
            store.save_cursor(
                CatalogCursor(
                    session_id="walk-001",
                    category="Absorption",
                    last_applied_name="Bio-Capacitor",
                    last_ability_index=72,
                    next_name="Bio-Energetic Conversion",
                    updated_at="2026-08-07",
                )
            )
            q = WalkQueue(store=store)
            q.mark_applied(
                "Stability Manipulation",
                ability_index=71,
                advance_cursor=False,
            )
            cur = q.load_cursor()
            assert cur is not None
            self.assertEqual(cur.next_name, "Bio-Energetic Conversion")
            self.assertEqual(cur.last_applied_name, "Bio-Capacitor")

    def test_walkable_skips_subcats(self) -> None:
        rows = [
            _entry("Zed"),
            _entry("Category:X", category_path=("Absorption", "_subcat")),
        ]
        pages = walkable_entries(rows)
        self.assertEqual([p.name for p in pages], ["Zed"])


if __name__ == "__main__":
    unittest.main()
