import unittest

from nexus.app.runner import NexusRunner, run_ability


class TestRunner(unittest.TestCase):
    def test_run_ability_executes_pipeline(self):
        principal = {"id": "u1", "secret": "s", "role": "admin"}
        payload = {
            "name": "Absorption",
            "family": "Information Cognition",
            "subject_domains": ["physics"],
            "effects": {"intake": 1.0},
        }
        policy = {"allow": ["ingest_ability"], "role": "admin", "guards": ["schema_valid"]}
        result = run_ability(principal, payload, policy)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["validation"]["accepted"], True)

    def test_runner_wraps_app(self):
        runner = NexusRunner()
        self.assertIsNotNone(runner.app)


if __name__ == "__main__":
    unittest.main()
