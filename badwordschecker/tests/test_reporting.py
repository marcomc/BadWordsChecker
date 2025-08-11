import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import mock_open, patch

from badwordschecker.reporting import (
    generate_per_file_report,
    generate_aggregated_report,
)


class TestReporting(unittest.TestCase):
    def test_generate_per_file_report(self):
        matches = Counter({"badword1": 2, "badword2": 1})
        output_dir = Path("test_output")
        mp3_path = Path("test.mp3")

        m = mock_open()
        with patch("builtins.open", m):
            with patch("pathlib.Path.mkdir") as mock_mkdir:
                generate_per_file_report(mp3_path, matches, output_dir)
                mock_mkdir.assert_called_once_with(exist_ok=True)
                m.assert_called_once_with(
                    output_dir / f"{mp3_path.name}.txt", "w", encoding="utf-8"
                )
                handle = m()
                handle.write.assert_any_call("File: test.mp3\n")
                handle.write.assert_any_call("Total bad words: 3\n")

    def test_generate_aggregated_report(self):
        all_matches = {
            "test1.mp3": Counter({"cazzo": 2, "merda": 1}),
            "test2.mp3": Counter({"cazzo": 2}),
        }
        output_dir = Path("test_output")

        m = mock_open()
        with patch("builtins.open", m):
            with patch("pathlib.Path.mkdir") as mock_mkdir:
                generate_aggregated_report(all_matches, output_dir, 2)
                mock_mkdir.assert_called_once_with(exist_ok=True)
                m.assert_called_once_with(
                    output_dir / "parolacce.txt", "w", encoding="utf-8"
                )
                handle = m()
                handle.write.assert_any_call("Bad Words Summary\n")
                handle.write.assert_any_call("Total files scanned: 2\n")


if __name__ == "__main__":
    unittest.main()
