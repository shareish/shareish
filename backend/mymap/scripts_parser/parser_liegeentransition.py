import json
from .model import normalize_base
from .model import to_geojson_feature
from .model import process_data

INPUT_FILE = "data/li_ge_en_transition.geojson"
OUTPUT_FILE = "data/liege_en_transition_clean.geojson"


def map_icon(url):
    if not url:
        return url

    # mapping par mot-clé (plus robuste)
    if "recycling" in url:
        return "/uploads/pictogram/recycling.svg"
    if "spring" in url:
        return "/uploads/pictogram/garden.svg"
    if "convenience" in url:
        return "/uploads/pictogram/convenience.svg"
    if "restaurant" in url:
        return "/uploads/pictogram/restaurant.svg"
    if "florist" in url:
        return "/uploads/pictogram/garden.svg"
    if "embassy" in url:
        return "/uploads/pictogram/embassy.svg"
    if "alcohol" in url:
        return "/uploads/pictogram/alcohol.svg"
    if "kiosk" in url:
        return "/uploads/pictogram/kiosk.svg"
    if "viewpoint" in url:
        return "/uploads/pictogram/viewpoint.svg"
    if "bicycle" in url:
        return "/uploads/pictogram/bicycle.svg"
    if "railway" in url:
        return "/uploads/pictogram/railway-station.svg"
    return url


def fetch_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_data(raw_data, key=None):
    data = json.loads(raw_data)
    return data.get("features", [])


def map_osm_to_shareish(osm_value):
    mapping = {
        "farm": ["FD", "GD"],   # nourriture + jardin
        "bakery": ["FD"],
        "supermarket": ["FD"],
        "clothes": ["CO"],
        "hairdresser": ["BT"],
        "school": ["EN"],
    }

    return mapping.get(osm_value, ["OT"])


def normalize_liege_en_transition(feature, source="Liège en Transition https://liegetransition.be/carte-des-initiatives"):
    base = normalize_base()

    props = feature.get("properties", {})
    geom = feature.get("geometry", {})

    base["type"] = "place"
    base["source"] = source

    # ID externe
    base["external_id"] = feature.get("id")

    # nom / description
    base["name"] = props.get("name")
    base["description"] = props.get("description")

    # coords
    coords = geom.get("coordinates", [None, None])
    if coords and len(coords) == 2:
        base["lng"], base["lat"] = coords

    # adresse
    base["address"] = {
        "street": props.get("street"),
        "number": props.get("housenumber"),
        "postal_code": props.get("postcode"),
        "city": props.get("city"),
        "country": props.get("country"),
    }

    # OSM
    base["osm"] = {
        "id": props.get("osm_id"),
        "type": props.get("osm_type"),
        "key": props.get("osm_key"),
        "value": props.get("osm_value"),
    }

    # catégories (faible signal → fallback simple)
    osm_value = props.get("osm_value")
    if osm_value:
        base["categories_original"] = [osm_value]

    base["categories"] = map_osm_to_shareish(osm_value)

    return base


def main():
    external_data = fetch_data(INPUT_FILE)
    locations = extract_data(external_data)
    geojson = process_data(locations,normalize_liege_en_transition)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)

    print("Fichier geojson Liege en transition généré ------------------")

    return geojson
    
if __name__ == "__main__":
    main()

    
