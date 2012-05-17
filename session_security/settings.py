import warnings

from django.conf import settings

__all__ = ['EXPIRE_AFTER', 'WARN_BEFORE', 'LOGIN_URL', 'LOGOUT_URL']

EXPIRE_AFTER = getattr(settings, 'SESSION_SECURITY_EXPIRE_AFTER', 600)

WARN_BEFORE = getattr(settings, 'SESSION_SECURITY_WARN_BEFORE', 20)

LOGIN_URL = settings.LOGIN_URL

LOGOUT_URL = getattr(settings, 'LOGOUT_URL', False)

if not LOGOUT_URL:
    if 'pinax.apps.account' in settings.INSTALLED_APPS:
        LOGOUT_URL = urlresolvers.reverse('acct_logout')
    else:
        raise Exception('LOGOUT_URL not configured, session_security cannot work')

if not getattr(settings, 'SESSION_EXPIRE_AT_BROWSER_CLOSE', False):
    warnings.warn('settings.SESSION_EXPIRE_AT_BROWSER_CLOSE is not True')
