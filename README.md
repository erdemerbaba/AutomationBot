## About Project
Automation Bot Project shortly manage X, Instagram and Youtube accounts and post a video automatically. In the near future this project will be get trend topics, generate videos and publish to social medias automatically every spesific time.

## Bots Overview

### YouTube Bot

The YouTube bot is responsible for uploading videos to YouTube. It uses the YouTube Data API v3 for authentication and video upload.

- **File:** [src/youtube_bot/youtube_uploader.py](src/youtube_bot/youtube_uploader.py)
- **Authentication:** OAuth 2.0
- **Dependencies:** `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `pickle`

### Instagram Bot

The Instagram bot uploads videos to Instagram Reels using the `instagrapi` library.

- **File:** [src/instagram_bot/instagram_uploader.py](src/instagram_bot/instagram_uploader.py)
- **Authentication:** Username and password with challenge handling
- **Dependencies:** `instagrapi`

### Twitter (X) Bot

The Twitter bot fetches top news headlines and tweets them using the Twitter API v2.

- **File:** [src/x_bot/x_uploader.py](src/x_bot/x_uploader.py)
- **Authentication:** Bearer token, API key, API secret key, Access token, Access token secret
- **Dependencies:** `tweepy`, `requests`

## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure the necessary credentials for each bot:
    - YouTube: Update [credentials.json](http://_vscodecontentref_/8) and `token.pkl` in [youtube_bot](http://_vscodecontentref_/9)
    - Instagram: Update the [username](http://_vscodecontentref_/10) and [password](http://_vscodecontentref_/11) in [instagram_uploader.py](http://_vscodecontentref_/12)
    - Twitter: Update the API credentials in [x_uploader.py](http://_vscodecontentref_/13)
    -Content Generation: Update the API secrets in config.json

## Usage

To upload a video to socialmedia example:
```sh
python src/main.py # Social Media Automation Bots

This project contains a collection of automation bots for uploading content to various social media platforms including YouTube, Instagram, and Twitter (X).
