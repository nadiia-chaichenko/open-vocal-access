"""Basic catalogue and CLI checks; run with unittest discover."""
import unittest
from vocal_access import load_catalogue, search_repertoire, main
from contextlib import redirect_stdout
from io import StringIO


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = load_catalogue()

    def test_catalogue_not_empty(self):
        self.assertGreater(len(self.catalogue), 0)

    def test_filter_by_language_and_voice(self):
        matches = search_repertoire(self.catalogue, language="French", voice="mezzo")
        self.assertGreater(len(matches), 0)
        self.assertTrue(all(row["language"] == "French" for row in matches))

    def test_keyword_is_case_insensitive(self):
        matches = search_repertoire(self.catalogue, keyword="CARMEN")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["opera"], "Carmen")

    def test_empty_results(self):
        matches = search_repertoire(self.catalogue, keyword="nonexistent-opera-999")
        self.assertEqual(matches, [])

    def test_json_mode(self):
        output = StringIO()
        with redirect_stdout(output):
            code = main(["--keyword", "Carmen", "--json"])
        self.assertEqual(code, 0)
        self.assertIn('"opera": "Carmen"', output.getvalue())


if __name__ == "__main__":
    unittest.main()
