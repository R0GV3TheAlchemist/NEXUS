import unittest

from nexus.cli import main


class TestCLISmoke(unittest.TestCase):
    def test_help_renders(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_run_subcommand_requires_inputs(self):
        with self.assertRaises(SystemExit):
            main(["run"])


if __name__ == "__main__":
    unittest.main()
