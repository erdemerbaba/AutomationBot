import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from instagram_bot import instagram_uploader

class TestInstagramUploader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"instagram_api": {"USERNAME_INFO": "username", "PASSWORD_INFO": "password"}}')
    @patch('instagrapi.Client.login')
    @patch('instagrapi.Client.clip_upload')
    def test_instagram_uploader(self, mock_clip_upload, mock_login, mock_open):
        instagram_uploader.main()
        self.assertTrue(mock_login.called)
        self.assertTrue(mock_clip_upload.called)

if __name__ == '__main__':
    unittest.main()
