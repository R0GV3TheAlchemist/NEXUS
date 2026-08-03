import unittest

from scripts.bootstrap_nexus import FILES


class TestBootstrapSkeleton(unittest.TestCase):
    def test_expected_paths_present(self):
        for path in [
            "src/nexus/__init__.py",
            "src/nexus/__main__.py",
            "src/nexus/core/policy/aaa.py",
            "src/nexus/policy/aaa.py",
        ]:
            self.assertIn(path, FILES)


if __name__ == "__main__":
    unittest.main()
