import requests
import json
from .model import normalize_base
from .model import to_geojson_feature

#URL = "https://www.tierslieux.xyz/co2/search/globalautocomplete?q=belgique"
URL = "https://www.tierslieux.xyz/co2/search/globalautocomplete"

INPUT_FILE="data/tierslieux-raw.json"
OUTPUT_FILE="data/tierslieux.geojson"

#to be refined
def map_tierslieux_categories(original_categories):
    if not original_categories:
        return ["OT"]

    mapped = set()

    for cat in original_categories:
        c = cat.lower()

        # --- FOOD ---
        if any(k in c for k in [
            "alimentation", "maraîchage", "épicerie", "food", "restauration",
            "cuisine", "foodlab", "distribution"
        ]):
            mapped.add("FD")

        # --- GARDEN / NATURE ---
        if any(k in c for k in [
            "nature", "jardin", "permaculture", "écologie",
            "restoration", "biodiversité"
        ]):
            mapped.add("GD")

        # --- DIY / ATELIERS ---
        if any(k in c for k in [
            "atelier", "artisan", "fabrication", "maker", "repair"
        ]):
            mapped.add("DY")

        # --- TOOLS / REPAIR ---
        if any(k in c for k in [
            "repair", "réparation", "outil", "bricolage"
        ]):
            mapped.add("EQ")

        # --- CULTURE / EVENTS ---
        if any(k in c for k in [
            "concert", "festival", "événement", "culture",
            "artistique", "spectacle", "célébration"
        ]):
            mapped.add("EN")

        # --- EDUCATION ---
        if any(k in c for k in [
            "école", "formation", "éducation", "transmission",
            "campus", "eduhub"
        ]):
            mapped.add("EN")

        # --- SOCIAL / MUTUAL AID ---
        if any(k in c for k in [
            "coopérative", "lien social", "intergénérationnel",
            "solidarité", "tierslieu", "commun"
        ]):
            mapped.add("HL")

        # --- CHILDHOOD ---
        if any(k in c for k in [
            "enfance", "petite enfance", "one"
        ]):
            mapped.add("CH")

        # --- MOBILITY / TRANSPORT ---
        if any(k in c for k in [
            "mobilité", "transport", "bus", "vélo", "parking"
        ]):
            mapped.add("TS")

        # --- ENERGY ---
        if any(k in c for k in [
            "énergie", "chauffage"
        ]):
            mapped.add("EY")

        # --- HOUSE / SPACE ---
        if any(k in c for k in [
            "hébergement", "logement", "espace", "lieu"
        ]):
            mapped.add("HS")

    # fallback
    if not mapped:
        mapped.add("OT")

    return list(mapped)


def parse_opening_hours(opening_hours):
    if not opening_hours:
        return None

    lines = []

    # --- Cas 1 : liste ---
    if isinstance(opening_hours, list):
        for oh in opening_hours:

            # --- sous-cas objet structuré ---
            if isinstance(oh, dict):
                day = oh.get("dayOfWeek")

                for h in oh.get("hours", []):
                    if isinstance(h, dict):
                        opens = h.get("opens")
                        closes = h.get("closes")

                        if day and opens and closes:
                            lines.append(f"{day}: {opens} - {closes}")

            # --- sous-cas string ---
            elif isinstance(oh, str):
                lines.append(oh)

    # --- Cas 2 : string directe ---
    elif isinstance(opening_hours, str):
        lines.append(opening_hours)

    # --- Cas 3 : autre (fallback) ---
    else:
        lines.append(str(opening_hours))

    return "\n".join(lines) if lines else None



def normalize_tierslieux(item, source="tierslieux_xyz https://www.tierslieux.xyz/#cartographie"):
    base = normalize_base()

    # --- Métadonnées ---
    if isinstance(item.get("_id"), dict):
        base["external_id"] = item["_id"].get("$id")
    else:
        base["external_id"] = item.get("_id")

    base["source"] = source
    base["type"] = "place"

    # --- Nom ---
    base["name"] = item.get("name")

    # --- Description ---
    base["description"] = item.get("description") or item.get("shortDescription")

    # --- Géolocalisation ---
    lat = None
    lng = None

    if item.get("geoPosition"):
        coords = item["geoPosition"].get("coordinates", [])
        if len(coords) == 2:
            lng, lat = coords
    elif item.get("geo"):
        lat = item["geo"].get("latitude")
        lng = item["geo"].get("longitude")

    try:
        base["lat"] = float(lat) if lat else None
        base["lng"] = float(lng) if lng else None
    except:
        base["lat"] = None
        base["lng"] = None

    # adresse
    addr = item.get("address", {})
    base["address"] = {
        "street": addr.get("streetAddress"),
        "postal_code": addr.get("postalCode"),
        "city": addr.get("addressLocality"), 
        "country": addr.get("addressCountry") or addr.get("level1Name")
    }
    
    # --- Website ---
    base["url"] = "https://www.tierslieux.xyz/#page.type.organizations.id."+base["external_id"]  #item.get("url") or item.get("primary_url")
    #print(base["website"])
    #6811d8c16624bb6eba1a0904

    # --- Email ---
    base["email"] = item.get("email")

    # --- Téléphone (absent ici généralement) ---
    base["phone"] = None

    # --- Images ---
    images = []
    #images are not publicly available therefore not used, or we put the full URL to tierslieux.../.../
    #if item.get("profilImageUrl"):
    #    images.append(item["profilImageUrl"])
    #elif item.get("profilMediumImageUrl"):
    #    images.append(item["profilMediumImageUrl"])

    base["images"] = images if images else None

    # --- Horaires ---
    base["schedule"] = parse_opening_hours(item.get("openingHours"))

    # --- Catégories ---
    original_categories = item.get("tags", [])
    base["original_categories"] = original_categories

    base["categories"] = map_tierslieux_categories(original_categories)

    # --- Réseaux sociaux ---
    base["facebook"] = None
    base["instagram"] = None
    base["linkedin"] = None

    # --- Raw (toujours utile pour debug / RAG) ---
    base["raw"] = item

    return base


#this fetch function uses payload that might break, another option would be to copy-paste the json output directly from the browser
#into a local file.
def fetch_data(url):
    payload = {
        "searchType[]": "organizations",
        "filters[$or][source.keys]": "tierslieuxbelgique",
        "sortBy[name]": 1,
        "indexMin": 0,
        "indexStep": 0,
        "count": True,
        "costumSlug": "tierslieuxbelgique",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, data=payload, headers=headers)

    print(response.status_code)
    return response.json()


    

def extract_data(raw_data, key=None):
    results = raw_data.get("results", {})
    if isinstance(results, dict):
        items = results.values()
    elif isinstance(results, list):
        items = results
    else:
        items = []
        
    return items


def process_data(features):
    output_features = []

    for feature in features:
        data = normalize_tierslieux(feature)

        # sécurité minimale
        if data["lat"] is None or data["lng"] is None:
            continue

        geojson_feature = to_geojson_feature(data,None)
        output_features.append(geojson_feature)

    return {
        "type": "FeatureCollection",
        "features": output_features
    }



def main():
    external_data = fetch_data(URL) 
    locations = extract_data(external_data)
    #print(locations);
    geojson = process_data(locations)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)
        
    print(f"{len(geojson['features'])} tiers-lieux exportés")

    return geojson

if __name__ == "__main__":
    main()
