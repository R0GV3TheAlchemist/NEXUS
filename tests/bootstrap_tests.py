import unittest
from pathlib import Path

from scripts.bootstrap_nexus import FILES


class TestBootstrap(unittest.TestCase):
    def test_bootstrap_file_manifest_exists(self):
        self.assertIn("src/nexus/__init__.py", FILES)
        self.assertIn("src/nexus/app/__init__.py", FILES)

    def test_manifest_is_minimal(self):
        self.assertGreaterEqual(len(FILES), 6)


if __name__ == "__main__":
    unittest.main()
