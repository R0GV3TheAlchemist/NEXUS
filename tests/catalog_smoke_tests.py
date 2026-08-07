"""Smoke tests for nexus.catalog (I1)."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from nexus.catalog import (
    CatalogCursor,
    CatalogEntry,
    CatalogStore,
    SchemaDraft,
    WalkRef,
    ensure_absorption_layout,
)
from nexus.catalog.models import POLICY_TAGS


class CatalogModelsTests(unittest.TestCase):
    def test_entry_round_trip(self) -> None:
        entry = CatalogEntry(
            name="Bio-Capacitor",
            url="https://powerlisting.fandom.com/wiki/Bio-Capacitor",
            letter_bucket="B",
            summary="Store ambient energy",
            schema_draft=SchemaDraft(
                family="energy_storage",
                stability="conditionally_stable",
                growth_tag="growth_oriented",
                subject_domains=("physics", "biology"),
                effects_hint={"chaos": -0.02, "order": 0.03},
                physics_analog="Biological capacitor",
            ),
            policy_tags=("resource_pool", "map_ok"),
            walk=WalkRef(
                status="applied",
                ability_index=72,
                batch_id="batch-08",
                session_id="walk-001",
            ),
        )
        restored = CatalogEntry.from_dict(entry.to_dict())
        self.assertEqual(restored.name, "Bio-Capacitor")
        self.assertEqual(restored.policy_tags, ("resource_pool", "map_ok"))
        self.assertEqual(restored.walk.ability_index, 72)
        self.assertEqual(restored.schema_draft.effects_hint["order"], 0.03)

    def test_rejects_unknown_policy_tag(self) -> None:
        with self.assertRaises(ValueError):
            CatalogEntry(
                name="X",
                url="https://example.com/X",
                policy_tags=("not_a_real_tag",),
            )

    def test_policy_tags_registry_non_empty(self) -> None:
        self.assertIn("ethics_reject", POLICY_TAGS)
        self.assertIn("map_ok", POLICY_TAGS)


class CatalogStoreTests(unittest.TestCase):
    def test_layout_and_cursor_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = ensure_absorption_layout(root)
            self.assertTrue((base / "pages").is_dir())
            self.assertTrue((base / "index.jsonl").exists())

            store = CatalogStore(repo_root=root)
            cursor = CatalogCursor(
                session_id="walk-001",
                category="Absorption",
                last_applied_name="Bio-Capacitor",
                last_ability_index=72,
                next_name="Bio-Energetic Conversion",
                updated_at="2026-08-07",
            )
            store.save_cursor(cursor)
            loaded = store.load_cursor()
            assert loaded is not None
            self.assertEqual(loaded.next_name, "Bio-Energetic Conversion")
            self.assertEqual(loaded.last_ability_index, 72)

    def test_index_append_and_get(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            entry = CatalogEntry(
                name="Bio-Capacitor",
                url="https://powerlisting.fandom.com/wiki/Bio-Capacitor",
                policy_tags=("map_ok",),
            )
            store.append_entry(entry)
            all_rows = store.load_index()
            self.assertEqual(len(all_rows), 1)
            found = store.get_by_name("bio-capacitor")
            assert found is not None
            self.assertEqual(found.name, "Bio-Capacitor")

    def test_store_does_not_import_simulation(self) -> None:
        """Catalog store must not import simulation / CoreState (docstrings OK)."""
        import nexus.catalog.store as store_mod

        source = Path(store_mod.__file__).read_text(encoding="utf-8")
        self.assertNotIn("nexus.simulation", source)
        self.assertNotIn("nexus.sim", source)
        import_corestate = re.compile(
            r"^\s*(from\s+\S+\s+import\s+.*\bCoreState\b|import\s+.*\bCoreState\b)",
            re.M,
        )
        self.assertIsNone(
            import_corestate.search(source),
            msg="store.py must not import CoreState",
        )


if __name__ == "__main__":
    unittest.main()
