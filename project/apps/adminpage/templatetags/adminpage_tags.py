from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.auth.models import User

register = template.Library()


# ==============================================================================================
#                                         AUTHORIZATION 
# ==============================================================================================

@register.filter('has_group')
def has_group(user, groups_name):
    if user.groups.filter(name__in=[arg.strip() for arg in groups_name.split(',')]).exists() | user.is_superuser:
        return True
    return False






# ==============================================================================================
#                                       CONTROL SIDEBAR
# ==============================================================================================
@register.filter(name='setactive')
def setactive(path, url):
    if path.lower() == reverse(url).lower():
        return 'active'
    return ''


@register.filter(name='setactiveopen')
def setactiveopen(path, url):
    inputurl = url.split('/')
    path = path.split('/')
    prefix = path[:(len(inputurl))]
    if url == '/'.join(prefix):
        return 'active open'
    return ''


@register.filter(name='setshow')
def setshow(path, url):
    inputurl = url.split('/')
    path = path.split('/')
    prefix = path[:(len(inputurl))]
    if url == '/'.join(prefix):
        return 'show'
    return ''





# ==============================================================================================
#                                      DATA MANIPULATION
# ==============================================================================================

@register.filter(name='JsonParseIsEmpty')
def JsonParseIsEmpty(value):
    if value and value is not None:
        return value
    return '{}'


@register.filter(name='getUrlSegment')
def getUrlSegment(path, index):
    path = path.split('/')
    return (path[index]).title()


@register.filter(name='ifempty')
def ifempty(value, default):
    if value and value is not None:
        return value
    return default
