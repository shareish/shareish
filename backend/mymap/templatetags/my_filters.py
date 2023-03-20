from django.template import Library

register = Library()


@register.filter
def get_key(dictionary, key):
    return dictionary.get(key)


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def ellipsis(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|ellipsis }}
        {{ string|ellipsis:50 }}
    """

    try:
        limit = int(limit)
    except ValueError:
        # Fail silently.
        return value

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Return string with removed useless spaces
    return value.strip() + '...'
