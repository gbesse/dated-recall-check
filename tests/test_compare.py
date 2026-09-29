import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compare import TEXT, compare, result_ids, score


class RecallTests(unittest.TestCase):
    def test_response_ids(self):
        self.assertEqual(result_ids({"results": [{"id": "a"}, {"memory_id": "b"}]}), ["a", "b"])

    def test_regression_and_lost_id(self):
        cases = [{"id": "x", "query": "when", "expected_ids": ["a"]}]
        rows = compare(cases, {"x": ["a"]}, {"x": ["b"]}, 1)
        self.assertEqual(rows[0]["lost_ids"], ["a"])
        self.assertEqual((rows[0]["before"], rows[0]["after"]), (1, 0))

    def test_languages(self):
        self.assertEqual(set(TEXT), {"en", "fr", "es"})
        self.assertTrue(all(TEXT[l]["lost"] for l in TEXT))


if __name__ == "__main__":
    unittest.main()
