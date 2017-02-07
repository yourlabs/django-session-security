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

PASSIVE_URL_NAMES
    Same as PASSIVE_URLS, but takes Django URL names instead of a path. This
    is useful in case path names change, or contain parameterized values, and
    thus cannot be described statically. NOTE: currently namespaces are not
    handled. Overridable in ``settings.SESSION_SECURITY_PASSIVE_URL_NAMES``.

SESSION_SECURITY_INSECURE
    Set this to True in your settings if you want the project to run without
    having to set SESSION_EXPIRE_AT_BROWSER_CLOSE=True, which you should
    because it makes no sense to use this app with
    ``SESSION_EXPIRE_AT_BROWSER_CLOSE`` to False.
"""
from django.conf import settings

__all__ = ['EXPIRE_AFTER', 'WARN_AFTER', 'PASSIVE_URLS']

EXPIRE_AFTER = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 600)

WARN_AFTER = getattr(settings, 'SESSION_SECURITY_WARN_AFTER', 540)

PASSIVE_URLS = getattr(settings, 'SESSION_SECURITY_PASSIVE_URLS', [])

PASSIVE_URL_NAMES = getattr(settings, 'SESSION_SECURITY_PASSIVE_URL_NAMES', [])

expire_at_browser_close = getattr(
    settings,
    'SESSION_EXPIRE_AT_BROWSER_CLOSE',
    False
)
force_insecurity = getattr(
    settings,
    'SESSION_SECURITY_INSECURE',
    False
)

if not (expire_at_browser_close or force_insecurity):
    raise Exception(
        'Enable SESSION_EXPIRE_AT_BROWSER_CLOSE or SESSION_SECURITY_INSECURE'
    )
