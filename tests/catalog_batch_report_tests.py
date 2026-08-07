"""Tests for I6 batch report writer."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from nexus.catalog.batch_report import (
    BatchReportInput,
    ConsoleSnapshot,
    ability_range_for_batch,
    batch_number_for_ability_index,
    collect_batch_entries,
    render_batch_markdown,
    write_batch_from_catalog,
    write_batch_report,
)
from nexus.catalog.models import CatalogEntry, SchemaDraft, WalkRef
from nexus.catalog.store import CatalogStore


def _applied(name: str, idx: int, tags: tuple[str, ...] = ("map_ok",)) -> CatalogEntry:
    return CatalogEntry(
        name=name,
        url=f"https://powerlisting.fandom.com/wiki/{name.replace(' ', '_')}",
        summary=f"Summary for {name}",
        policy_tags=tags,
        schema_draft=SchemaDraft(
            family="test",
            stability="conditionally_stable",
            growth_tag="growth_oriented",
        ),
        walk=WalkRef(
            status="applied",
            ability_index=idx,
            batch_id=f"batch-{(idx - 1) // 10 + 1:02d}",
            session_id="walk-001",
        ),
    )


class BatchMathTests(unittest.TestCase):
    def test_batch_number(self) -> None:
        self.assertEqual(batch_number_for_ability_index(70), 7)
        self.assertEqual(batch_number_for_ability_index(71), 8)
        self.assertEqual(ability_range_for_batch(7), (61, 70))


class BatchRenderTests(unittest.TestCase):
    def test_markdown_contains_rows_and_state(self) -> None:
        entries = [
            _applied("Bio-Capacitor", 72, ("resource_pool", "map_ok")),
            _applied("Stability Manipulation", 71, ("stabilizer", "map_ok")),
        ]
        md = render_batch_markdown(
            BatchReportInput(
                batch_number=8,
                abilities=entries,
                core_state_end={
                    "chaos": 0.72,
                    "order": 0.73,
                    "void": 0.0,
                    "light": 0.78,
                    "balance": 0.32,
                    "law": 1.0,
                    "magic": 1.0,
                    "time_step": 75,
                },
                console=ConsoleSnapshot(
                    pace="allow", high_risk_count=7, high_risk_cap=3
                ),
                narrative="Batch 8 partial fixture.",
            )
        )
        self.assertIn("# Batch 08", md)
        self.assertIn("Bio-Capacitor", md)
        self.assertIn("Stability Manipulation", md)
        self.assertIn("| Chaos | 0.72 |", md)
        self.assertIn("high-risk **7 / 3**", md)

    def test_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "docs" / "walks"
            entries = [_applied(f"Ability {i}", i) for i in range(61, 71)]
            result = write_batch_report(
                BatchReportInput(batch_number=7, abilities=entries),
                repo_root=root,
                out_dir=out,
                write_json=True,
            )
            self.assertTrue(result.markdown_path.exists())
            self.assertTrue(result.json_path and result.json_path.exists())
            self.assertEqual(result.ability_count, 10)
            body = result.markdown_path.read_text(encoding="utf-8")
            self.assertIn("Ability 61", body)
            self.assertIn("Ability 70", body)
            payload = json.loads(result.json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["batch_number"], 7)
            self.assertEqual(len(payload["abilities"]), 10)

    def test_from_catalog_store(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    _applied("A", 61, ("ethics_reject",)),
                    _applied("B", 62, ("map_ok",)),
                    _applied("Outside", 80, ("map_ok",)),
                ]
            )
            got = collect_batch_entries(store, 7)
            self.assertEqual([e.name for e in got], ["A", "B"])
            result = write_batch_from_catalog(
                7, repo_root=root, store=store, write_json=False
            )
            self.assertEqual(result.ability_count, 2)
            self.assertTrue(result.markdown_path.exists())


if __name__ == "__main__":
    unittest.main()
