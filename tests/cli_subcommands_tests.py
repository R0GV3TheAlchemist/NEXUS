import unittest

from nexus.cli import build_parser, main


class TestCLISubcommands(unittest.TestCase):
    def test_parser_exposes_subcommands(self):
        parser = build_parser()
        self.assertIsNotNone(parser)

    def test_validate_subcommand_parses(self):
        code = main(["validate", "--principal", '{"id": "u1"}', "--ability", '{"name": "Absorption"}'])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
