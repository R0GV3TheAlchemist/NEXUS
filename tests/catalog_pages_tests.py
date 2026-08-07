"""Offline tests for I3 page fetch/parse + enrich."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexus.catalog.enrich import apply_documents_to_index, enrich_absorption_pages
from nexus.catalog.models import CatalogEntry, WalkRef
from nexus.catalog.pages import (
    build_extracts_url,
    fetch_page_documents,
    parse_extracts_payload,
    slugify_title,
)
from nexus.catalog.store import CatalogStore

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class ParseExtractTests(unittest.TestCase):
    def test_parse_bio_capacitor(self) -> None:
        raw = (FIXTURES / "page_extract_bio_capacitor.json").read_bytes()
        docs = parse_extracts_payload(raw)
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.title, "Bio-Capacitor")
        self.assertIn("ambient energy", doc.summary)
        self.assertIn("Absorption", doc.categories)
        self.assertIn("Bio-Capacitor", doc.url)

    def test_parse_skips_missing(self) -> None:
        raw = (FIXTURES / "page_extract_batch.json").read_bytes()
        docs = parse_extracts_payload(raw)
        titles = {d.title for d in docs}
        self.assertIn("Absorption", titles)
        self.assertNotIn("Not A Real Page", titles)

    def test_slugify(self) -> None:
        self.assertEqual(slugify_title("Bio-Capacitor"), "Bio-Capacitor")
        self.assertTrue(slugify_title("Foo Bar").startswith("Foo"))

    def test_build_extracts_url(self) -> None:
        url = build_extracts_url(["Bio-Capacitor", "Absorption"])
        self.assertIn("extracts", url)
        self.assertIn("Bio-Capacitor", url)


class EnrichTests(unittest.TestCase):
    def test_apply_preserves_walk_and_writes_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    CatalogEntry(
                        name="Bio-Capacitor",
                        url="https://powerlisting.fandom.com/wiki/Bio-Capacitor",
                        policy_tags=("map_ok",),
                        walk=WalkRef(
                            status="applied",
                            ability_index=72,
                            session_id="walk-001",
                        ),
                    )
                ]
            )
            raw = (FIXTURES / "page_extract_bio_capacitor.json").read_bytes()
            docs = parse_extracts_payload(raw)
            report = apply_documents_to_index(store, docs, write_sidecars=True)
            self.assertEqual(report.updated, 1)
            self.assertEqual(report.written_sidecars, 1)
            entry = store.get_by_name("Bio-Capacitor")
            assert entry is not None
            self.assertIn("ambient energy", entry.summary)
            self.assertEqual(entry.walk.ability_index, 72)
            self.assertIn("map_ok", entry.policy_tags)
            side = list((store.root / "pages").glob("*.json"))
            self.assertEqual(len(side), 1)

    def test_enrich_with_injected_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = CatalogStore(repo_root=root)
            store.save_index(
                [
                    CatalogEntry(
                        name="Absorption",
                        url="https://powerlisting.fandom.com/wiki/Absorption",
                    ),
                    CatalogEntry(
                        name="Bio-Energetic Conversion",
                        url="https://powerlisting.fandom.com/wiki/Bio-Energetic_Conversion",
                    ),
                ]
            )
            payload = (FIXTURES / "page_extract_batch.json").read_bytes()

            def fetch(_url: str) -> bytes:
                return payload

            report = enrich_absorption_pages(
                repo_root=root,
                fetch=fetch,
                write_sidecars=True,
            )
            self.assertEqual(report.fetched, 2)
            self.assertGreaterEqual(report.updated, 1)
            abs_entry = store.get_by_name("Absorption")
            assert abs_entry is not None
            self.assertIn("absorb anything", abs_entry.summary)

    def test_fetch_page_documents_injected(self) -> None:
        payload = (FIXTURES / "page_extract_bio_capacitor.json").read_bytes()

        def fetch(_url: str) -> bytes:
            return payload

        docs = fetch_page_documents(["Bio-Capacitor"], fetch=fetch)
        self.assertEqual(docs[0].title, "Bio-Capacitor")


if __name__ == "__main__":
    unittest.main()
