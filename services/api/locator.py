import requests
import streamlit as st


@st.cache_data
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

    lat = data[0]["lat"]
    long = data[0]["lon"]

    return lat, long


