from django import template
register = template.Library()
@register.filter
def split_by_dash(value):
    return value.split('-')
@register.filter
def strip_char(value, char):
    return value.rstrip(char)