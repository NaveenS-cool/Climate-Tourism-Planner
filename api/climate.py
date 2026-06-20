
import requests
from  .locator import get_coords
from datetime import date

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
today=date.today().isoformat()

lat, long = get_coords(location)

daily = get_climate(lat, long)
current={}

for i in range(len(daily["time"])):
    if daily["time"][i]==today:
        current={0:today,1:daily["temperature_2m_mean"][i],2: daily["relative_humidity_2m_mean"][i],3:daily["precipitation_sum"][i]} 
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

for i in range(4):
    print(current[i])