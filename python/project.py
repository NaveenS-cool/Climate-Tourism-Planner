import requests
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude":10.52,
    "longitude":75.21,
    "current":"temperature_2m,relative_humidity_2m,wind_speed_10m,cloud_cover"
}
data=requests.get(url,params=params).json()
curr=data["current"]
print("temperature=",curr["temperature_2m"],"C")
print("relative humidity=",curr["relative_humidity_2m"],"%")
print("wind speed=",curr["wind_speed_10m"],"Km/hr")

