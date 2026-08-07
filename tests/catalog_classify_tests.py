"""Tests for I4 fail-closed policy classifier."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.catalog.classify import classify_entry, classify_index, classify_text
from nexus.catalog.models import CatalogEntry, WalkRef
from nexus.catalog.store import CatalogStore


class ClassifyHeuristicTests(unittest.TestCase):
    def test_bio_capacitor_map_ok_resource(self) -> None:
        r = classify_text(
            "Bio-Capacitor",
            "The power to bio-absorb and store ambient energy for later use.",
        )
        self.assertIn("resource_pool", r.tags)
        self.assertIn("map_ok", r.tags)
        self.assertNotIn("ethics_reject", r.tags)
        self.assertEqual(r.primary, "resource_pool")

    def test_aura_absorption_ethics(self) -> None:
        r = classify_text(
            "Aura Absorption",
            "Absorb auras including spiritual essence, personality, and powers.",
        )
        self.assertIn("ethics_reject", r.tags)
        self.assertNotIn("map_ok", r.tags)

    def test_assimilative_infection_ethics_hr(self) -> None:
        r = classify_text(
            "Assimilative Infection",
            "Infect others and assimilate them contagiously.",
        )
        self.assertIn("ethics_reject", r.tags)

    def test_beauty_thievery(self) -> None:
        r = classify_text(
            "Beauty Thievery",
            "Taking away their targets' radiance, health, and vitality.",
        )
        self.assertIn("ethics_reject", r.tags)

    def test_absolute_absorption_needs_human_or_quarantine(self) -> None:
        r = classify_text("Absolute Absorption", "Absorb anything without limit.")
        self.assertTrue(
            "quarantine_named" in r.tags
            or "needs_human" in r.tags
            or "high_risk" in r.tags
        )
        self.assertNotIn("map_ok", r.tags)

    def test_stability_manipulation_stabilizer(self) -> None:
        r = classify_text(
            "Stability Manipulation",
            "Manipulate stability to keep systems stable.",
        )
        self.assertIn("stabilizer", r.tags)
        self.assertIn("map_ok", r.tags)

    def test_subcategory_structural(self) -> None:
        e = CatalogEntry(
            name="Category:Consumption",
            url="https://powerlisting.fandom.com/wiki/Category:Consumption",
            category_path=("Absorption", "_subcat"),
        )
        r = classify_entry(e)
        self.assertEqual(r.primary, "structural")
        self.assertEqual(r.tags, ())


class ClassifyIndexTests(unittest.TestCase):
    def test_index_write_preserves_walk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    CatalogEntry(
                        name="Bio-Capacitor",
                        url="https://powerlisting.fandom.com/wiki/Bio-Capacitor",
                        summary="Store ambient energy for later use.",
                        walk=WalkRef(
                            status="applied",
                            ability_index=72,
                            session_id="walk-001",
                        ),
                    ),
                    CatalogEntry(
                        name="Aura Absorption",
                        url="https://powerlisting.fandom.com/wiki/Aura_Absorption",
                        summary="Absorb auras and personality.",
                    ),
                ]
            )
            report, _ = classify_index(store, write=True)
            self.assertEqual(report.total, 2)
            bio = store.get_by_name("Bio-Capacitor")
            aura = store.get_by_name("Aura Absorption")
            assert bio is not None and aura is not None
            self.assertEqual(bio.walk.ability_index, 72)
            self.assertIn("map_ok", bio.policy_tags)
            self.assertIn("ethics_reject", aura.policy_tags)
            self.assertNotIn("map_ok", aura.policy_tags)


if __name__ == "__main__":
    unittest.main()
