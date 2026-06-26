import re
import requests
import streamlit as st


def is_valid_location_query(query):
    if not query or not isinstance(query, str):
        return False
    query = query.strip()
    if len(query) < 2:
        return False
        
    # Check if there are invalid characters.
    # Allow alphanumeric characters (including unicode), spaces, commas, hyphens, periods, apostrophes, and a single ampersand.
    if not re.match(r"^[\w\s,\-'.&]+$", query):
        return False
        
    # Check for consecutive special symbols (e.g. '&&', '--', ',,')
    if re.search(r"&{2,}|-{2,}|,{2,}|\.{2,}|'{2,}", query):
        return False
        
    # If there is an ampersand, it shouldn't be leading or trailing
    if '&' in query:
        if query.startswith('&') or query.endswith('&'):
            return False
            
    # Must contain at least one letter (Unicode-aware check)
    if not any(c.isalpha() for c in query):
        return False
        
    return True


@st.cache_data(show_spinner=False)
def get_coords(location):
    if not is_valid_location_query(location):
        return False

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers={"User-Agent": "ClimateTourismPlanner/1.0 (contact@example.com)"},
            timeout=10
        )
        if response.status_code != 200:
            return False

        data = response.json()
        if not data:
            return False

        lat = data[0]["lat"]
        long = data[0]["lon"]

        return lat, long
    except (requests.exceptions.RequestException, ValueError):
        return False


