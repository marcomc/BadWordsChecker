import unittest
from collections import Counter

from badwordschecker.scanning import scan_text


class TestScanning(unittest.TestCase):
    def test_scan_text_exact_match(self):
        text = "This is a test with badword1 and badword2."
        bad_words = {"badword1", "badword2"}
        matches = scan_text(text, bad_words, match_mode="exact")
        self.assertEqual(matches, Counter({"badword1": 1, "badword2": 1}))

    def test_scan_text_substring_match(self):
        text = "This is a test with badword1 and anotherbadword."
        bad_words = {"badword"}
        matches = scan_text(text, bad_words, match_mode="substring")
        self.assertEqual(matches, Counter({"badword": 2}))

    def test_scan_text_no_match(self):
        text = "This is a clean text."
        bad_words = {"badword1", "badword2"}
        matches = scan_text(text, bad_words)
        self.assertEqual(matches, Counter())


if __name__ == "__main__":
    unittest.main()
