import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def get_coords(location):

    url = "https://nominatim.openstreetmap.org/search"
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
    if not data:
        return False
    

    lat = data[0]["lat"]
    long = data[0]["lon"]

    return lat, long


