import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from badwordschecker.model_manager import get_model_path, handle_model_download, DEFAULT_MODEL_PATH

class TestModelManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_get_model_path(self):
        config_path = Path("/custom/path")
        self.assertEqual(get_model_path(config_path), config_path)
        self.assertEqual(get_model_path(None), DEFAULT_MODEL_PATH)

    @patch("badwordschecker.model_manager._download_model")
    @patch("badwordschecker.model_manager._unzip_model")
    @patch("pathlib.Path.exists", return_value=False)
    def test_handle_model_download_calls_downloader(self, mock_exists, mock_unzip, mock_download):
        model_path = Path(self.temp_dir) / "model"
        handle_model_download(model_path)
        mock_download.assert_called_once()
        mock_unzip.assert_called_once()

    @patch("pathlib.Path.exists", return_value=True)
    def test_handle_model_download_skips_if_exists(self, mock_exists):
        model_path = Path(self.temp_dir) / "model"
        with patch("badwordschecker.model_manager._download_model") as mock_download:
            handle_model_download(model_path)
            mock_download.assert_not_called()