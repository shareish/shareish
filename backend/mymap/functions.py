import re

from geopy import Nominatim

locator = Nominatim(user_agent='shareish')

def verif_location(data):
    if isinstance(data, str):
        address = data.strip()
        if address == "":
            return {'success': None}
        elif re.match("^SRID=4326;POINT \([0-9]+(\.[0-9]+)? [0-9]+(\.[0-9]+)?\)$", address):
            return {'success': address}
        else:
            try:
                location = locator.geocode(address)
                if location is not None:
                    return {'success': "SRID=4326;POINT ({} {})".format(
                        str(location.longitude),
                        str(location.latitude)
                    )}
                else:
                    return {'error': "Couldn't find location."}
            except:
                return {'error': "Third party geolocation service did not work properly."}
    elif isinstance(data, dict):
        if 'longitude' in data and 'latitude' in data:
            address = "SRID=4326;POINT ({} {})".format(data['longitude'], data['latitude'])
            return {'success': address}
        else:
            return {'error': "No suitable address to process."}
    elif data is None:
        return {'success': None}
    else:
        return {'error': "No suitable address to process."}
