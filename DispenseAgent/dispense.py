import json
import pprint

def dispense():
    with open("response.json", "r") as file:
        data = json.load(file)

    activity_data = {
        "activity_type": data.get("type", "Unknown"),
        "distance_km": data.get("distance", 0) / 1000,  
        "average_speed_kmh": data.get("average_speed", 0) * 3.6,  
        "sport_type": data.get("sport_type", "Unknown"),
        "athlete_count": data.get("athlete_count", 1),
        "calories": data.get("calories", 0),
        "commute": data.get("commute", False),
        "total_elevation_gain": data.get("total_elevation_gain", 0),
        "start_date_local": data.get("start_date_local", "Unknown"),
        "achievement_count": data.get("achievement_count", 0),
        "start_latlng": data.get("start_latlng", [0, 0]),
        "device_name": data.get("device_name", "Unknown"),
    }
    activity_data["gear_info"] = {
        "gear_name": data.get("gear", {}).get("name", "Unknown"),
        "gear_nickname": data.get("gear", {}).get("nickname", "Unknown")
    }

    activity_data["splits"] = [
        {
            "distance": item.get("distance"),
            "elevation_difference": item.get("elevation_difference"),
            "moving_time": item.get("moving_time")
        }
        for item in data.get("splits_metric", [])
    ]

    if data.get("device_watts", False):
        activity_data["average_watts"] = data.get("average_watts", "Unknown")

    return activity_data