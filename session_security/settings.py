import warnings

from django.conf import settings

__all__ = ['SECONDS', 'LOGIN_URL']

SECONDS = getattr(settings, 'SESSION_EXPIRY_SECONDS', 600)

LOGIN_URL = settings.LOGIN_URL

if not getattr(settings, 'SESSION_EXPIRE_AT_BROWSER_CLOSE', False):
    warnings.warn('settings.SESSION_EXPIRE_AT_BROWSER_CLOSE is not True')
