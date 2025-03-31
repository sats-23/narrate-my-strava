import requests
from dotenv import load_dotenv
import os
import pprint
import json 

ENV_FILE = "var.env"
load_dotenv(ENV_FILE)

ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

def get_activity(activity_id):
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open("response.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4) 
            
        return data 
    else:
        return f"Error: {response.status_code}, {response.json()}"


