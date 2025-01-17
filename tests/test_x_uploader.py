import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from x_bot import x_uploader

class TestXUploader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"x_api": {"API_KEY": "key", "API_SECRET_KEY": "secret", "ACCESS_TOKEN": "token", "ACCESS_TOKEN_SECRET": "token_secret", "BEARER_TOKEN": "bearer"}}')
    @patch('tweepy.Client.create_tweet')
    @patch('requests.get')
    def test_x_uploader(self, mock_get, mock_create_tweet, mock_open):
        mock_get.return_value.json.return_value = {
            'articles': [
                {'description': 'Test description', 'source': {'name': 'Test source'}, 'publishedAt': '2025-01-16T00:00:00Z'}
            ]
        }
        x_uploader.main()
        self.assertTrue(mock_create_tweet.called)

if __name__ == '__main__':
    unittest.main()
