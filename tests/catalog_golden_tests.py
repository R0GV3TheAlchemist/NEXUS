"""I7 golden tests: batch report structure from a fixed Batch 7 ledger."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from nexus.catalog.batch_report import (
    BatchReportInput,
    ConsoleSnapshot,
    render_batch_markdown,
    write_batch_report,
)
from nexus.catalog.models import CatalogEntry, SchemaDraft, WalkRef

FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOLDEN = FIXTURES / "golden_batch07_names.json"

REQUIRED_HEADINGS = [
    "# Batch 07 — Primordial Walk Catalog",
    "## Ability table",
    "### Wiki references (research)",
    "## Batch narrative",
    "## CoreState",
    "## Policy summary",
    "## Console / operator",
    "## Recommendations",
    "## Build implications (evidence only)",
    "## Files",
    "## Batch 7 closed",
]


def _entries_from_golden() -> list[CatalogEntry]:
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    out: list[CatalogEntry] = []
    for row in data["abilities"]:
        tags = tuple(row.get("policy_tags") or ())
        stability = "rule_breaking" if (
            set(tags) & {"ethics_reject", "high_risk", "quarantine_named"}
        ) else "stable"
        growth = (
            "growth_oriented"
            if "stabilizer" in tags or "map_ok" in tags
            else "destructive_oriented"
        )
        name = row["name"]
        idx = int(row["ability_index"])
        out.append(
            CatalogEntry(
                name=name,
                url=f"https://powerlisting.fandom.com/wiki/{name.replace(' ', '_')}",
                summary=f"Golden fixture summary for {name}.",
                policy_tags=tags,
                schema_draft=SchemaDraft(
                    family="golden",
                    stability=stability if stability in {
                        "stable", "conditionally_stable", "rule_breaking"
                    } else "conditionally_stable",
                    growth_tag=growth if growth in {
                        "growth_oriented", "context_dependent", "destructive_oriented"
                    } else "context_dependent",
                ),
                walk=WalkRef(
                    status="applied",
                    ability_index=idx,
                    batch_id="batch-07",
                    session_id="walk-001",
                ),
            )
        )
    return out


class GoldenBatch07Tests(unittest.TestCase):
    def test_golden_has_ten_abilities(self) -> None:
        entries = _entries_from_golden()
        self.assertEqual(len(entries), 10)
        self.assertEqual(entries[0].walk.ability_index, 61)
        self.assertEqual(entries[-1].walk.ability_index, 70)

    def test_markdown_has_required_sections_and_names(self) -> None:
        entries = _entries_from_golden()
        md = render_batch_markdown(
            BatchReportInput(
                batch_number=7,
                abilities=entries,
                core_state_end={
                    "chaos": 1.0,
                    "order": 0.49,
                    "void": 0.0,
                    "light": 0.67,
                    "balance": 0.12,
                    "law": 1.0,
                    "magic": 1.0,
                    "time_step": 70,
                },
                console=ConsoleSnapshot(
                    pace="allow",
                    high_risk_count=7,
                    high_risk_cap=3,
                    session_id="walk-001",
                ),
                narrative="Golden Batch 7 fixture for CI.",
                closed_at="2026-08-07",
            )
        )
        for heading in REQUIRED_HEADINGS:
            self.assertIn(heading, md, msg=f"missing heading: {heading}")
        for e in entries:
            self.assertIn(e.name, md)
        self.assertIn("| Chaos | 1.0 |", md)
        self.assertIn("high-risk **7 / 3**", md)
        self.assertIn("Assimilation Immunity", md)
        self.assertTrue("reject" in md)

    def test_write_batch_07_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "docs" / "walks"
            result = write_batch_report(
                BatchReportInput(
                    batch_number=7,
                    abilities=_entries_from_golden(),
                    console=ConsoleSnapshot(high_risk_count=7, high_risk_cap=3),
                    closed_at="2026-08-07",
                ),
                repo_root=root,
                out_dir=out,
                write_json=True,
            )
            self.assertEqual(result.ability_count, 10)
            self.assertTrue(result.markdown_path.exists())
            self.assertTrue(result.json_path and result.json_path.exists())
            payload = json.loads(result.json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["batch_number"], 7)
            self.assertEqual(payload["ability_range"], [61, 70])
            names = [a["name"] for a in payload["abilities"]]
            self.assertEqual(names[0], "Antimatter Absorption")
            self.assertEqual(names[-1], "Bio-Absorbing Replication")


if __name__ == "__main__":
    unittest.main()
