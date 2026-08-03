import unittest

from nexus.app.runner import run_ability


class TestCLIBehavior(unittest.TestCase):
    def test_single_command_path_accepts_json_inputs(self):
        principal = {"id": "u1", "secret": "s", "role": "admin"}
        ability = {
            "name": "Absorption",
            "family": "Information Cognition",
            "subject_domains": ["physics"],
            "effects": {"intake": 1.0},
        }
        policy = {"allow": ["ingest_ability"], "role": "admin", "guards": ["schema_valid"]}
        result = run_ability(principal, ability, policy)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["decision"].reason, "allowed")


if __name__ == "__main__":
    unittest.main()
