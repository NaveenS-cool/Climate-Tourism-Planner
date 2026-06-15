import requests
from .locator import get_coords


def get_elevation(lat,lon):
    
    url = (
        f"https://api.opentopodata.org/v1/srtm90m"
        f"?locations={lat},{lon}"
    )

    response = requests.get(url).json()

    return response["results"][0]["elevation"]


location = "Munnar, Kerala" #Just a sample location. Edit this to get location from the UI later

lat, long =  get_coords(location)

elev = get_elevation(lat,long)
print("Elevation : ",elev)
