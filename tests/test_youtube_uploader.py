import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from youtube_bot import youtube_uploader

class TestYouTubeUploader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"youtube_api": {"TOKEN_FILE": "token.pkl", "CLIENT_SECRETS_FILE": "credentials.json"}}')
    @patch('os.path.exists', return_value=True)
    @patch('pickle.load')
    @patch('googleapiclient.discovery.build')
    def test_authenticate_youtube(self, mock_build, mock_pickle_load, mock_exists, mock_open):
        youtube = youtube_uploader.authenticate_youtube()
        self.assertTrue(mock_build.called)
        self.assertTrue(mock_pickle_load.called)

    @patch('builtins.open', new_callable=mock_open, read_data='{"youtube_api": {"TOKEN_FILE": "token.pkl", "CLIENT_SECRETS_FILE": "credentials.json"}}')
    @patch('os.path.exists', return_value=True)
    @patch('pickle.load')
    @patch('googleapiclient.discovery.build')
    @patch('googleapiclient.http.MediaFileUpload')
    def test_upload_video(self, mock_media_upload, mock_build, mock_pickle_load, mock_exists, mock_open):
        youtube = MagicMock()
        youtube_uploader.upload_video(youtube)
        self.assertTrue(youtube.videos().insert().execute.called)

if __name__ == '__main__':
    unittest.main()
