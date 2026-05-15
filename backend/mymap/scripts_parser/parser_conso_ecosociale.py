import requests
import json
import re
from .model import normalize_base
from .model import to_geojson_feature

URL = "https://conso.economiesociale.be/"
OUTPUT_FILE="data/ecosociale_full_new.geojson"

CONCERTES_ICON_MAPPING = {
    "recup": "recycling.svg",
    "alimentation": "greengrocer.svg",
    "parcs-jardins": "garden.svg",
    "construction-travaux": "castle-manor.svg",
    "energie": "power-wind.svg",
    "titres-services": "copyshop.svg",
}

CONCERTES_CATEGORY_MAPPING = {
    # jardin / nature
    "parcs-jardins": ["GD"],

    # réemploi / seconde main
    "recup": ["CO", "CL"],  # vêtements + objets

    # alimentation
    "alimentation": ["FD"],

    # construction / habitat
    "construction-travaux": ["HS", "EQ"],

    # énergie
    "energie": ["EY"],

    # services (souvent aide à domicile)
    "titres-services": ["HL", "HS"],
}

def fetch_source(url):
    return fetch_html(url);
    
def fetch_html(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text


#function to get all categories in this source based on sectors data field
# ['alimentation', 'construction-travaux', 'energie', 'parcs-jardins', 'recup', 'titres-services']
def collect_categories(locations):
    all_categories = set()

    for loc in locations.values():
        sectors = loc.get("sectors", {})

        if isinstance(sectors, dict):
            all_categories.update(sectors.keys())
        elif isinstance(sectors, list):
            all_categories.update(sectors)

    return sorted(all_categories)


def map_concertes_categories(sectors):
    result = set()

    if isinstance(sectors, dict):
        keys = sectors.keys()
    elif isinstance(sectors, list):
        keys = sectors
    else:
        keys = []

    for key in keys:
        if key in CONCERTES_CATEGORY_MAPPING:
            result.update(CONCERTES_CATEGORY_MAPPING[key])
        else:
            result.add("OT")  # fallback

    return list(result)


def normalize_concertes(key,loc, source="ConcertES https://conso.economiesociale.be/"):
    base = normalize_base()

    print(loc);
    base["type"] = "place"
    base["source"] = source
    base["external_id"] = key

    base["name"] = loc.get("name")
    base["description"] = loc.get("content")

    # coordonnées
    marker = loc.get("marker", [None, None])
    if marker and len(marker) == 2:
        base["lat"], base["lng"] = marker

    # adresse
    addr = loc.get("address", {})
    base["address"] = {
        "street": addr.get("street"),
        "number": None,
        "postal_code": addr.get("zip"),
        "city": addr.get("city"),
        "country": addr.get("country"),
    }

    base["url"] = loc.get("website_url")
    base["phone"] = loc.get("phone")
    base["email"] = loc.get("email")

    # social
    base["facebook"] = loc.get("facebook")
    base["instagram"] = loc.get("instagram")
    base["linkedin"] = loc.get("linkedin")

    base["schedule"] = loc.get("schedule")
    base["logo"] = loc.get("logo")
    photos = loc.get("photos")
    if isinstance(photos, list):
        base["images"] = photos
    elif isinstance(photos, str):
        base["images"] = [photos]
    else:
        base["images"] = []

    
    # catégories
    sectors = loc.get("sectors", {})
    base["categories_original"] = list(sectors.keys()) if isinstance(sectors, dict) else sectors
    base["categories"] = map_concertes_categories(sectors)

    return base


def extract_data(html,var_name):
    return extract_js_object(html,var_name);

#extract data from URL html output
def extract_js_object(html, var_name):
    # Trouver "var sectors = {" ou variantes
    pattern = re.compile(rf"{var_name}\s*=\s*\{{", re.IGNORECASE)
    match = pattern.search(html)

    if not match:
        raise ValueError(f"Variable '{var_name}' introuvable")

    start = match.end() - 1  # position du '{'

    brace_count = 0
    end = start

    for i in range(start, len(html)):
        if html[i] == "{":
            brace_count += 1
        elif html[i] == "}":
            brace_count -= 1

        if brace_count == 0:
            end = i + 1
            break

    raw_json = html[start:end]

    return json.loads(raw_json)


def process_data(locations):
    return process_concertes(locations)

def process_concertes(locations):
    features = []

    print(locations)
    for key,loc in locations.items():
        norm_data = normalize_concertes(key,loc)
        feature = to_geojson_feature(norm_data,CONCERTES_ICON_MAPPING)
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }


   
  
def main():

    #all_categories = collect_categories(locations);
    #print("---------------------------------------------------------------------------");
    #print(all_categories);
    #print("---------------------------------------------------------------------------");
    #sectors = extract_js_object(html, "sectors")


    
    features = []
    external_data = fetch_source(URL)
    locations = extract_data(external_data, "locations")
    geojson = process_data(locations)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)
    print("Fichier geojson généré ------------------")

    return geojson

if __name__ == "__main__":
    main()
