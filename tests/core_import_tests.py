import unittest


class TestCoreImports(unittest.TestCase):
    def test_core_exports_import_cleanly(self):
        import nexus.core as core
        self.assertTrue(hasattr(core, "RunResult"))
        self.assertFalse(hasattr(core, "AbilityRecord"))


if __name__ == "__main__":
    unittest.main()
