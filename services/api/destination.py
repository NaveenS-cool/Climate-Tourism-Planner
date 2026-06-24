import time
import requests
from collections import defaultdict

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

PLACE_CATEGORIES = {
    "beach":        {"natural": ["coastline"],"place": ["islet", "island"]}, 
    "mountain":     {"natural": ["peak", "ridge", "saddle", "cliff","mountain","hill"]}, 
    "waterbodies":   {"water": ["lake", "reservoir"]}, 
    "forest":       {"landuse": ["forest"],
                     "leisure": ["nature_reserve"]}, 
    "urban": {"place": ["city","town"]},
    "village": {"place": ["village","hamlet","isolated_dwelling"]},
    "wildlife":  {"boundary": ["national_park","protected_area"], "leisure" : ["nature_reserve"]}

}

CATEGORY_WEIGHTS = {
    "beach": 5,
    "mountain": 4,
    "forest": 2,
    "wildlife": 3,
    "waterbodies": 2,
    "village": 2,
    "urban": 1,
    "other": 0
}


def classify_tags(tags):
    matched = []
    for category, tag_map in PLACE_CATEGORIES.items():
        for tag_key, values in tag_map.items():
            if tags.get(tag_key) in values:
                matched.append(category)
                break
    return matched or ["other"]


def get_terrain_type(lat, lon, radius=5000):

    query = f"""
[out:json][timeout:25];

(
  node(around:{radius},{lat},{lon})["natural"];
  way(around:{radius},{lat},{lon})["natural"];
  relation(around:{radius},{lat},{lon})["natural"];

  node(around:{radius},{lat},{lon})["water"];
  way(around:{radius},{lat},{lon})["water"];
  relation(around:{radius},{lat},{lon})["water"];

  node(around:{radius},{lat},{lon})["landuse"];
  way(around:{radius},{lat},{lon})["landuse"];
  relation(around:{radius},{lat},{lon})["landuse"];

  node(around:{radius},{lat},{lon})["place"];
  way(around:{radius},{lat},{lon})["place"];
  relation(around:{radius},{lat},{lon})["place"];

  node(around:{radius},{lat},{lon})["boundary"];
  way(around:{radius},{lat},{lon})["boundary"];
  relation(around:{radius},{lat},{lon})["boundary"];

  node(around:{radius},{lat},{lon})["leisure"];
  way(around:{radius},{lat},{lon})["leisure"];
  relation(around:{radius},{lat},{lon})["leisure"];
);

out tags;
"""

    headers = {
        "User-Agent": "ClimaTourismPlanner",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                OVERPASS_URL, data={"data": query}, headers=headers, timeout=95
            )
            response.raise_for_status()
            data = response.json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Overpass API attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                print("All Overpass API retries exhausted. Returning fallback.")
                return {"coords": (lat, lon), "primary": "unknown", "all_types": [], "places": []}

    type_counts = defaultdict(int)
    places = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name", "Unnamed")

        if "center" in el:
            el_lat, el_lon = el["center"]["lat"], el["center"]["lon"]
        else:
            el_lat, el_lon = el.get("lat"), el.get("lon")

        categories = classify_tags(tags)
        for cat in categories:
            type_counts[cat] += CATEGORY_WEIGHTS[cat]

        places.append({
            "name": name,
            "lat": el_lat,
            "lon": el_lon,
            "categories": categories,
            "tags": tags,
        })

    primary = max(type_counts, key=type_counts.get) if type_counts else "unknown"
    all_types = sorted(type_counts, key=type_counts.get, reverse=True)
    print(type_counts)

    return {
        "coords": (lat, lon),
        "primary": primary,
        "all_types": all_types,
        "places": places,
    }

