import unittest


class TestEntrypoint(unittest.TestCase):
    def test_entrypoint_module_exists(self):
        import nexus.__main__  # noqa: F401
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
