import unittest

from nexus.core.ingestion import validate_payload, build_ability, ingest_ability_payload
from nexus.core.policy import should_accept_ability
from nexus.core.ability_schema import AbilitySchema, AbilityStability, AbilityGrowthTag


class TestIngestionAndPolicy(unittest.TestCase):
    def test_validate_payload_requires_fields(self):
        issues = validate_payload({"name": "Teleportation"})
        self.assertIn("missing_family", issues)
        self.assertIn("missing_subject_domains", issues)
        self.assertIn("missing_effects", issues)

    def test_build_ability_normalizes_family(self):
        ability = build_ability({
            "name": "Teleportation",
            "family": "Information Cognition",
            "subject_domains": ["physics", "psychology"],
            "effects": {"light": 1.0},
        })
        self.assertEqual(ability.family, "information_cognition")
        self.assertEqual(ability.name, "Teleportation")

    def test_ingest_accepts_complete_payload(self):
        result = ingest_ability_payload({
            "name": "Enhanced Perception",
            "family": "Information Cognition",
            "subject_domains": ["psychology"],
            "effects": {"light": 1.0, "balance": 0.25},
            "stability": "stable",
            "growth_tag": "growth_oriented",
        })
        self.assertTrue(result["accepted"])
        self.assertEqual(result["issues"], [])
        self.assertIsNotNone(result["ability"])

    def test_policy_rejects_rule_writing_destruction(self):
        ability = AbilitySchema(
            name="Reality Erasure",
            family="magic",
            subject_domains=["philosophy"],
            effects={"chaos": 10.0},
            stability=AbilityStability.RULE_WRITING,
            growth_tag=AbilityGrowthTag.DESTRUCTIVE_ORIENTED,
        )
        self.assertFalse(should_accept_ability(ability))


if __name__ == "__main__":
    unittest.main()
