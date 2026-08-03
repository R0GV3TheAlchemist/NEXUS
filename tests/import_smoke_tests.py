import unittest


class TestImportSmoke(unittest.TestCase):
    def test_cli_imports_without_app_stack(self):
        import nexus.cli as cli
        self.assertTrue(hasattr(cli, "build_parser"))

    def test_package_imports(self):
        import nexus
        import nexus.core
        import nexus.core.policy
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
