import requests

url = "https://nominatim.openstreetmap.org/search"


def get_coords(location):
    params = {
        "q": location,
        "format": "json"
    }

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "ClimateTourismPlanner"}
    )

    data = response.json()

    lat = data[0]["lat"]
    long = data[0]["lon"]

    return lat, long


