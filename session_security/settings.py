"""
Settings for django-session-security.

EXPIRE_AFTER
    The number of seconds after which the session should expire if the
    authenticated user is idle. Default is 600, so if a user opens a page, and
    leaves his browser during 10 minutes, the session will expire. Overridable
    through settings.SESSION_SECURITY_EXPIRE_AFTER

WARN_AFTER
    The number of seconds before session expiry that should trigger the warning
    dialog. Default is 30, so if the user opens a page, and leaves his browser,
    a dialog will show up 30 seconds before the session expires, allowing the
    user to extend his session. Overridable through
    settings.SESSION_SECURITY_WARN_AFTER.

PASSIVE_URLS
    Urls that should not count as activity when hit. For example, an ajax
    request that pings the server without the user consent's should be added to
    PASSIVE_URLS. PASSIVE_URLS is a list overridable through
    settings.SESSION_SECURITY_PASSIVE_URLS.

LOGOUT_URL
    The url to use for logout. Note that it will be passed a GET argument,
    'next', with the url from which the user was logged-out. Overridable
    through settings.LOGOUT_URL.

LOGIN_URL
    The url to use for login. Like LOGOUT_URL, it is passed a GET request
    argument, 'next', and is overridable through settings.LOGIN_URL.

Note that this module will raise a warning if
settings.SESSION_EXPIRE_AT_BROWSER_CLOSE is not True.
"""

import warnings

from django.core import urlresolvers
from django.conf import settings

__all__ = ['EXPIRE_AFTER', 'WARN_AFTER', 'LOGIN_URL', 'LOGOUT_URL', 'PASSIVE_URLS', 'SKEW_MARGIN']

EXPIRE_AFTER = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 600)

WARN_AFTER = getattr(settings, 'SESSION_SECURITY_WARN_AFTER', 30)

LOGIN_URL = settings.LOGIN_URL

LOGOUT_URL = getattr(settings, 'LOGOUT_URL', False)

SKEW_MARGIN = getattr(settings, 'SESSION_SECURITY_SKEW_MARGIN', 3)

PASSIVE_URLS = getattr(settings, 'SESSION_SECURITY_PASSIVE_URLS', [])
PASSIVE_URLS += [
    urlresolvers.reverse('session_security_ping'),
    LOGOUT_URL,
]

if not LOGOUT_URL:
    if 'pinax.apps.account' in settings.INSTALLED_APPS:
        LOGOUT_URL = urlresolvers.reverse('acct_logout')
    else:
        raise Exception('LOGOUT_URL not configured, session_security cannot work')

if not getattr(settings, 'SESSION_EXPIRE_AT_BROWSER_CLOSE', False):
    warnings.warn('settings.SESSION_EXPIRE_AT_BROWSER_CLOSE is not True')
