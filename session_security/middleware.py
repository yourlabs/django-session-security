"""
SessionSecurityMiddleware is the heart of the security that this application
attemps to provide.

To install this middleware, add to your ``settings.MIDDLEWARE_CLASSES``::

    'session_security.middleware.SessionSecurityMiddleware'

Make sure that it is placed **after** authentication middlewares.
"""

import time
from datetime import datetime, timedelta

from django import http
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

from .utils import get_last_activity, set_last_activity
from .settings import EXPIRE_AFTER, PASSIVE_URLS


class SessionSecurityMiddleware(object):
    """
    In charge of maintaining the real 'last activity' time, and log out the
    user if appropriate.
    """

    def is_passive_request(self, request):
        return request.path in PASSIVE_URLS

    def process_request(self, request):
        """ Update last activity time or logout. """
        if not request.user.is_authenticated():
            return

        now = datetime.now()
        self.update_last_activity(request, now)

        delta = now - get_last_activity(request.session)
        if delta >= timedelta(seconds=EXPIRE_AFTER):
            logout(request)
        elif not self.is_passive_request(request):
            set_last_activity(request.session, now)

    def update_last_activity(self, request, now):
        """
        If ``request.GET['idleFor']`` is set, check if it refers to a more
        recent activity than ``request.session['_session_security']`` and
        update it in this case.
        """
        if '_session_security' not in request.session:
            set_last_activity(request.session, now)

        last_activity = get_last_activity(request.session)
        server_idle_for = (now - last_activity).seconds

        if (request.path == reverse('session_security_ping') and
                'idleFor' in request.GET):
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
