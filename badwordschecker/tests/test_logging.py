import unittest
import logging
from unittest.mock import patch
from badwordschecker.utils.logging import setup_logging

class TestLogging(unittest.TestCase):

    @patch('logging.basicConfig')
    def test_setup_logging_text(self, mock_basic_config):
        setup_logging(verbose=False, log_format="text")
        self.assertEqual(logging.getLogger().level, logging.INFO)

    @patch('logging.basicConfig')
    def test_setup_logging_json(self, mock_basic_config):
        setup_logging(verbose=True, log_format="json")
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

if __name__ == '__main__':
    unittest.main()
