import requests
import json
import os
import time
from dotenv import load_dotenv

ENV_FILE = "var.env"

# Load environment variables
load_dotenv(ENV_FILE)

# Strava API credentials from environment variables
CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
EXPIRES_AT = int(os.getenv("STRAVA_EXPIRES_AT", 0))


def refresh_strava_token():
    global REFRESH_TOKEN
    
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        new_tokens = response.json()
        save_tokens(new_tokens)
        print("Access token updated successfully!")
        return new_tokens["access_token"]
    else:
        print("Error refreshing token:", response.json())
        return None


def save_tokens(tokens):
    global REFRESH_TOKEN
    
    REFRESH_TOKEN = tokens["refresh_token"]
    data = {
        "STRAVA_ACCESS_TOKEN": tokens["access_token"],
        "STRAVA_REFRESH_TOKEN": tokens["refresh_token"],
        "STRAVA_EXPIRES_AT": str(tokens["expires_at"]),
    }
    
    with open(ENV_FILE, "r") as f:
        lines = f.readlines()
    
    with open(ENV_FILE, "w") as f:
        for line in lines:
            if not line.startswith("STRAVA_ACCESS_TOKEN") and not line.startswith("STRAVA_REFRESH_TOKEN") and not line.startswith("STRAVA_EXPIRES_AT"):
                f.write(line)
        for key, value in data.items():
            f.write(f"{key}={value}\n")
    
    print("Tokens saved successfully!")


def get_access_token():
    global EXPIRES_AT
    if EXPIRES_AT > time.time():
        return ACCESS_TOKEN
    else:
        return refresh_strava_token()


if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        print("Your latest access token is:", access_token)
    else:
        print("Failed to retrieve access token.")
