import re

from geopy import Nominatim

locator = Nominatim(user_agent='shareish')

def verif_location(data):
    if isinstance(data, str):
        address = data.strip()
        if address == "":
            return {'success': ""}
    elif data is None:
        return {'success': ""}
    else:
        return {'error': "No suitable address to process."}

    if not re.match("^SRID=4326;POINT \([0-9]+(\.[0-9]+)? [0-9]+(\.[0-9]+)?\)$", address):
        location = locator.geocode(address)
        if location is not None:
            return {'success': "SRID=4326;POINT ({} {})".format(
                str(location.longitude),
                str(location.latitude)
            )}
        else:
            return {'error': "Couldn't find location."}
    else:
        return {'success': address}