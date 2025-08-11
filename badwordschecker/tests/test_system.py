import unittest
from unittest.mock import patch
from badwordschecker.utils.system import command_exists

class TestSystem(unittest.TestCase):

    @patch('shutil.which', return_value='/usr/bin/ffmpeg')
    def test_command_exists(self, mock_which):
        self.assertTrue(command_exists('ffmpeg'))

    @patch('shutil.which', return_value=None)
    def test_command_does_not_exist(self, mock_which):
        self.assertFalse(command_exists('nonexistentcommand'))

if __name__ == '__main__':
    unittest.main()
