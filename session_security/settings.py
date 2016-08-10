"""
Settings for django-session-security.

WARN_AFTER
    Time (in seconds) before the user should be warned that is session will
    expire because of inactivity. Default 540. Overridable in
    ``settings.SESSION_SECURITY_WARN_AFTER``.

EXPIRE_AFTER
    Time (in seconds) before the user should be logged out if inactive. Default
    is 600. Overridable in ``settings.SESSION_SECURITY_EXPIRE_AFTER``.

PASSIVE_URLS
    List of urls that should be ignored by the middleware. For example the ping
    ajax request of session_security is made without user intervention, as such
    it should not be used to update the user's last activity datetime.
    Overridable in ``settings.SESSION_SECURITY_PASSIVE_URLS``.

EXPIRATION_MESSAGE
    Let's you set a default logout message displayed after the user is logged
    out. Uses Django's message service. Default is None.

PREVENT_LOGOUT_FOR_SUPERUSERS
    If you want to keep staff/superusers always logged in, set this value
    to True. Default is False.

Note that this module will raise a warning if
``settings.SESSION_EXPIRE_AT_BROWSER_CLOSE`` is not True, because it makes no
sense to use this app with ``SESSION_EXPIRE_AT_BROWSER_CLOSE`` to False.
"""

import warnings

from django.core import urlresolvers
from django.conf import settings

__all__ = ['EXPIRE_AFTER', 'WARN_AFTER', 'PASSIVE_URLS', 'EXPIRATION_MESSAGE']

EXPIRE_AFTER = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 600)

WARN_AFTER = getattr(settings, 'SESSION_SECURITY_WARN_AFTER', 540)

EXPIRATION_MESSAGE = getattr(
    settings, 'SESSION_SECURITY_EXPIRATION_MESSAGE', None)

PREVENT_LOGOUT_FOR_SUPERUSERS = getattr(
    settings, 'SESSION_SECURITY_PREVENT_LOGOUT_FOR_SUPERUSERS', False)

PASSIVE_URLS = getattr(settings, 'SESSION_SECURITY_PASSIVE_URLS', [])
PASSIVE_URLS += [
    urlresolvers.reverse('session_security_ping'),
]

if not getattr(settings, 'SESSION_EXPIRE_AT_BROWSER_CLOSE', False):
    warnings.warn('settings.SESSION_EXPIRE_AT_BROWSER_CLOSE is not True')
