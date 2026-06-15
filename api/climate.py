import requests
from .locator import get_coords

def get_climate(lat,long):

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":lat,
        "longitude":long,
        "current":"temperature_2m,relative_humidity_2m,wind_speed_10m,cloud_cover"
    }
    data=requests.get(url,params=params).json()
    curr=data["current"]
   
    return curr

location = "Coorg, Karnataka"

lat, long =  get_coords(location) 

curr = get_climate(lat,long)

print("temperature=",curr["temperature_2m"],"C")
print("relative humidity=",curr["relative_humidity_2m"],"%")
print("wind speed=",curr["wind_speed_10m"],"Km/hr")
