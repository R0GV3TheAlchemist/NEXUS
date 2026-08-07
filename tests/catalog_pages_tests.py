"""Offline tests for I3 / I3.1 page fetch, parse fallback, and enrich."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from nexus.catalog.enrich import apply_documents_to_index, enrich_absorption_pages
from nexus.catalog.models import CatalogEntry, WalkRef
from nexus.catalog.pages import build_extracts_url, build_parse_url, fetch_page_documents, html_to_first_paragraph, parse_extracts_payload, parse_parse_payload, slugify_title
from nexus.catalog.store import CatalogStore
FIXTURES = Path(__file__).resolve().parent / "fixtures"

class ParseExtractTests(unittest.TestCase):
    def test_parse_bio_capacitor(self):
        doc = parse_extracts_payload((FIXTURES / "page_extract_bio_capacitor.json").read_bytes())[0]
        self.assertEqual(doc.title, "Bio-Capacitor"); self.assertIn("ambient energy", doc.summary); self.assertIn("Absorption", doc.categories)
    def test_parse_skips_missing(self):
        titles = {d.title for d in parse_extracts_payload((FIXTURES / "page_extract_batch.json").read_bytes())}
        self.assertIn("Absorption", titles); self.assertNotIn("Not A Real Page", titles)
    def test_parse_api_fallback(self):
        doc = parse_parse_payload((FIXTURES / "page_parse_absolute_absorption.json").read_bytes())
        assert doc is not None
        self.assertIn("without limit", doc.summary); self.assertNotIn("second paragraph", doc.summary); self.assertIn("Absolute Powers", doc.categories)
    def test_html_first_paragraph(self):
        self.assertEqual(html_to_first_paragraph("<div><p>First &amp; useful.</p><p>Second.</p></div>"), "First & useful.")
    def test_slugify(self): self.assertEqual(slugify_title("Bio-Capacitor"), "Bio-Capacitor")
    def test_build_urls(self):
        self.assertIn("extracts", build_extracts_url(["Bio-Capacitor"])); self.assertIn("action=parse", build_parse_url("Absolute Absorption"))

class EnrichTests(unittest.TestCase):
    def test_apply_preserves_walk_and_writes_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CatalogStore(repo_root=Path(tmp))
            store.save_index([CatalogEntry(name="Bio-Capacitor", url="https://powerlisting.fandom.com/wiki/Bio-Capacitor", policy_tags=("map_ok",), walk=WalkRef(status="applied", ability_index=72, session_id="walk-001"))])
            report = apply_documents_to_index(store, parse_extracts_payload((FIXTURES / "page_extract_bio_capacitor.json").read_bytes()), write_sidecars=True)
            self.assertEqual(report.updated, 1); self.assertEqual(report.written_sidecars, 1)
            entry = store.get_by_name("Bio-Capacitor"); assert entry is not None
            self.assertIn("ambient energy", entry.summary); self.assertEqual(entry.walk.ability_index, 72)
    def test_enrich_with_injected_fetch(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CatalogStore(repo_root=Path(tmp)); store.save_index([CatalogEntry(name="Absorption", url="https://powerlisting.fandom.com/wiki/Absorption"), CatalogEntry(name="Bio-Energetic Conversion", url="https://powerlisting.fandom.com/wiki/Bio-Energetic_Conversion")])
            payload = (FIXTURES / "page_extract_batch.json").read_bytes()
            report = enrich_absorption_pages(repo_root=Path(tmp), fetch=lambda _: payload, write_sidecars=True)
            self.assertEqual(report.fetched, 2)
            entry = store.get_by_name("Absorption"); assert entry is not None
            self.assertIn("absorb anything", entry.summary)
    def test_blank_extract_falls_back_to_parse(self):
        extract = (FIXTURES / "page_extract_blank_absolute.json").read_bytes(); parsed = (FIXTURES / "page_parse_absolute_absorption.json").read_bytes(); calls=[]
        def fetch(url): calls.append(url); return parsed if "action=parse" in url else extract
        docs = fetch_page_documents(["Absolute Absorption"], fetch=fetch)
        self.assertEqual(len(calls), 2); self.assertIn("without limit", docs[0].summary)
    def test_fetch_page_documents_injected(self):
        payload=(FIXTURES / "page_extract_bio_capacitor.json").read_bytes()
        self.assertEqual(fetch_page_documents(["Bio-Capacitor"], fetch=lambda _: payload)[0].title, "Bio-Capacitor")

if __name__ == "__main__": unittest.main()
