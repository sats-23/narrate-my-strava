import requests
import os
import webbrowser
import time
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import urllib.parse

ENV_FILE = "var.env"
load_dotenv(ENV_FILE)

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5001"

auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if "code" in query_params:
            auth_code = query_params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Authorization successful! You can close this tab.</h1>")
            print(f"Captured Authorization Code: {auth_code}")

    def log_message(self, format, *args):
        return  

def start_server():
    server = HTTPServer(("localhost", 5001), OAuthHandler)
    print("Waiting for authorization response on port 5001...")
    server.handle_request()

def request_authorization():
    url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={CLIENT_ID}&response_type=code"
        f"&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read,activity:read_all"
    )
    print(f"Opening browser for authorization: {url}")
    webbrowser.open(url)
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

def exchange_token(auth_code):
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        tokens = response.json()
        save_tokens(tokens)
        print("Access token obtained and saved!")
        return tokens["access_token"]
    else:
        print("Error exchanging token:", response.json())
        return None

def save_tokens(tokens):
    env_vars = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                key, _, value = line.strip().partition("=")
                env_vars[key] = value
    
    env_vars["STRAVA_ACCESS_TOKEN"] = tokens['access_token']
    env_vars["STRAVA_REFRESH_TOKEN"] = tokens['refresh_token']
    env_vars["STRAVA_EXPIRES_AT"] = str(tokens['expires_at'])
    
    with open(ENV_FILE, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print("Tokens saved to var.env")

if __name__ == "__main__":
    request_authorization()
    while auth_code is None:
        time.sleep(1)
    access_token = exchange_token(auth_code)
    if access_token:
        print(f"Your new access token: {access_token}")
    else:
        print("Failed to retrieve access token.")
