from django import template

from session_security.settings import ADMIN_WARN_AFTER, WARN_AFTER, ADMIN_EXPIRE_AFTER, EXPIRE_AFTER

register = template.Library()


@register.filter
def expire_after(request):
    if request.user.is_superuser():
        return ADMIN_EXPIRE_AFTER
    return EXPIRE_AFTER


@register.filter
def warn_after(request):
    if request.user.is_superuser():
        return ADMIN_WARN_AFTER
    return WARN_AFTER
