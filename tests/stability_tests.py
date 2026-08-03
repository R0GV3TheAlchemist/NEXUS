import unittest

from nexus.cli import handle_bootstrap


class TestStability(unittest.TestCase):
    def test_bootstrap_reports_existing_paths(self):
        result = handle_bootstrap(".")
        self.assertIn("checked", result)
        self.assertIn("src/nexus/core/policy/aaa.py", result["checked"])


if __name__ == "__main__":
    unittest.main()
