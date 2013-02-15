import datetime

from django import http
from django.contrib.auth import logout

from settings import *


class SessionSecurityMiddleware(object):
    """
    The heart of the security that this application attemps to provide.

    To install this middleware, add to your ``settings.MIDDLEWARE_CLASSES``::

        'session_security.middleware.SessionSecurityMiddleware'
        
    Make sure that it is placed **after** authentication middlewares.
    """

    def process_request(self, request):
        """
        Set up ``request.session['session_security']`` if unset, logout and
        redirect the user to ``LOGIN_URL?next=/the/path/`` if his session has
        expired.

        - If the user is not authenticated: do nothing.
        - If the request url is in ``PASSIVE_URLS``: do nothing.
        - If ``request.session['session_security']`` is unset: set it up.
        - If the seconds elapsed since
          ``request.session['session_security']['last_activity']`` exceeds
          ``EXPIRE_AFTER``:
            - Logout the user,
            - Redirect to ``LOGIN_URL?next=/the/path/``.
        - Otherwise: update
          ``request.session['session_security']['last_activity']`` to now.
        """

        if not request.user.is_authenticated():
            return

        now = datetime.datetime.now()
        request.session.setdefault('_session_security', now)

        delta = now - request.session['_session_security']
        if delta.seconds > EXPIRE_AFTER and request.path_info != LOGIN_URL:
            logout(request)
            if request.is_ajax():
                return http.HttpResponseRedirect(
                    '%s?next=%s' % (LOGIN_URL, request.path_info))
