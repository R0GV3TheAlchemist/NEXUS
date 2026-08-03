import unittest


class TestPolicyAcceptance(unittest.TestCase):
    def test_should_accept_ability_exists(self):
        from nexus.core.policy import should_accept_ability
        self.assertTrue(callable(should_accept_ability))


if __name__ == "__main__":
    unittest.main()
