from django.template import Library

register = Library()


@register.filter(name='times')
def times(number, multiplier):
    return number * multiplier


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)
