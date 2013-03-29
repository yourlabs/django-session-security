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

from settings import *


class SessionSecurityMiddleware(object):
    """
    In charge of maintaining the real 'last activity' time, and log out the
    user if appropriate.
    """

    def process_request(self, request):
        """ Update last activity time or logout. """
        if not request.user.is_authenticated():
            return

        now = datetime.now()
        self.update_last_activity(request, now)

        delta = now - request.session['_session_security']
        if delta.seconds >= EXPIRE_AFTER:
            logout(request)
        elif request.path not in PASSIVE_URLS:
            request.session['_session_security'] = now

    def update_last_activity(self, request, now):
        """
        If ``request.GET['idleFor']`` is set, check if it refers to a more
        recent activity than ``request.session['_session_security']`` and
        update it in this case.
        """
        request.session.setdefault('_session_security', now)
        last_activity = request.session['_session_security']
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
                request.session['_session_security'] = last_activity
