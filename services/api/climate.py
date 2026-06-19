
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

    data = requests.get(url, params=params, headers={"User-Agent": "ClimateTourismPlanner"}).json()

    return data["daily"]

