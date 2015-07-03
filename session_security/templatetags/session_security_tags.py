from django import template

from session_security.settings import (
    WARN_AFTER, EXPIRE_AFTER, CONFIRM_FORM_DISCARD
)

register = template.Library()


@register.filter
def expire_after(request):
    return EXPIRE_AFTER


@register.filter
def warn_after(request):
    return WARN_AFTER


@register.filter
def confirm_form_discard(request):
    return CONFIRM_FORM_DISCARD
