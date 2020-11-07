"""
SessionSecurityMiddleware is the heart of the security that this application
attemps to provide.

To install this middleware, add to your ``settings.MIDDLEWARE_CLASSES``::

    'session_security.middleware.SessionSecurityMiddleware'

Make sure that it is placed **after** authentication middlewares.
"""

from datetime import datetime, timedelta

import django
from django.contrib.auth import logout
try: # Django 2.0
    from django.urls import reverse, resolve, Resolver404
except: # Django < 2.0
    from django.core.urlresolvers import reverse, resolve, Resolver404

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # Works perfectly for everyone using MIDDLEWARE_CLASSES
    MiddlewareMixin = object

from .utils import get_last_activity, set_last_activity
from .settings import EXPIRE_AFTER, PASSIVE_URLS, PASSIVE_URL_NAMES


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    In charge of maintaining the real 'last activity' time, and log out the
    user if appropriate.
    """

    def is_passive_request(self, request):
        """ Should we skip activity update on this URL/View. """
        if request.path in PASSIVE_URLS:
            return True

        try:
            match = resolve(request.path)
            # TODO: check namespaces too
            if match.url_name in PASSIVE_URL_NAMES:
                return True
        except Resolver404:
            pass

        return False

    def get_expire_seconds(self, request):
        """Return time (in seconds) before the user should be logged out."""
        return EXPIRE_AFTER

    def process_request(self, request):
        """ Update last activity time or logout. """
        
        if django.VERSION < (1, 10):
            is_authenticated = request.user.is_authenticated()
        else:
            is_authenticated = request.user.is_authenticated

        if not is_authenticated:
            return

        now = datetime.now()
        if '_session_security' not in request.session:
            set_last_activity(request.session, now)
            return

        delta = now - get_last_activity(request.session)
        expire_seconds = self.get_expire_seconds(request)
        if delta >= timedelta(seconds=expire_seconds):
            logout(request)
        elif (request.path == reverse('session_security_ping') and
                'idleFor' in request.GET):
            self.update_last_activity(request, now)
        elif not self.is_passive_request(request):
            set_last_activity(request.session, now)

    def update_last_activity(self, request, now):
        """
        If ``request.GET['idleFor']`` is set, check if it refers to a more
        recent activity than ``request.session['_session_security']`` and
        update it in this case.
        """
        last_activity = get_last_activity(request.session)
        server_idle_for = (now - last_activity).seconds

        # Gracefully ignore non-integer values
        try:
            client_idle_for = int(request.GET['idleFor'])
        except ValueError:
            return

        # Disallow negative values, causes problems with delta calculation
        if client_idle_for < 0:
            client_idle_for = 0

        if client_idle_for < server_idle_for:
            # Client has more recent activity than we have in the session
            last_activity = now - timedelta(seconds=client_idle_for)

        # Update the session
        set_last_activity(request.session, last_activity)
