**Narrate My Strava**

This AI solution can help write crisp descriptions for your strava activities. 
It accounts for all factors like sport type, weather, device/gear used, distance, speed, time, watts, calories, elevation and splits as well.
Just pass it your Strava activity ID and watch it throw down artistic descriptions of the fun times you've had.


**How?**

1. Create venv
2. pip install -r requirements.txt
3. Install Ollama and model of choice
4. Create Strava App and get your API credentials
5. Insert credentials (STRAVA_ACCESS_TOKEN, STRAVA_REFRESH_TOKEN, STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET) into var.env under StravaAgent dir
6. python ai.py


**Working?**

1. Prompts you to authenticate and authorise the Strava App (redirects to localhost after)
2. App auth code, refresh and access token are all dynamically updated into var.env for you (make sure to gitignore)
3. Enter activity ID and watch agents unroll.

**Asides**

1. Weather API can retrieve data from past 1 week only
2. Enhance it further for auto trigger via activity push & auto-overwrite activity description with results
3. Make prompt params tuneable for description length, tone, analysis, and so on.
4. Strava activity data is potent, use it wisely to crunch right conclusions

Demo:
![Screenshot 2025-03-31 at 2 58 32 PM](https://github.com/user-attachments/assets/434f6b7a-144e-41e7-b182-b992eebc779c)
