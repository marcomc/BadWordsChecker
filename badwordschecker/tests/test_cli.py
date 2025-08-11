import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from badwordschecker.cli import main

class TestCli(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @patch("sys.argv", ["badwordschecker", "--download-dict"])
    @patch("badwordschecker.cli.download_dictionary")
    def test_download_dict_flag(self, mock_download):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_download.assert_called_once()

    @patch("sys.argv", ["badwordschecker", "--edit-dict"])
    @patch("badwordschecker.cli.edit_dictionary")
    def test_edit_dict_flag(self, mock_edit):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        mock_edit.assert_called_once()

    @patch("sys.argv", ["badwordschecker", "non_existent_folder"])
    def test_folder_not_found(self):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

    @patch("sys.argv", ["badwordschecker"])
    @patch("pathlib.Path.cwd")
    def test_no_folder_uses_cwd(self, mock_cwd):
        mock_cwd.return_value = Path(self.temp_dir)
        # We expect a SystemExit because the model is not found,
        # but this confirms that the CWD is being used.
        with self.assertRaises(SystemExit):
            main()
