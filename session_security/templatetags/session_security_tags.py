from django import template

from session_security.settings import (
    get_expire_after, get_warn_after)

register = template.Library()


@register.filter
def expire_after(request):
    return get_expire_after(request)


@register.filter
def warn_after(request):
    return get_warn_after(request)
