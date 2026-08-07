"""I4.1 policy classifier tests."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from nexus.catalog.classify import classify_entry,classify_index,classify_text
from nexus.catalog.models import CatalogEntry,WalkRef
from nexus.catalog.store import CatalogStore
class ClassifyTests(unittest.TestCase):
 def test_enriched_capacitor_is_map_ok(self):
  r=classify_text("Bio-Capacitor","The power to bio-absorb and store ambient energy for later use."); self.assertIn("resource_pool",r.tags); self.assertIn("map_ok",r.tags); self.assertNotIn("needs_human",r.tags)
 def test_empty_summary_needs_human(self):
  r=classify_text("Unknown Absorption"); self.assertIn("needs_human",r.tags); self.assertNotIn("map_ok",r.tags)
 def test_ethics_not_map_ok(self):
  r=classify_text("Aura Absorption","Absorb auras including personality."); self.assertIn("ethics_reject",r.tags); self.assertNotIn("map_ok",r.tags)
 def test_absolute_not_map_ok(self):
  r=classify_text("Absolute Absorption","Absorb anything without limit."); self.assertTrue(set(r.tags)&{"quarantine_named","high_risk","needs_human"}); self.assertNotIn("map_ok",r.tags)
 def test_structural(self):
  r=classify_entry(CatalogEntry(name="Category:X",url="https://x",category_path=("Absorption","_subcat"))); self.assertEqual(r.primary,"structural")
 def test_index_preserves_walk(self):
  with tempfile.TemporaryDirectory() as tmp:
   store=CatalogStore(repo_root=Path(tmp)); store.save_index([CatalogEntry(name="Bio-Capacitor",url="https://x",summary="Store ambient energy.",walk=WalkRef(status="applied",ability_index=72,session_id="walk-001")),CatalogEntry(name="Unknown",url="https://x")]); classify_index(store)
   bio=store.get_by_name("Bio-Capacitor"); unknown=store.get_by_name("Unknown"); assert bio and unknown
   self.assertEqual(bio.walk.ability_index,72); self.assertIn("map_ok",bio.policy_tags); self.assertIn("needs_human",unknown.policy_tags)
 def test_invasive_biological_absorption_rejects(self):
  for name in (
   "Blood Absorption",
   "Bodily Fluid Absorption",
   "Brain Absorption",
  ):
   result=classify_text(name,"Nonempty catalog summary.")
   self.assertIn("ethics_reject",result.tags)
   self.assertNotIn("map_ok",result.tags)

if __name__=="__main__": unittest.main()
