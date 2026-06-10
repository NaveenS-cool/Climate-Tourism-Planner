from locator import get_coords

location = "Munnar, Kerala" #Just a sample location. Edit this to get location from the UI later

lat, long =  get_coords(location) #Find climate data from the given coordinates

print("Latitude : ",lat)
print("Longitude : ",long)