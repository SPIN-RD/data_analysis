from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def startswith(text, starts):
    return text.startswith(starts)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
