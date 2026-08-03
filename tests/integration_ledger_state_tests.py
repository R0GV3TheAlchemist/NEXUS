import unittest

from nexus.app.entrypoint import NexusApp
from nexus.domains.router import route_domain


class TestLedgerStateIntegration(unittest.TestCase):
    def test_end_to_end_pipeline_records_state_and_ledger(self):
        app = NexusApp()
        principal = {"id": "u1", "secret": "s", "role": "admin"}
        payload = {
            "name": "Absorption",
            "family": "Information Cognition",
            "subject_domains": ["physics", "cognition"],
            "effects": {"intake": 1.0},
        }
        policy = {"allow": ["ingest_ability"], "role": "admin"}

        result = app.submit(principal, payload, policy)

        self.assertTrue(result["accepted"])
        self.assertEqual(route_domain(payload), "physics")
        self.assertEqual(len(app.ledger.entries), 1)
        self.assertEqual(app.ledger.entries[0]["outcome"], "approved")
        self.assertIn("Absorption", app.engine.state.abilities)
        self.assertEqual(app.engine.state.ledger[0]["accepted"], True)
        self.assertEqual(result["state"]["abilities"]["Absorption"]["name"], "Absorption")


if __name__ == "__main__":
    unittest.main()
