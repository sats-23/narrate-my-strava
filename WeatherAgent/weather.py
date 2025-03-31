import requests
from datetime import datetime, timedelta

def get_historical_weather(lat, lon, timestamp):
    # Convert timestamp to ISO 8601 format (YYYY-MM-DDTHH:MM)
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    date_str = dt.strftime("%Y-%m-%d")
    
    # Open-Meteo API URL for historical weather
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weathercode,precipitation,wind_speed_10m,cloudcover,visibility&past_days=7&timezone=UTC"
    
    response = requests.get(url)
    data = response.json()
    
    # Extract the relevant weather data
    hourly_data = data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    weather_codes = hourly_data.get("weathercode", [])
    precipitation = hourly_data.get("precipitation", [])
    wind_speeds = hourly_data.get("wind_speed_10m", [])
    cloud_cover = hourly_data.get("cloudcover", [])
    visibility = hourly_data.get("visibility", [])
    
    # Find the closest matching timestamp
    closest_time = None
    min_diff = timedelta.max
    closest_index = -1
    
    for i, t in enumerate(times):
        t_dt = datetime.strptime(t, "%Y-%m-%dT%H:%M")
        diff = abs(t_dt - dt)
        if diff < min_diff:
            min_diff = diff
            closest_time = t
            closest_index = i
    
    if closest_time is not None:
        return {
            "datetime": closest_time,
            "temperature": temperatures[closest_index],
            "weather_code": weather_codes[closest_index],
            "precipitation": precipitation[closest_index],
            "wind_speed": wind_speeds[closest_index],
            "cloud_cover": cloud_cover[closest_index],
            "visibility": visibility[closest_index]
        }
    
    return {"error": "Weather data not found for the given timestamp"}

#Test data
lat, lon = 12.972617, 77.636968
timestamp = "2025-03-24T07:39:32Z"

#API works only with dates upto 1 week
weather_info = get_historical_weather(lat, lon, timestamp)
print(weather_info)
