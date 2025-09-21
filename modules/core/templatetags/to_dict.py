from django import template
import json

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_dict(value):
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return mark_safe(value)
