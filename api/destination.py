import requests
from collections import defaultdict
from locator import get_coords

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

PLACE_CATEGORIES = {
    "beach":        {"natural": ["beach", "sand"], "leisure": ["beach_resort"]},
    "mountain":     {"natural": ["peak", "ridge", "saddle", "cliff", "arete", "mountain"]},
    "hill":         {"natural": ["hill"]},
    "waterfall":    {"waterway": ["waterfall"], "natural": ["waterfall"]},
    "river_lake":   {"natural": ["water", "bay", "spring", "hot_spring"],
                     "waterway": ["river", "stream", "lake"]},
    "forest":       {"natural": ["wood"], "landuse": ["forest"],
                     "leisure": ["nature_reserve"]},
    "cave":         {"natural": ["cave_entrance"]},
    "valley":       {"natural": ["valley", "gorge"]},
    "volcano":      {"natural": ["volcano"]},
    "wetland":      {"natural": ["wetland", "marsh", "mangrove", "mud"]},
    "island":       {"place": ["island", "islet"]},
    "park":         {"leisure": ["park", "garden"],
                     "landuse": ["recreation_ground", "village_green"]},
    "wildlife":     {"leisure": ["bird_hide", "wildlife_hide"]},
    "viewpoint":    {"tourism": ["viewpoint"]},
    "historic":     {"historic": ["castle", "fort", "ruins", "archaeological_site",
                                  "monument", "battlefield"]},
    "religious":    {"amenity": ["place_of_worship"]},
}

def classify_tags(tags):
    matched = []
    for category, tag_map in PLACE_CATEGORIES.items():
        for tag_key, values in tag_map.items():
            if tags.get(tag_key) in values:
                matched.append(category)
                break
    return matched or ["other"]


def get_terrain_type(lat,lon, radius=1000):

    query = f"""
    [out:json][timeout:25];
    (
      node["natural"](around:{radius},{lat},{lon});
      node["waterway"~"river|stream|waterfall"](around:{radius},{lat},{lon});
      node["leisure"~"park|garden|nature_reserve|beach_resort|bird_hide"](around:{radius},{lat},{lon});
      node["tourism"="viewpoint"](around:{radius},{lat},{lon});
      node["historic"](around:{radius},{lat},{lon});
      node["amenity"="place_of_worship"](around:{radius},{lat},{lon});
      node["place"~"island|islet"](around:{radius},{lat},{lon});
      way["natural"](around:{radius},{lat},{lon});
      way["waterway"](around:{radius},{lat},{lon});
      way["landuse"~"forest|reservoir|recreation_ground"](around:{radius},{lat},{lon});
      way["leisure"~"park|garden|nature_reserve"](around:{radius},{lat},{lon});
    );
    out center tags;
    """

    headers = {
        "User-Agent": "ClimaTourismPlanner",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(OVERPASS_URL, data={"data": query}, headers=headers)
    response.raise_for_status()
    data = response.json()

    type_counts = defaultdict(int)
    places = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name", "Unnamed")

        # get coords
        if "center" in el:
            el_lat, el_lon = el["center"]["lat"], el["center"]["lon"]
        else:
            el_lat, el_lon = el.get("lat"), el.get("lon")

        categories = classify_tags(tags)
        for cat in categories:
            type_counts[cat] += 1

        places.append({
            "name": name,
            "lat": el_lat,
            "lon": el_lon,
            "categories": categories,
            "tags": tags,
        })

    primary = max(type_counts, key=type_counts.get) if type_counts else "unknown"
    all_types = sorted(type_counts, key=type_counts.get, reverse=True)

    return {
        "coords": (lat, lon),
        "primary": primary,
        "all_types": all_types,
        "places": places,
    }

location = "Coorg, Karnataka"

lat, long =  get_coords(location) 

result = get_terrain_type(lat,long)

print(f"Primary terrain : {result['primary']}")  # We will use the primary terrain during analysis
print(f"All types found : {result['all_types']}")
