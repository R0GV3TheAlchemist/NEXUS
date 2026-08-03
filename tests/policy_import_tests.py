import unittest


class TestPolicyImports(unittest.TestCase):
    def test_core_policy_import(self):
        from nexus.core.policy import decide, account
        self.assertTrue(callable(decide))
        self.assertTrue(callable(account))


if __name__ == "__main__":
    unittest.main()
