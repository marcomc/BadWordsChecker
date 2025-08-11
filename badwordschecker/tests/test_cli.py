import unittest
from unittest.mock import patch, MagicMock

from badwordschecker.cli import main


class TestCli(unittest.TestCase):
    @patch("sys.argv", ["badwordschecker", "--download-dict"])
    @patch("badwordschecker.cli.download_dictionary")
    def test_download_dict(self, mock_download):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_download.assert_called_once()

    @patch("sys.argv", ["badwordschecker", "--edit-dict"])
    @patch("badwordschecker.cli.edit_dictionary")
    def test_edit_dict(self, mock_edit):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_edit.assert_called_once()

    @patch("sys.argv", ["badwordschecker", "non_existent_folder"])
    @patch("pathlib.Path.is_dir", return_value=False)
    def test_mp3_folder_not_found(self, mock_is_dir):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
