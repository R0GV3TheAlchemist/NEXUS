"""Offline tests for I2 category discovery + index merge."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.catalog.discover import (
    build_categorymembers_url,
    discover_category_members,
    pages_only,
    parse_categorymembers_payload,
    subcats_only,
)
from nexus.catalog.models import CatalogEntry, WalkRef
from nexus.catalog.store import CatalogStore
from nexus.catalog.sync import merge_members_into_index, member_to_entry

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class ParseTests(unittest.TestCase):
    def test_parse_fixture_page1(self) -> None:
        raw = (FIXTURES / "absorption_categorymembers_page1.json").read_bytes()
        members, cont = parse_categorymembers_payload(raw)
        self.assertIsNone(cont)
        self.assertEqual(len(members), 5)
        self.assertEqual(len(pages_only(members)), 3)
        self.assertEqual(len(subcats_only(members)), 2)
        bio = next(m for m in members if m.title == "Bio-Capacitor")
        self.assertIn("Bio-Capacitor", bio.url)

    def test_build_url_contains_category(self) -> None:
        url = build_categorymembers_url(category_title="Category:Absorption")
        self.assertIn("categorymembers", url)
        self.assertIn("Category%3AAbsorption", url)


class DiscoverPaginationTests(unittest.TestCase):
    def test_pagination_with_injected_fetch(self) -> None:
        page2 = (FIXTURES / "absorption_categorymembers_page2.json").read_bytes()
        page1_final = (FIXTURES / "absorption_categorymembers_page1.json").read_bytes()
        calls: list[str] = []

        def fetch(url: str) -> bytes:
            calls.append(url)
            if "cmcontinue" in url:
                return page1_final
            return page2

        members = discover_category_members(fetch=fetch, pause_seconds=0.0)
        self.assertEqual(len(calls), 2)
        titles = {m.title for m in members}
        self.assertIn("Absolute Absorption", titles)
        self.assertIn("Bio-Capacitor", titles)


class MergeTests(unittest.TestCase):
    def test_merge_preserves_walk_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.append_entry(
                CatalogEntry(
                    name="Bio-Capacitor",
                    url="https://powerlisting.fandom.com/wiki/Bio-Capacitor",
                    policy_tags=("map_ok", "resource_pool"),
                    walk=WalkRef(
                        status="applied",
                        ability_index=72,
                        batch_id="batch-08",
                        session_id="walk-001",
                    ),
                )
            )
            raw = (FIXTURES / "absorption_categorymembers_page1.json").read_bytes()
            members, _ = parse_categorymembers_payload(raw)
            report = merge_members_into_index(store, members)
            self.assertGreaterEqual(report.added, 2)
            bio = store.get_by_name("Bio-Capacitor")
            assert bio is not None
            self.assertEqual(bio.walk.status, "applied")
            self.assertEqual(bio.walk.ability_index, 72)
            self.assertIn("map_ok", bio.policy_tags)

    def test_member_to_entry_pending(self) -> None:
        raw = (FIXTURES / "absorption_categorymembers_page1.json").read_bytes()
        members, _ = parse_categorymembers_payload(raw)
        page = pages_only(members)[0]
        entry = member_to_entry(page)
        self.assertEqual(entry.walk.status, "pending")
        self.assertEqual(entry.policy_tags, ())


if __name__ == "__main__":
    unittest.main()
