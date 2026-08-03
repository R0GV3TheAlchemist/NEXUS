import unittest

from nexus.policy.schema import normalize_policy
from nexus.policy.aaa import authenticate, authorize, decide


class TestGuardAwarePolicy(unittest.TestCase):
    def test_normalize_policy_includes_guards(self):
        policy = normalize_policy({
            "name": "ingest_guarded",
            "allow": ["ingest_ability"],
            "role": "admin",
            "guards": ["source_verified", "schema_valid"],
        })
        self.assertEqual(policy.name, "ingest_guarded")
        self.assertIn("source_verified", policy.guards)
        self.assertIn("schema_valid", policy.guards)

    def test_authenticate_requires_identity_and_secret(self):
        self.assertTrue(authenticate({"id": "u1", "secret": "s"}))
        self.assertFalse(authenticate({"id": "u1"}))

    def test_authorize_respects_role_and_allow_list(self):
        principal = {"id": "u1", "secret": "s", "role": "admin"}
        policy = {"allow": ["ingest_ability"], "role": "admin"}
        self.assertTrue(authorize(principal, "ingest_ability", {}, policy))
        self.assertFalse(authorize(principal, "delete_ability", {}, policy))
        self.assertFalse(authorize({"id": "u2", "secret": "s", "role": "viewer"}, "ingest_ability", {}, policy))

    def test_decide_fails_without_authentication_or_authorization(self):
        denied = decide({"id": "u1"}, "ingest_ability", {}, {"allow": ["ingest_ability"], "role": "admin"})
        self.assertFalse(denied.authenticated)
        self.assertFalse(denied.authorized)
        allowed = decide({"id": "u1", "secret": "s", "role": "admin"}, "ingest_ability", {}, {"allow": ["ingest_ability"], "role": "admin"})
        self.assertTrue(allowed.authenticated)
        self.assertTrue(allowed.authorized)


if __name__ == "__main__":
    unittest.main()
