import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil

from badwordschecker.cli import main


class TestConfigIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # minimal dict file referenced by config
        (Path(self.temp_dir) / "badwords-it.txt").write_text("par\nparola", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("badwordschecker.cli.setup_logging")
    @patch("badwordschecker.cli.Model")
    @patch("badwordschecker.cli.Path.exists", return_value=True)
    def test_match_mode_from_config(self, mock_exists, mock_model, mock_setup_logging):
        (Path(self.temp_dir) / "badwordschecker.ini").write_text(
            """[dictionary]\npath = badwords-it.txt\nurl = http://example.com/dict.txt\n[options]\nmatch_mode = substring\nrecursive = true\nverbose = true\n""",
            encoding="utf-8",
        )
        (Path(self.temp_dir) / "sample.mp3").write_bytes(b"ID3")
        with patch("badwordschecker.utils.config.Path.cwd", return_value=Path(self.temp_dir)), \
             patch("sys.argv", ["badwordschecker", str(self.temp_dir)]), \
             patch("badwordschecker.cli.load_bad_words", return_value={"par"}), \
             patch("badwordschecker.cli.process_mp3_file", return_value="parola testo"), \
             patch("badwordschecker.cli.generate_per_file_report"), \
             patch("badwordschecker.cli.generate_aggregated_report") as mock_agg, \
             patch("badwordschecker.cli.scan_text", return_value={"par": 1}) as mock_scan:
            main()  # Should complete without SystemExit
            mock_agg.assert_called_once()
            # ensure substring match applied
            called_mode = mock_scan.call_args[0][2]
            self.assertEqual(called_mode, "substring")
            mock_setup_logging.assert_called_with(True)

    @patch("badwordschecker.cli.Model")
    @patch("badwordschecker.cli.Path.exists", return_value=True)
    def test_cli_overrides_config(self, mock_exists, mock_model):
        (Path(self.temp_dir) / "badwordschecker.ini").write_text(
            """[dictionary]\npath = badwords-it.txt\n[options]\nmatch_mode = substring\nrecursive = false\nverbose = false\n""",
            encoding="utf-8",
        )
        (Path(self.temp_dir) / "sample.mp3").write_bytes(b"ID3")
        with patch("badwordschecker.utils.config.Path.cwd", return_value=Path(self.temp_dir)), \
             patch("sys.argv", ["badwordschecker", "--match-mode", "exact", str(self.temp_dir)]), \
             patch("badwordschecker.cli.load_bad_words", return_value={"par"}), \
             patch("badwordschecker.cli.process_mp3_file", return_value="par par"), \
             patch("badwordschecker.cli.generate_per_file_report"), \
             patch("badwordschecker.cli.generate_aggregated_report") as mock_agg, \
             patch("badwordschecker.cli.scan_text", return_value={"par": 2}) as mock_scan:
            main()
            mock_agg.assert_called_once()
            called_mode = mock_scan.call_args[0][2]
            self.assertEqual(called_mode, "exact")

    @patch("badwordschecker.cli.download_dictionary")
    def test_download_uses_config_url(self, mock_download):
        (Path(self.temp_dir) / "badwordschecker.ini").write_text(
            """[dictionary]\nurl = http://config-url.example/dict.txt\npath = custom.txt\n""",
            encoding="utf-8",
        )
        (Path(self.temp_dir) / "custom.txt").write_text("x", encoding="utf-8")
        with patch("badwordschecker.utils.config.Path.cwd", return_value=Path(self.temp_dir)), \
             patch("sys.argv", ["badwordschecker", "--download-dict", str(self.temp_dir)]), \
             patch("badwordschecker.cli.Path.is_dir", return_value=True):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
        mock_download.assert_called_once()

    @patch("badwordschecker.cli.Model")
    @patch("badwordschecker.cli.Path.exists", return_value=True)
    def test_quarantine_moves_file(self, mock_exists, mock_model):
        (Path(self.temp_dir) / "badwordschecker.ini").write_text(
            """[dictionary]\npath = badwords-it.txt\n[options]\nmatch_mode = exact\nverbose = false\n""",
            encoding="utf-8",
        )
        mp3 = Path(self.temp_dir) / "sample.mp3"
        mp3.write_bytes(b"ID3")
        quarantine_dir = Path(self.temp_dir) / "q_zone"
        with patch("badwordschecker.utils.config.Path.cwd", return_value=Path(self.temp_dir)), \
             patch("sys.argv", ["badwordschecker", "--quarantine", str(quarantine_dir), str(self.temp_dir)]), \
                 patch("badwordschecker.cli.load_bad_words", return_value={"par"}), \
                 patch("badwordschecker.cli.process_mp3_file", return_value="par par"), \
                 patch("badwordschecker.cli.generate_per_file_report"), \
                 patch("badwordschecker.cli.generate_aggregated_report"):
                main()
        # File should have been moved
        assert not mp3.exists()
        assert (quarantine_dir / "sample.mp3").exists()

    @patch("badwordschecker.cli.download_dictionary")
    @patch("badwordschecker.cli.setup_logging")
    def test_dict_url_cli_override(self, mock_setup_logging, mock_download):
        # No config file to ensure CLI param used
        with patch("badwordschecker.utils.config.Path.cwd", return_value=Path(self.temp_dir)), \
             patch("sys.argv", ["badwordschecker", "--download-dict", "--dict-url", "http://override.example/d.txt", str(self.temp_dir)]), \
             patch("badwordschecker.cli.Path.is_dir", return_value=True):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
        mock_download.assert_called_once()


if __name__ == "__main__":
    unittest.main()
