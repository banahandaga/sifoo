from django import template
from django.urls import reverse

register = template.Library()

@register.filter(name='setempty')
def setempty(value):
    if value is not None:
        return value
    return ''