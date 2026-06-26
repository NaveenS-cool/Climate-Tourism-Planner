import requests
import pandas as pd
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
import streamlit as st


@st.cache_data(ttl=5400,show_spinner=False)
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
    today=date.today().isoformat()
    current={}
    data = requests.get(url, params=params, headers={"User-Agent": "ClimateTourismPlanner"}).json()
    daily = data["daily"]
    for i in range(len(daily["time"])):
        if daily["time"][i]==today:
            current={0:today,1:daily["temperature_2m_mean"][i],2: daily["relative_humidity_2m_mean"][i],3:daily["precipitation_sum"][i]}




    return data["daily"],current

@st.cache_data
def fetch_year_window(lat, long, year_offset):

    print("cache miss")

    today = date.today()
    target_year = today.year - year_offset
    center_date = date(target_year,today.month,today.day)
    start_date = center_date - timedelta(days=7)
    end_date = center_date + timedelta(days=7)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "daily": ["temperature_2m_mean","relative_humidity_2m_mean", "precipitation_sum"],
        "timezone": "Asia/Kolkata"
    }
    resp = requests.get(url, params=params, headers={"User-Agent": "ClimateTourismPlanner"})
    return resp.json()["daily"]

def hist_climate(lat,long):


    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:

        responses = list(
            executor.map(
            lambda offset: fetch_year_window(lat,long,offset), range(1,6)
            )
        )
    for data in responses:
        for i in range(len(data["time"])):
            results.append({
                "date": data["time"][i],
                "temp_mean": data["temperature_2m_mean"][i],
                "rh_mean": data["relative_humidity_2m_mean"][i],
                "precipitation": data["precipitation_sum"][i],
            })
    
    df = pd.DataFrame(results)

    hist_data = {
        "temp_mean" : float(df["temp_mean"].mean()),
        "temp_std" : float(df["temp_mean"].std()),

        "rh_mean" : float(df["rh_mean"].mean()),
        "rh_std" : float(df["rh_mean"].std()),

        "precipitation_mean" : float(df["precipitation"].mean()),
        "precipitation_std" : float(df["precipitation"].std())
    }

    return hist_data



