from django import template

from session_security.settings import WARN_AFTER, EXPIRE_AFTER

register = template.Library()


@register.filter
def expire_after(request):
    return EXPIRE_AFTER


@register.filter
def warn_after(request):
    return WARN_AFTER
