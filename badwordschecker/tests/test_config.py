import unittest
from pathlib import Path
from unittest.mock import patch
import tempfile
import shutil
from configparser import ConfigParser

from badwordschecker.utils import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "badwordschecker.ini"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_get_config_option(self):
        config_parser = ConfigParser()
        config_parser.add_section("test_section")
        config_parser.set("test_section", "test_key", "test_value")
        with open(self.config_path, "w") as f:
            config_parser.write(f)

        with patch("badwordschecker.utils.config._get_config") as mock_get_config:
            mock_get_config.return_value = config_parser
            value = config.get_config_option("test_section", "test_key")
            self.assertEqual(value, "test_value")

    def test_get_config_dict_url(self):
        # Test with CLI override
        self.assertEqual(config.get_config_dict_url("http://cli.url"), "http://cli.url")

        # Test with config file
        with patch("badwordschecker.utils.config.get_config_option", return_value="http://config.url"):
            self.assertEqual(config.get_config_dict_url(), "http://config.url")

        # Test with fallback
        with patch("badwordschecker.utils.config.get_config_option", return_value=None):
            self.assertEqual(config.get_config_dict_url(), config.DEFAULT_DICT_URL)

if __name__ == '__main__':
    unittest.main()
