import unittest

from nexus.app.entrypoint import NexusApp
from nexus.domains.router import route_domain, load_domain_manifest


class TestDomainAwareWorkflow(unittest.TestCase):
    def test_route_domain_prefers_physics_then_cognition_then_metaphysics(self):
        self.assertEqual(route_domain({"subject_domains": ["physics", "cognition"]}), "physics")
        self.assertEqual(route_domain({"subject_domains": ["cognition", "metaphysics"]}), "cognition")
        self.assertEqual(route_domain({"subject_domains": ["metaphysics"]}), "metaphysics")
        self.assertEqual(route_domain({"subject_domains": []}), "physics")

    def test_load_domain_manifest_returns_domain_data(self):
        manifest = load_domain_manifest("cognition")
        self.assertEqual(manifest["name"], "cognition")
        self.assertEqual(manifest["status"], "skeleton")

    def test_workflow_processes_and_routes_ability(self):
        app = NexusApp()
        principal = {"id": "u1", "secret": "s", "role": "admin"}
        payload = {
            "name": "Absorption",
            "family": "Information Cognition",
            "subject_domains": ["cognition", "metaphysics"],
            "effects": {"intake": 1.0},
        }
        policy = {"allow": ["ingest_ability"], "role": "admin"}

        result = app.submit(principal, payload, policy)

        self.assertTrue(result["accepted"])
        self.assertEqual(route_domain(payload), "cognition")
        self.assertEqual(result["state"]["abilities"]["Absorption"]["subject_domains"][0], "cognition")


if __name__ == "__main__":
    unittest.main()
