import json
import os
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import pickle

# Determine the correct path to the configuration file
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

# Load the configuration file
with open(config_path, 'r') as file:
    config = json.load(file)

# YouTube API parameters from config
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = config['youtube_api']['TOKEN_FILE']
CLIENT_SECRETS_FILE = config['youtube_api']['CLIENT_SECRETS_FILE']

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    credentials = None

    # Load credentials from file
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token_file:
            credentials = pickle.load(token_file)

    # If no valid credentials are available, request them
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save credentials for next time
        with open(TOKEN_FILE, 'wb') as token_file:
            pickle.dump(credentials, token_file)

    # Build YouTube API service
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)
    return youtube

def upload_video(youtube):
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": "Uploaded from Python",
            "description": "This is the most awesome description ever",
            "tags": ["test", "python", "api"]
        },
        "status": {
            "privacyStatus": "private"
        }
    }

    # Path to the video
    media_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'video.mp4')

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(media_file, chunksize=-1, resumable=True)
    )

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Video uploaded with ID: {response['id']}")

if __name__ == "__main__":
    youtube = authenticate_youtube()
    upload_video(youtube)
