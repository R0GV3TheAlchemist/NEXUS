import unittest


class TestCorePolicyAaa(unittest.TestCase):
    def test_core_policy_aaa_imports(self):
        from nexus.core.policy.aaa import decide, account, should_accept_ability
        self.assertTrue(callable(decide))
        self.assertTrue(callable(account))
        self.assertTrue(callable(should_accept_ability))


if __name__ == "__main__":
    unittest.main()
