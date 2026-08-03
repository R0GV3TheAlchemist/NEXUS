import unittest

from nexus.policy.enforcement import evaluate_guards, enforce_policy
from nexus.policy.schema import normalize_policy


class TestPolicyEnforcement(unittest.TestCase):
    def test_evaluate_guards_detects_missing_context(self):
        policy = normalize_policy({
            "name": "guarded",
            "allow": ["ingest_ability"],
            "guards": ["source_verified", "schema_valid", "state_ready"],
        })
        failures = evaluate_guards(policy, {"source_verified": True, "schema_valid": False, "state_ready": True})
        self.assertEqual(failures, ["schema_valid"])

    def test_enforce_policy_denies_when_guard_fails(self):
        result = enforce_policy(
            {"name": "guarded", "allow": ["ingest_ability"], "role": "admin", "guards": ["source_verified"]},
            {"id": "u1", "role": "admin"},
            "ingest_ability",
            {"source_verified": False},
        )
        self.assertFalse(result["decision"])
        self.assertEqual(result["guard_failures"], ["source_verified"])

    def test_enforce_policy_allows_when_requirements_met(self):
        result = enforce_policy(
            {"name": "guarded", "allow": ["ingest_ability"], "role": "admin", "guards": ["source_verified", "schema_valid"]},
            {"id": "u1", "role": "admin"},
            "ingest_ability",
            {"source_verified": True, "schema_valid": True},
        )
        self.assertTrue(result["decision"])
        self.assertEqual(result["guard_failures"], [])


if __name__ == "__main__":
    unittest.main()
