import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from badwordschecker.dictionary import load_bad_words, download_dictionary


class TestDictionary(unittest.TestCase):
    def test_load_bad_words(self):
        m = mock_open(read_data="word1\n#comment\nword2\n\nword3")
        with patch("builtins.open", m):
            with patch("pathlib.Path.exists", return_value=True):
                words = load_bad_words(Path("dummy_path"))
                self.assertEqual(words, {"word1", "word2", "word3"})

    def test_load_bad_words_empty(self):
        m = mock_open(read_data="")
        with patch("builtins.open", m):
            with patch("pathlib.Path.exists", return_value=True):
                words = load_bad_words(Path("dummy_path"))
                self.assertEqual(words, set())

    def test_load_bad_words_not_found(self):
        with patch("pathlib.Path.exists", return_value=False):
            words = load_bad_words(Path("non_existent_path"))
            self.assertEqual(words, set())

    @patch("requests.get")
    @patch("pathlib.Path.write_text")
    def test_download_dictionary(self, mock_write_text, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "word1\nword2"
        with patch("pathlib.Path.exists", return_value=False):
            download_dictionary("http://example.com/dict.txt", Path("dummy_path.txt"))
            mock_write_text.assert_called_once_with("word1\nword2", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
