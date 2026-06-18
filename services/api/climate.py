
import requests
from  .locator import get_coords

def get_climate(lat, long):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": long,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "relative_humidity_2m_max",
            "relative_humidity_2m_min",
            "relative_humidity_2m_mean",
            "precipitation_sum",
            "sunshine_duration",
            "wind_speed_10m_max"
        ],
        "past_days": 7,
        "timezone": "auto"
    }

    data = requests.get(url, params=params).json()

    return data["daily"]

location = "Coorg, Karnataka"

lat, long = get_coords(location)

daily = get_climate(lat, long)

for i in range(len(daily["time"])):
    print("Date:", daily["time"][i])
    print("Max Temp:", daily["temperature_2m_max"][i])
    print("Min Temp:", daily["temperature_2m_min"][i])
    print("Mean Temp:", daily["temperature_2m_mean"][i])
    print("Max Humidity:", daily["relative_humidity_2m_max"][i])
    print("Min Humidity:", daily["relative_humidity_2m_min"][i])
    print("Mean Humidity:", daily["relative_humidity_2m_mean"][i])
    print("Precipitation:", daily["precipitation_sum"][i])
    print("Sunshine Duration:", daily["sunshine_duration"][i])
    print("Max Wind Speed:", daily["wind_speed_10m_max"][i])
    print("-" * 40)