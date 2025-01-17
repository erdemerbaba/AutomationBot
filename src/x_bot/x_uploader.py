import json
import os
import requests
from datetime import datetime, timedelta
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
    BEARER_TOKEN = config['x_api']['BEARER_TOKEN']

    # Authenticate to Twitter using the v2 API
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN,
                               consumer_key=API_KEY,
                               consumer_secret=API_SECRET_KEY,
                               access_token=ACCESS_TOKEN,
                               access_token_secret=ACCESS_TOKEN_SECRET)
    except Exception as e:
        logging.error(f"Error authenticating to Twitter: {e}")
        return

    # News API parameters from config
    secret = config['contentgenerator_api']['TOPIC_SECRET']
    url = config['contentgenerator_api']['TOPIC_INFO']

    parameters = {
        'pageSize': 100,
        'sources': 'bbc-news',
        'apiKey': secret
    }

    # Make the request
    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        response_json = response.json()
    except requests.RequestException as e:
        logging.error(f"Error making request to News API: {e}")
        return

    # Get yesterday's date
    yesterday = (datetime.utcnow() - timedelta(days=1)).date()

    # Prepare output list
    output_list = []

    # Process articles
    for article in response_json.get('articles', []):
        description = article.get('description')
        source = article.get('source', {}).get('name')
        published_at = article.get('publishedAt')

        # Check if description, source, or publishedAt is empty or "none"
        if not description or not source or not published_at:
            continue

        # Check if publishedAt is yesterday
        published_date = datetime.fromisoformat(published_at.replace('Z', '')).date()
        if published_date != yesterday:
            continue

        if len(description) > 80:
            description = description[:130]
            if '.' in description:
                description = description[:description.rfind('.') + 1]

        # Create a formatted string
        formatted_string = f"{description[:130]}"
        
        # Check the length of the output string
        if len(formatted_string) <= 260:
            output_list.append(formatted_string)

    # Prepare the output string
    output_list2 = '\n\n'.join(sentence.strip("'") for sentence in output_list)
    output = "Daily Top News\n\n" + output_list2
    truncated_output = output[:280]
    logging.info(truncated_output)

    # Post the tweet
    try:
        client.create_tweet(text=truncated_output)
        logging.info(f"Tweeted: {truncated_output}")
    except Exception as e:
        logging.error(f"Error while tweeting: {e}")

if __name__ == "__main__":
    main()


