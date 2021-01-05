from django import template

register = template.Library()


@register.filter
def keyvalue(a_dict, key):
    try:
        return a_dict[key]
    except KeyError:
        return ""
