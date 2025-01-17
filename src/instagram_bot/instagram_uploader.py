import json
import os
from instagrapi import Client
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

    # Instagram credentials from config
    USERNAME_INFO = config['instagram_api']['USERNAME_INFO']
    PASSWORD_INFO = config['instagram_api']['PASSWORD_INFO']

    # Initialize the client
    client = Client()

    # Challenge handler function
    def challenge_handler(USERNAME_INFO, choice):
        # Resolve the challenge and print the URL for manual resolution
        logging.info(f"Visit this URL to resolve the challenge: {client.challenge_resolve()}")
        return True

    # Set the custom challenge handler
    client.challenge_code_handler = challenge_handler

    try:
        # Clear any cached session and login
        client.settings = {}  # Reset session
        client.login(USERNAME_INFO, PASSWORD_INFO)

        logging.info("Login successful!")

        # Perform actions after successful login
        # Example: Upload a Reel
        video_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'video.mp4')
        caption = "Your Reel caption here"
        reel = client.clip_upload(video_path, caption=caption)
        logging.info(f"Reel uploaded successfully: {reel.pk}")

    except Exception as e:
        # Print the error message and the last JSON response
        logging.error("An error occurred during login or processing:")
        logging.error(e)
        logging.error(f"Last response from Instagram (if available): {client.last_json}")

if __name__ == "__main__":
    main()
