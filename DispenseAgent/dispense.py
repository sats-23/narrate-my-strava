import json
import ast


with open("sample.json", "r") as file:
    raw_data = file.read()

data = ast.literal_eval(raw_data)

json_data = json.loads(json.dumps(data))

activity_data = {
    "activity_type": data.get("type", "Unknown"),
    "distance_km": data.get("distance", 0) / 1000,  
    "average_speed_mps": data.get("average_speed", 0),  
    "average_speed_kmh": data.get("average_speed", 0) * 3.6,  
    "sport_type": data.get("sport_type", "Unknown"),
    "athlete_count": data.get("athlete_count", 1),
    "calories": data.get("calories", 0),
    "commute": data.get("commute", False),

}

if data.get("device_watts", False):
    activity_data["average_watts"] = data.get("average_watts", 0)

print(activity_data)