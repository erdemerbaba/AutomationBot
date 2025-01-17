import json
import os
import tweepy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Determine the correct path to the configuration file
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

    # Load the configuration file
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from config file: {e}")
        return

    # Twitter API credentials from config
    API_KEY = config['x_api']['API_KEY']
    API_SECRET_KEY = config['x_api']['API_SECRET_KEY']
    ACCESS_TOKEN = config['x_api']['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = config['x_api']['ACCESS_TOKEN_SECRET']

    # Authenticate to Twitter using the v1.1 API for media upload
    try:
        auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    except Exception as e:
        logging.error(f"Error authenticating to Twitter: {e}")
        return

    # Path to the video
    video_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'video.mp4')

    # Upload the video to Twitter
    try:
        media = api.media_upload(video_path, media_category='tweet_video')
        logging.info(f"Video uploaded successfully: {media.media_id}")

        # Post the tweet with the video
        api.update_status(status="Check out this video!", media_ids=[media.media_id])
        logging.info("Tweeted video successfully")
    except Exception as e:
        logging.error(f"Error while uploading video or tweeting: {e}")

if __name__ == "__main__":
    main()
