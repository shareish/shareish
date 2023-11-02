import re

from geopy import Nominatim

locator = Nominatim(user_agent='shareish')

def verif_location(data):
    srid = None
    if data is not None:
        if isinstance(data, str):
            address = data.strip()
            if address != "":
                # Verifies the most common form of location first
                match = re.match("^SRID=4326;POINT \((-?\d+(\.\d+)?) (-?\d+(\.\d+)?)\)$", address)
                if match:
                    srid = address
                else:
                    # Builds the coords separating chars options
                    coords_separating_options = [
                        " ",
                        ",", ", ", " ,", " , ",
                        "-", "- ", " -", " - ",
                        ":", ": ", " :", " : ",
                    ]
                    coords_separating_options_regex = "(" + "|".join(coords_separating_options) + ")"

                    # Looks for coords in decimal format
                    match = re.match("^(-?\d+(\.\d+)?)" + coords_separating_options_regex + "(-?\d+(\.\d+)?)$", address)
                    if match:
                        latitude = float(match.group(1))
                        longitude = float(match.group(4))

                        # Verifies that values are in the correct range
                        if abs(latitude) <= 90:
                            if abs(longitude) <= 180:
                                srid = "SRID=4326;POINT ({} {})".format(str(longitude), str(latitude))
                            else:
                                return {'error': "Latitude value is invalid."}
                        else:
                            return {'error': "Longitude value is invalid."}
                    else:
                        # Looks for coords using orientation
                        match = re.match("^(\d+)°((\d+)['’])?((\d+(\.\d+)?)[\"″])?([NnEeSsWw])" + coords_separating_options_regex + "(\d+)°((\d+)['’])?((\d+(\.\d+)?)[\"″])?([NnEeSsWw])$", address)
                        if match:
                            first_is_lat = match.group(7) in ('N', 'n', 'S', 's')
                            second_is_lat = match.group(15) in ('N', 'n', 'S', 's')
                            if first_is_lat != second_is_lat:
                                # Sets to 0 all the None values that need to represent a coordinates value to
                                # be able to sum them later
                                values = {}
                                for k, value in enumerate(match.groups()):
                                    if k + 1 in (1, 3, 5, 9, 11, 13) and value is None:
                                        values[k] = 0
                                    else:
                                        values[k] = value

                                # Converts degrees to decimals
                                first = float(values[0]) + float(values[2])/60 + float(values[4])/3600
                                second = float(values[8]) + float(values[10])/60 + float(values[12])/3600

                                # Switches to negative if in South or West part of the world
                                if match.group(7) in ('S', 's') or match.group(7) in ('W', 'w'):
                                    first = -first
                                if match.group(15) in ('S', 's') or match.group(15) in ('W', 'w'):
                                    second = -second

                                latitude = first if first_is_lat else second
                                longitude = second if first_is_lat else first

                                # Verifies that values are in the correct range
                                if abs(latitude) <= 90:
                                    if abs(longitude) <= 180:
                                        srid = "SRID=4326;POINT ({} {})".format(str(longitude), str(latitude))
                                    else:
                                        return {'error': "Latitude value is invalid."}
                                else:
                                    return {'error': "Longitude value is invalid."}
                            else:
                                return {'error': "One value must be north or south and the other one east or west."}
                        else:
                            # It's a string complete address that we need to find
                            try:
                                loc = locator.geocode(address)
                                if loc is not None:
                                    srid = "SRID=4326;POINT ({} {})".format(str(loc.longitude), str(loc.latitude))
                                else:
                                    return {'error': "Couldn't find location."}
                            except:
                                return {'error': "Third party geolocation service did not work properly."}
        elif isinstance(data, dict):
            if 'latitude' in data and 'longitude' in data:
                latitude = data['longitude']
                longitude = data['latitude']

                # Verifies if the values are in accepted formats
                if isinstance(latitude, str) or isinstance(latitude, int) or isinstance(latitude, float):
                    if isinstance(longitude, str) or isinstance(longitude, int) or isinstance(longitude, float):
                        latitude = float(data['longitude'])
                        longitude = float(data['latitude'])

                        # Verifies that values are in the correct range
                        if abs(latitude) <= 90:
                            if abs(longitude) <= 180:
                                srid = "SRID=4326;POINT ({} {})".format(str(longitude), str(latitude))
                            else:
                                return {'error': "Longitude value is invalid."}
                        else:
                            return {'error': "Latitude value is invalid."}
                    else:
                        return {'error': "Longitude value is invalid."}
                else:
                    return {'error': "Latitude value is invalid."}
            else:
                return {'error': "No suitable address to process."}
        else:
            return {'error': "No suitable address to process."}

    return {'success': srid}