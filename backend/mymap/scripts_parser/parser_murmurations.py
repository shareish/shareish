import requests
import json
from .model import normalize_base
from .model import to_geojson_feature
from .model import process_data

# URL de l'API MurmurMaps pour la Belgique
#URL = "https://murmurmaps.murmurations.network/api/index/nodes?schema=organizations_schema-v1.0.0&country=BE&status=posted&tags_filter=or&tags_exact=false&page_size=30&page=1&index_url=https%3A%2F%2Findex.murmurations.network"
URL = "https://murmurmaps.murmurations.network/api/index/nodes?schema=all&country=BE&status=posted&tags_filter=or&tags_exact=false&page_size=100&page=1&index_url=https%3A%2F%2Findex.murmurations.network"
OUTPUT_FILE="data/murmurmaps_be.geojson"

def fetch_data(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def extract_data(raw_data):
    results = raw_data.get("data", {})
    if isinstance(results, dict):
        items = results.values()
    elif isinstance(results, list):
        items = results
    else:
        items = []
    return items


import requests

def fetch_profile(profile_url):
    if not profile_url:
        return {}

    try:
        r = requests.get(profile_url, timeout=10)
        if r.status_code != 200:
            return {}
        return r.json()
    except Exception:
        return {}

    

def map_murmurations_categories(tags):
    if not tags:
        return ["OT"]

    mapped = set()

    for tag in tags:
        t = tag.lower()

        # --- FOOD ---
        if any(k in t for k in ["food", "agriculture", "permaculture"]):
            mapped.add("FD")

        # --- NATURE / ECOLOGY ---
        if any(k in t for k in ["nature", "ecology", "restoration"]):
            mapped.add("GD")

        # --- COMMUNITY / TRANSITION ---
        if any(k in t for k in ["transition", "community", "collective"]):
            mapped.add("HL")

        # --- EDUCATION ---
        if any(k in t for k in ["education", "learning"]):
            mapped.add("EN")

        # --- REPAIR / DIY ---
        if any(k in t for k in ["repair", "diy", "maker"]):
            mapped.add("DY")

        # --- ENERGY ---
        if any(k in t for k in ["energy"]):
            mapped.add("EY")

    if not mapped:
        mapped.add("OT")

    return list(mapped)


def normalize_murmurations(item, source="murmurations https://murmurmaps.murmurations.network/index-explorer"):
    base = normalize_base()

    #print(item)
    profile = fetch_profile(item.get("profile_url"))
    #print(profile)
    
    # --- Métadonnées ---
    base["source"] = source
    base["type"] = "place"

    # Murmurations n'a pas toujours un ID explicite → fallback URL
    base["external_id"] = item.get("profile_url") or item.get("primary_url")

    # --- Nom ---
    base["name"] = item.get("name")

    # --- Description (parfois absente)
    base["description"] = " ".join(filter(None, [
        base.get("description"),
        profile.get("description"),
        profile.get("mission"),
        base.get("tags")
    ])).strip()

    
    print(base["description"])
    
    # --- Géolocalisation ---
    geo = item.get("geolocation", {})
    base["lat"] = geo.get("lat")
    base["lng"] = geo.get("lon")

    # --- Adresse ---

    #addr = profile.get("full_address", {})
    base["address"] = {
        "street": profile.get("full_address"),
        #"postal_code": addr.get("postalCode"),
        #"city": addr.get("addressLocality"), 
        "country": profile.get("country_iso_3166")
    }

    
    base["street"] = None
    base["postal_code"] = None
    base["city"] = item.get("locality")
    base["country"] = item.get("country")

    # --- Website ---
    website = profile.get("primary_url")
    #base["external_id"]
    # corriger les URLs sans https://
    #if website and not website.startswith("http"):
    #    website = "https://" + website
    base["url"] = website
          
    # --- Email / téléphone ---
    base["email"] = profile.get("contact_details", {}).get("email")
    base["phone"] = None

    # --- Catégories ---
    original_categories = item.get("tags", [])
    base["original_categories"] = original_categories

    base["categories"] = map_murmurations_categories(original_categories)

    # --- Images ---
    base["logo"] = profile.get("image") or "https://murmurations.network/wp-content/uploads/2020/06/murmurations-logo-200.png"
    base["images"] = profile.get("image") or "https://murmurations.network/wp-content/uploads/2020/06/murmurations-logo-200.png"

    # --- Horaires ---
    base["schedule"] = None

    # --- Réseaux sociaux ---
    base["facebook"] = None
    base["instagram"] = None
    base["linkedin"] = None

    # --- Raw ---
    base["raw"] = item

    return base


def main():
    external_data = fetch_data(URL) 
    locations = extract_data(external_data)
    #print(locations);
    geojson = process_data(locations,normalize_murmurations)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)       
    print(f"{len(geojson['features'])} murmurations nodes exported")

    return geojson

if __name__ == "__main__":
    main()
