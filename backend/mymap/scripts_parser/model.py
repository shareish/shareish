def normalize_base():
    return {
        "type": None,  # "place" | "event"
        "external_id": None,
        
        "name": None,
        "description": None,

        "lat": None,
        "lng": None,

        "address": {
            "street": None,
            "number": None,
            "postal_code": None,
            "city": None,
            "country": None,
        },

        #contact
        "url": None,
        "phone": None,
        "email": None,
        
        # social
        "facebook": None,
        "instagram": None,
        "linkedin": None,

        # other content
        "schedule": None,
        "logo": None,
        "images": [],
        
        # important
        "categories": [],              # normalisées (shareish)
        "categories_original": [],     # brutes

        # metadata
        "source": None,

        # spécifique événements
        "start_date": None,
        "end_date": None,

        # extension libre
        "extras": {}
    }


SHAREISH_CATEGORIES = {
    "FD": "food",
    "AN": "animals",
    "EN": "entertainment",
    "CL": "collectors",
    "HL": "helping",
    "AT": "administrative",
    "DY": "diy",
    "BT": "beauty",
    "HE": "health",
    "EY": "energy",
    "CH": "childhood",
    "CO": "clothes",
    "IT": "it",
    "CS": "software",
    "GD": "garden",
    "HS": "house",
    "EQ": "tools",
    "HD": "holidays",
    "BK": "book",
    "MD": "media",
    "SP": "sport",
    "TS": "transport",
    "VE": "vehicle",
    "PR": "publicresource",
    "OT": "other",
}


def build_description(data):
    parts = []

    if data.get("name"):
        parts.append(f"<h3>{data['name']}</h3>")

    if data.get("logo"):
        parts.append(f'<img src="{data["logo"]}" style="max-height:80px;"><br>')

    # adresse
    addr = data.get("address", {})
    address_str = " ".join(filter(None, [
        addr.get("street"),
        addr.get("postal_code"),
        addr.get("city")
    ]))
    if address_str:
        parts.append(f"<p>📍 {address_str}</p>")

    # description
    if data.get("description"):
        parts.append(f"<div>{data['description']}</div>")

    # catégories originales (important)
    if data.get("categories_original"):
        parts.append(f"<p><b>Catégories:</b> {', '.join(data['categories_original'])}</p>")

    # horaires
    if data.get("schedule"):
        parts.append(f"<p><b>Horaires:</b><br>{data['schedule']}</p>")

    # contact
    if data.get("url"):
        parts.append(f'<p>🌐 <a href="{data["url"]}" target="_blank">Site web</a></p>')

    if data.get("phone"):
        parts.append(f"<p>📞 {data['phone']}</p>")

    if data.get("email"):
        parts.append(f"<p>📧 {data['email']}</p>")

    # réseaux sociaux
    if data.get("facebook"):
        parts.append(f'<p><a href="{data["facebook"]}" target="_blank">Facebook</a></p>')

    if data.get("instagram"):
        parts.append(f'<p><a href="{data["instagram"]}" target="_blank">Instagram</a></p>')

    if data.get("linkedin"):
        parts.append(f'<p><a href="{data["linkedin"]}" target="_blank">LinkedIn</a></p>')

    if data.get("source"):
        parts.append(f"<p><b>Source</b>: {data['source']}</p>")
        
    images = data.get("images")
    if isinstance(images, list) and len(images) > 0:
        parts.append(f'<img src="{images[0]}" style="max-width:100%; max-height:200px;"><br>')
    
    return "\n".join(parts)



def build_umap_options(data,icon_mapping):
    icon = None
    
    # priorité aux catégories originales pour les icones umap
    original_categories = data.get("categories_original", [])
    if original_categories and icon_mapping:
        for cat in original_categories:
            if cat in icon_mapping:
                icon = icon_mapping[cat]
                break

    # fallback vers catégories normalisées
    if not icon:
        normalized_categories = data.get("categories", [])
        icon_map = {
            "FD": "greengrocer.svg",
            "CO": "clothes.svg",
            "CL": "recycling.svg",
            "GD": "garden.svg",
            "EY": "power-wind.svg",
            "HS": "castle-manor.svg",
            "EQ": "doityourself.svg",
            "HT": "doctor.svg",
            "BT": "chemist.svg",
            "EN": "museum.svg",
            "OT": "recycling.svg",
            "HL": "pitch.svg",
        }
        for cat in normalized_categories:
            if cat in icon_map:
                icon = icon_map[cat]
                break
            
    return {
        "iconClass": "Drop",
        "iconUrl": f"/uploads/pictogram/{icon}",
        "color": "green"
    }



def clean_dict(d):
    return {
        k: v for k, v in d.items()
        if v not in [None, "", [], {}]
    }

def to_geojson_feature(data,icon_mapping):
    addr = data.get("address", {})

    properties = clean_dict({
        "name": data["name"],
        "external_id": data["external_id"],
        "description": build_description(data),
        "url": data.get("url"),
        "phone": data.get("phone"),
        "email": data.get("email"),
        "facebook": data.get("facebook"),
        "instagram": data.get("instagram"),
        "linkedin": data.get("linkedin"),
        "schedule": data.get("schedule"),
        "logo": data.get("logo"),
        "images": data.get("images"),
        "categories": data.get("categories"),
        "categories_original": data.get("categories_original"),
        "source": data.get("source"),
    })
    
    # options uMap
    umap_options = clean_dict(build_umap_options(data,icon_mapping))

    if umap_options:
        properties["_umap_options"] = umap_options

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [data["lng"], data["lat"]],
        },
        "properties": properties
    }


#Given a list of normalized features, this function generate a Featurecollection in geojson
def process_data(features, normalize_func):
    output_features = []
    
    for feature in features:
        data = normalize_func(feature)

        # sécurité minimale
        if data.get("lat") is None or data.get("lng") is None:
            continue

        geojson_feature = to_geojson_feature(data,None)
        output_features.append(geojson_feature)

    return {
        "type": "FeatureCollection",
        "features": output_features
    }
