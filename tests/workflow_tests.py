import unittest

from nexus.app.entrypoint import NexusApp


class TestWorkflow(unittest.TestCase):
    def test_rejects_invalid_payload(self):
        app = NexusApp()
        result = app.submit({"id": "u1", "secret": "s", "role": "admin"}, {"name": "Absorption"}, {"allow": ["ingest_ability"], "role": "admin"})
        self.assertFalse(result["accepted"])
        self.assertEqual(result["validation"]["accepted"], False)

    def test_accepts_valid_payload_with_policy(self):
        app = NexusApp()
        result = app.submit({"id": "u1", "secret": "s", "role": "admin"}, {
            "name": "Absorption",
            "family": "Information Cognition",
            "subject_domains": ["physics", "cognition"],
            "effects": {"intake": 1.0},
        }, {"allow": ["ingest_ability"], "role": "admin"})
        self.assertTrue(result["accepted"])
        self.assertIn("state", result)


if __name__ == "__main__":
    unittest.main()
