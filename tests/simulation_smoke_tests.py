"""Smoke tests for the canonical Super-Simulation entrypoint.

These tests must stay import-safe and fast. They protect initialization and
a single ability ingest path so regressions fail clearly in CI smoke runs.
"""

from __future__ import annotations

import tempfile
import unittest


class TestSimulationSmoke(unittest.TestCase):
    def test_canonical_package_imports(self):
        from nexus.simulation import (
            NEXUSEngine,
            CoreState,
            SuperSimulation,
            initialize_super_simulation,
            primordial_baseline,
        )

        self.assertTrue(callable(initialize_super_simulation))
        self.assertTrue(callable(primordial_baseline))
        self.assertIsNotNone(NEXUSEngine)
        self.assertIsNotNone(CoreState)
        self.assertIsNotNone(SuperSimulation)

    def test_initialize_super_simulation(self):
        from nexus.simulation import initialize_super_simulation

        with tempfile.TemporaryDirectory() as tmp:
            sim = initialize_super_simulation(output_dir=tmp, use_primordial=True)
            snap = sim.snapshot()

        self.assertIn("chaos", snap)
        self.assertIn("order", snap)
        self.assertIn("time_step", snap)
        # Primordial baseline expectations
        self.assertGreaterEqual(snap["chaos"], 0.7)
        self.assertLessEqual(snap["order"], 0.3)
        self.assertEqual(snap["time_step"], 0)

    def test_ingest_payload_advances_state(self):
        from nexus.simulation import initialize_super_simulation

        payload = {
            "name": "Smoke Test Strength",
            "family": "physical",
            "subject_domains": ["physics", "biology"],
            "effects": {"order": 0.05, "chaos": -0.02},
            "stability": "stable",
            "growth_tag": "growth_oriented",
        }

        with tempfile.TemporaryDirectory() as tmp:
            sim = initialize_super_simulation(output_dir=tmp)
            before = sim.snapshot()
            result = sim.ingest_payload(payload, run_id="smoke-001")
            after = sim.snapshot()

        self.assertTrue(result["accepted"], msg=f"ingest rejected: {result}")
        self.assertEqual(result["run_id"], "smoke-001")
        self.assertAlmostEqual(after["order"], before["order"] + 0.05, places=5)
        self.assertAlmostEqual(after["chaos"], before["chaos"] - 0.02, places=5)
        self.assertEqual(after["time_step"], 1)

    def test_reject_invalid_payload_clearly(self):
        from nexus.simulation import initialize_super_simulation

        with tempfile.TemporaryDirectory() as tmp:
            sim = initialize_super_simulation(output_dir=tmp)
            result = sim.ingest_payload({"name": ""}, run_id="smoke-bad")

        self.assertFalse(result["accepted"])
        self.assertIn("issues", result)
        self.assertTrue(len(result["issues"]) > 0)

    def test_recommend_returns_list(self):
        from nexus.simulation import initialize_super_simulation

        with tempfile.TemporaryDirectory() as tmp:
            sim = initialize_super_simulation(output_dir=tmp)
            tips = sim.recommend()

        self.assertIsInstance(tips, list)
        self.assertGreaterEqual(len(tips), 1)
        self.assertIn("priority", tips[0])
        self.assertIn("focus", tips[0])
        self.assertIn("reason", tips[0])


if __name__ == "__main__":
    unittest.main()
