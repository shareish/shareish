from geopy import Nominatim

locator = Nominatim(user_agent='shareish')

LOCATION_PREFIX = "SRID=4326;POINT"

def verif_location(data):
    if isinstance(data, str):
        address = data.strip()
        if address == "":
            return {'success': ""}
    elif data is None:
        return {'success': ""}
    else:
        return {'error': "No suitable address to process."}

    if not address.startswith(LOCATION_PREFIX):
        location = locator.geocode(address)
        if location is not None:
            return {'success': "{} ({} {})".format(
                LOCATION_PREFIX,
                str(location.latitude),
                str(location.longitude)
            )}
        else:
            return {'error': "Couldn't find location."}
    else:
        return {'success': address}