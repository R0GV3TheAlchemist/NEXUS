"""I7 offline pipeline smoke: store → classify → queue → batch (no network)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.catalog.batch_report import write_batch_from_catalog
from nexus.catalog.classify import classify_index
from nexus.catalog.models import CatalogCursor, CatalogEntry
from nexus.catalog.store import CatalogStore
from nexus.catalog.walk_queue import WalkQueue


class CatalogPipelineSmokeTests(unittest.TestCase):
    def test_end_to_end_offline_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    CatalogEntry(
                        name="Bio-Capacitor",
                        url="https://powerlisting.fandom.com/wiki/Bio-Capacitor",
                        summary="Store ambient energy for later use.",
                    ),
                    CatalogEntry(
                        name="Aura Absorption",
                        url="https://powerlisting.fandom.com/wiki/Aura_Absorption",
                        summary="Absorb auras and personality from others.",
                    ),
                    CatalogEntry(
                        name="Bio-Energetic Conversion",
                        url="https://powerlisting.fandom.com/wiki/Bio-Energetic_Conversion",
                        summary="Convert absorbed bio-energy.",
                    ),
                ]
            )
            store.save_cursor(
                CatalogCursor(
                    session_id="walk-001",
                    category="Absorption",
                    last_applied_name=None,
                    last_ability_index=None,
                    next_name="Aura Absorption",
                    updated_at="2026-08-07",
                )
            )

            report, _ = classify_index(store, write=True)
            self.assertGreaterEqual(report.total, 3)

            bio = store.get_by_name("Bio-Capacitor")
            aura = store.get_by_name("Aura Absorption")
            assert bio is not None and aura is not None
            self.assertIn("map_ok", bio.policy_tags)
            self.assertIn("ethics_reject", aura.policy_tags)

            q = WalkQueue(store=store, session_id="walk-001")
            q.sync_cursor_from_name("Aura Absorption", ability_index=67)
            nxt = q.peek()
            assert nxt is not None
            self.assertEqual(nxt.name, "Bio-Capacitor")

            q.mark_applied("Bio-Capacitor", ability_index=72)
            cur = q.load_cursor()
            assert cur is not None
            self.assertEqual(cur.last_applied_name, "Bio-Capacitor")
            self.assertEqual(cur.next_name, "Bio-Energetic Conversion")

            q.mark_applied(
                "Aura Absorption", ability_index=67, advance_cursor=False
            )
            result = write_batch_from_catalog(
                7,
                repo_root=root,
                store=store,
                write_json=True,
            )
            self.assertGreaterEqual(result.ability_count, 1)
            self.assertTrue(result.markdown_path.exists())
            body = result.markdown_path.read_text(encoding="utf-8")
            self.assertIn("# Batch 07", body)
            self.assertIn("Aura Absorption", body)

    def test_imports_public_surface(self) -> None:
        import nexus.catalog as cat

        for name in (
            "CatalogStore",
            "classify_index",
            "WalkQueue",
            "write_batch_report",
            "discover_absorption_members",
            "enrich_absorption_pages",
        ):
            self.assertTrue(hasattr(cat, name), msg=name)


if __name__ == "__main__":
    unittest.main()
